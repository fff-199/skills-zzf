#!/usr/bin/env node

const fs = require('fs');
const https = require('https');
const cheerio = require('cheerio');

const DEFAULT_BROWSERS = [
  process.env.CHROME_PATH,
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
].filter(Boolean);

function request(url, headers = {}, redirectCount = 0) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers }, (res) => {
      if (
        res.statusCode >= 300 &&
        res.statusCode < 400 &&
        res.headers.location &&
        redirectCount < 5
      ) {
        const nextUrl = new URL(res.headers.location, url).toString();
        res.resume();
        resolve(request(nextUrl, headers, redirectCount + 1));
        return;
      }

      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    });
    req.on('error', reject);
    req.setTimeout(20000, () => {
      req.destroy(new Error('Request timeout'));
    });
  });
}

function parseArgs(argv) {
  const args = {
    query: '',
    num: 10,
    output: '',
    resolveUrl: false,
    provider: 'sogou',
    browser: '',
    headful: false,
    timeoutMs: 20000,
  };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '-n' || arg === '--num') {
      args.num = Math.max(1, Math.min(50, Number(argv[++i] || 10)));
    } else if (arg === '-o' || arg === '--output') {
      args.output = argv[++i] || '';
    } else if (arg === '-r' || arg === '--resolve-url') {
      args.resolveUrl = true;
    } else if (arg === '-p' || arg === '--provider') {
      args.provider = String(argv[++i] || 'auto').toLowerCase();
    } else if ((arg === '-b' || arg === '--browser') && argv[i + 1]) {
      args.browser = argv[++i];
    } else if ((arg === '-t' || arg === '--timeout') && argv[i + 1]) {
      args.timeoutMs = Math.max(5000, Number(argv[++i] || 20000));
    } else if (arg === '--headful') {
      args.headful = true;
    } else if (!arg.startsWith('-') && !args.query) {
      args.query = arg;
    }
  }
  return args;
}

function normalizeUrl(url) {
  if (!url) return '';
  const cleaned = String(url).replace(/&amp;/g, '&').trim();
  if (cleaned.startsWith('/')) return `https://weixin.sogou.com${cleaned}`;
  return cleaned;
}

function normalizeProvider(provider) {
  const value = String(provider || 'sogou').toLowerCase();
  if (value === 'auto' || value === 'brave' || value === 'sogou') {
    return value;
  }
  throw new Error(`Unsupported provider "${provider}". Use auto, brave, or sogou.`);
}

function attachSearchMeta(articles, meta) {
  return Object.assign(articles, meta);
}

function getBrowserPath(explicitPath) {
  const candidates = explicitPath ? [explicitPath] : DEFAULT_BROWSERS;
  return candidates.find((candidate) => candidate && fs.existsSync(candidate));
}

function resultSourceLabel(value) {
  const text = extractText(value);
  return text || 'WeChat Public Platform';
}

function parseBravePage(html, limit) {
  const $ = cheerio.load(html);
  const items = [];
  const seen = new Set();

  $('div.result-content').each((_, el) => {
    if (items.length >= limit) return false;

    const root = $(el);
    const link = root.find('a.l1[href^="https://mp.weixin.qq.com/"], a[href^="https://mp.weixin.qq.com/"]').first();
    const url = normalizeUrl(link.attr('href'));
    if (!url || seen.has(url)) return;

    seen.add(url);
    items.push({
      title: extractText(link.find('.title').first()) || extractText(link),
      url,
      summary:
        extractText(root.find('.generic-snippet .content').first()) ||
        extractText(root.find('[class*="snippet"] [class*="content"]').first()),
      source: resultSourceLabel(root.find('.site-name-content .desktop-small-semibold').first()),
      date_description: ''
    });
  });

  if (!items.length) {
    $('a[href^="https://mp.weixin.qq.com/"]').each((_, el) => {
      if (items.length >= limit) return false;

      const link = $(el);
      const url = normalizeUrl(link.attr('href'));
      if (!url || seen.has(url)) return;

      seen.add(url);
      items.push({
        title: extractText(link.find('.title').first()) || extractText(link),
        url,
        summary: '',
        source: 'WeChat Public Platform',
        date_description: ''
      });
    });
  }

  return items;
}

async function searchWechatWithBrave(query, num) {
  const searchQuery = `site:mp.weixin.qq.com ${query}`;
  const url = `https://search.brave.com/search?q=${encodeURIComponent(searchQuery)}&source=web`;
  const html = await request(url, {
    'User-Agent': 'Mozilla/5.0',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
  });
  return parseBravePage(html, num);
}

function parseSogouPage(html, limit) {
  const $ = cheerio.load(html);
  const items = [];
  $('ul.news-list li').each((_, el) => {
    if (items.length >= limit) return false;
    const root = $(el);
    const link = root.find('h3 a').first();
    if (!link.length) return;

    const source = extractText(root.find('.account').first()) || extractText(root.find('.all-time-y2').first());
    const timeText = extractText(root.find('.s2').first().clone().children().remove().end());

    items.push({
      title: extractText(link),
      url: normalizeUrl(link.attr('href')),
      summary: extractText(root.find('p.txt-info').first()),
      source,
      date_description: timeText
    });
  });
  return items;
}

async function searchWechatWithSogou(query, num, resolveUrl) {
  const encoded = encodeURIComponent(query);
  const results = [];
  const pages = Math.ceil(num / 10);

  for (let page = 1; page <= pages && results.length < num; page++) {
    const url = `https://weixin.sogou.com/weixin?type=2&query=${encoded}&page=${page}&ie=utf8`;
    const html = await request(url, {
      'User-Agent': 'Mozilla/5.0',
      'Referer': 'https://weixin.sogou.com/',
      'Accept-Language': 'zh-CN,zh;q=0.9'
    });
    const pageItems = parseSogouPage(html, num - results.length);
    if (!pageItems.length) break;
    results.push(...pageItems);
  }

  if (resolveUrl) {
    for (const item of results) {
      item.url = await resolveWechatUrl(item.url);
    }
  }

  return results;
}

async function resolveWechatUrlsInBrowser(results, query, options = {}) {
  const unresolved = results.filter((item) => item.url.includes('weixin.sogou.com/link'));
  if (!unresolved.length) {
    return [];
  }

  const warnings = [];
  const browserPath = getBrowserPath(options.browser);
  if (!browserPath) {
    warnings.push('No supported Chrome/Edge executable found for browser-based Sogou link resolution.');
    return warnings;
  }

  let chromium;
  try {
    ({ chromium } = require('playwright-core'));
  } catch (error) {
    warnings.push(`playwright-core is unavailable for browser-based Sogou link resolution: ${error.message}`);
    return warnings;
  }

  const browser = await chromium.launch({
    headless: !options.headful,
    executablePath: browserPath,
  });

  const context = await browser.newContext({
    locale: 'zh-CN',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    viewport: { width: 1400, height: 1200 },
  });

  const page = await context.newPage();

  try {
    const searchUrl = `https://weixin.sogou.com/weixin?type=2&query=${encodeURIComponent(query)}&page=1&ie=utf8`;
    await page.goto(searchUrl, {
      waitUntil: 'domcontentloaded',
      timeout: options.timeoutMs || 20000,
    });
    await page.waitForTimeout(2000);

    for (const item of unresolved) {
      try {
        await page.goto(item.url, {
          waitUntil: 'domcontentloaded',
          timeout: options.timeoutMs || 20000,
        });
        await page.waitForFunction(() => {
          return (
            location.href.includes('mp.weixin.qq.com') ||
            location.href.includes('/antispider/') ||
            !location.href.includes('weixin.sogou.com/link')
          );
        }, {
          timeout: Math.max(5000, Math.min(options.timeoutMs || 20000, 15000)),
        }).catch(() => null);
        await page.waitForTimeout(1000);
        const finalUrl = page.url();
        if (finalUrl.includes('mp.weixin.qq.com')) {
          item.url = finalUrl;
        }
      } catch {
        // Fall back to the original URL and let the HTTP resolver try afterward.
      }
    }
  } finally {
    await context.close();
    await browser.close();
  }

  return warnings;
}

async function searchWechatDetailed(query, num, options = {}) {
  const provider = normalizeProvider(options.provider || 'sogou');
  const resolveUrl = Boolean(options.resolveUrl);
  const warnings = [];

  if (provider === 'auto' || provider === 'brave') {
    const braveResults = await searchWechatWithBrave(query, num);
    if (braveResults.length) {
      if (num > braveResults.length) {
        warnings.push(`Brave returned ${braveResults.length} direct mp.weixin.qq.com results on the first page.`);
      }
      return {
        providerUsed: 'brave',
        warnings,
        articles: braveResults
      };
    }

    if (provider === 'brave') {
      warnings.push('Brave did not return any direct mp.weixin.qq.com results for this query.');
      return {
        providerUsed: 'brave',
        warnings,
        articles: []
      };
    }

    warnings.push('Brave search returned no direct mp.weixin.qq.com links. Falling back to Sogou HTML results.');
  }

  const sogouResults = await searchWechatWithSogou(query, num, false);
  if (resolveUrl && sogouResults.some((item) => item.url.includes('weixin.sogou.com'))) {
    warnings.push(...await resolveWechatUrlsInBrowser(sogouResults, query, options));
    for (const item of sogouResults) {
      if (item.url.includes('weixin.sogou.com')) {
        item.url = await resolveWechatUrl(item.url);
      }
    }
    if (sogouResults.some((item) => item.url.includes('weixin.sogou.com'))) {
      warnings.push('Some Sogou relay links could not be resolved to direct mp.weixin.qq.com URLs.');
    }
  }

  return {
    providerUsed: 'sogou',
    warnings,
    articles: sogouResults
  };
}

async function searchWechat(query, num, resolveUrl = false, provider = 'sogou') {
  const result = await searchWechatDetailed(query, num, { resolveUrl, provider });
  return attachSearchMeta(result.articles, {
    providerUsed: result.providerUsed,
    warnings: result.warnings
  });
}

function extractText(node) {
  return node.text().replace(/\s+/g, ' ').trim();
}

function parsePage(html, limit) {
  return parseSogouPage(html, limit);
}

async function resolveWechatUrl(url) {
  if (!url.includes('weixin.sogou.com')) return url;
  return new Promise((resolve) => {
    const req = https.get(url, {
      headers: { 'User-Agent': 'Mozilla/5.0' }
    }, (res) => {
      const location = res.headers.location;
      if (location && location.includes('mp.weixin.qq.com')) {
        resolve(location);
        return;
      }
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        const html = Buffer.concat(chunks).toString('utf8');
        const match = html.match(/https:\/\/mp\.weixin\.qq\.com[^"'\\s<>]+/);
        resolve(match ? match[0].replace(/&amp;/g, '&') : url);
      });
    });
    req.on('error', () => resolve(url));
    req.setTimeout(10000, () => {
      req.destroy();
      resolve(url);
    });
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.query) {
    console.log('Usage: node scripts/search_wechat.js "关键词" [-n 10] [-o result.json] [-r] [-p sogou|auto|brave] [-b chrome.exe] [--headful]');
    process.exit(0);
  }

  const result = await searchWechatDetailed(args.query, args.num, {
    resolveUrl: args.resolveUrl,
    provider: args.provider,
    browser: args.browser,
    headful: args.headful,
    timeoutMs: args.timeoutMs,
  });
  const output = JSON.stringify({
    query: args.query,
    total: result.articles.length,
    provider_requested: normalizeProvider(args.provider),
    provider_used: result.providerUsed,
    warnings: result.warnings,
    articles: result.articles
  }, null, 2);

  if (args.output) {
    fs.writeFileSync(args.output, output, 'utf8');
  }
  console.log(output);
}

module.exports = {
  searchWechat,
  searchWechatDetailed,
  resolveWechatUrl,
};

if (require.main === module) {
  main().catch((error) => {
    console.error(error.message);
    process.exit(1);
  });
}
