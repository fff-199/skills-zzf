#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const { searchWechatDetailed } = require('./search_wechat');

const DEFAULT_BROWSERS = [
  process.env.CHROME_PATH,
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
].filter(Boolean);

function parseArgs(argv) {
  const args = {
    query: '',
    url: '',
    num: 3,
    output: '',
    format: 'json',
    provider: 'sogou',
    headful: false,
    browser: '',
    timeoutMs: 20000,
  };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if ((arg === '-n' || arg === '--num') && argv[i + 1]) {
      args.num = Math.max(1, Math.min(10, Number(argv[++i] || 3)));
    } else if ((arg === '-u' || arg === '--url') && argv[i + 1]) {
      args.url = argv[++i];
    } else if ((arg === '-o' || arg === '--output') && argv[i + 1]) {
      args.output = argv[++i];
    } else if ((arg === '-f' || arg === '--format') && argv[i + 1]) {
      args.format = String(argv[++i]).toLowerCase();
    } else if ((arg === '-p' || arg === '--provider') && argv[i + 1]) {
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

function getBrowserPath(explicitPath) {
  const candidates = explicitPath ? [explicitPath] : DEFAULT_BROWSERS;
  return candidates.find((candidate) => candidate && fs.existsSync(candidate));
}

function normalizeText(value) {
  return String(value || '').replace(/\r/g, '').replace(/\n{3,}/g, '\n\n').trim();
}

function renderMarkdown(result) {
  const lines = [`# ${result.query}`, ''];
  for (const article of result.articles) {
    lines.push(`## ${article.title || 'Untitled'}`);
    lines.push('');
    lines.push(`- source: ${article.source || ''}`);
    lines.push(`- publish_time: ${article.publish_time || ''}`);
    lines.push(`- url: ${article.url || ''}`);
    lines.push(`- status: ${article.fetch_status || ''}`);
    lines.push('');
    if (article.summary) {
      lines.push(article.summary);
      lines.push('');
    }
    if (article.content) {
      lines.push(article.content);
      lines.push('');
    }
  }
  return lines.join('\n').trim() + '\n';
}

async function extractArticle(page, article, timeoutMs) {
  await page.goto(article.url, { waitUntil: 'domcontentloaded', timeout: timeoutMs });
  const contentTimeoutMs = Math.max(5000, Math.min(timeoutMs, 15000));

  await Promise.race([
    page.waitForSelector('#js_content, .rich_media_content, article', { timeout: contentTimeoutMs }).catch(() => null),
    page.waitForFunction(() => {
      const text = document.body?.innerText || '';
      return (
        text.includes('以下内容需登录后查看') ||
        text.includes('请在微信客户端打开链接') ||
        text.includes('此内容因违规无法查看')
      );
    }, { timeout: contentTimeoutMs }).catch(() => null),
  ]);
  await page.waitForTimeout(1500);

  const snapshot = await page.evaluate(() => {
    const title =
      document.querySelector('#activity-name')?.textContent ||
      document.querySelector('.rich_media_title')?.textContent ||
      document.title;
    const author =
      document.querySelector('#js_name')?.textContent ||
      document.querySelector('.rich_media_meta_nickname')?.textContent ||
      '';
    const publishTime =
      document.querySelector('#publish_time')?.textContent ||
      document.querySelector('.rich_media_meta_text')?.textContent ||
      '';
    const contentRoot =
      document.querySelector('#js_content') ||
      document.querySelector('.rich_media_content') ||
      document.querySelector('article');
    const loginWall = document.body.innerText.includes('以下内容需登录后查看') ||
      document.body.innerText.includes('请在微信客户端打开链接');
    const removed = document.body.innerText.includes('此内容因违规无法查看');
    const antiBot =
      location.href.includes('/antispider/') ||
      document.body.innerText.includes('不是自动程序发出的') ||
      document.body.innerText.includes('验证码用于确认这些请求是您的正常行为');

    return {
      finalUrl: location.href,
      title: title?.trim() || '',
      author: author?.trim() || '',
      publishTime: publishTime?.trim() || '',
      content: contentRoot?.innerText?.trim() || '',
      loginWall,
      removed,
      antiBot,
    };
  });

  const fetchStatus = snapshot.antiBot
    ? 'antibot'
    : snapshot.removed
    ? 'removed'
    : snapshot.loginWall
      ? 'login_required'
      : snapshot.content
        ? 'ok'
        : 'empty';

  return {
    ...article,
    url: snapshot.finalUrl || article.url,
    title: snapshot.title || article.title,
    source: snapshot.author || article.source,
    publish_time: snapshot.publishTime || '',
    content: normalizeText(snapshot.content),
    fetch_status: fetchStatus,
  };
}

async function primeSogouSession(page, query, timeoutMs) {
  const url = `https://weixin.sogou.com/weixin?type=2&query=${encodeURIComponent(query)}&page=1&ie=utf8`;
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: timeoutMs });
  await page.waitForTimeout(2000);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.query && !args.url) {
    console.log('Usage: node scripts/fetch_wechat_content.js "关键词" [-n 3] [-o output.json] [-f json|md] [-p sogou|auto|brave] [--headful] [-b chrome.exe]');
    console.log('   or: node scripts/fetch_wechat_content.js --url "https://mp.weixin.qq.com/s/..."');
    process.exit(0);
  }

  const browserPath = getBrowserPath(args.browser);
  if (!browserPath) {
    throw new Error('No supported Chrome/Edge executable found. Pass one with -b or set CHROME_PATH.');
  }

  const warnings = [];
  const searchResult = args.url
    ? { providerUsed: '', warnings: [], articles: [] }
    : await searchWechatDetailed(args.query, args.num, {
        resolveUrl: false,
        provider: args.provider,
      });
  const searchResults = searchResult.articles;
  warnings.push(...searchResult.warnings);
  const useSogouRelayLinks = searchResult.providerUsed === 'sogou' && !args.url;
  const targetArticles = args.url
    ? [{ title: '', summary: '', source: '', url: args.url, date_description: '' }]
    : searchResults.filter(
        (item) =>
          item.url.includes('mp.weixin.qq.com') ||
          (useSogouRelayLinks && item.url.includes('weixin.sogou.com/link'))
      );

  if (!targetArticles.length) {
    warnings.push(
      searchResult.providerUsed === 'sogou'
        ? 'Keyword search did not return any usable Sogou article links.'
        : 'Keyword search did not return any direct mp.weixin.qq.com article URLs.'
    );
  }

  const browser = await chromium.launch({
    headless: !args.headful,
    executablePath: browserPath,
  });

  const context = await browser.newContext({
    locale: 'zh-CN',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    viewport: { width: 1400, height: 1200 },
  });

  const page = await context.newPage();
  const articles = [];

  try {
    if (useSogouRelayLinks && targetArticles.length) {
      await primeSogouSession(page, args.query, args.timeoutMs);
    }

    for (const article of targetArticles) {
      try {
        const result = await extractArticle(page, article, args.timeoutMs);
        articles.push(result);
      } catch (error) {
        articles.push({
          ...article,
          publish_time: '',
          content: '',
          fetch_status: `error: ${error.message}`,
        });
      }
      await page.waitForTimeout(1200);
    }
  } finally {
    await context.close();
    await browser.close();
  }

  const result = {
    query: args.query,
    url: args.url || '',
    searched: searchResults.length,
    resolved: targetArticles.length,
    fetched: articles.length,
    search_provider_requested: args.provider,
    search_provider_used: searchResult.providerUsed || '',
    browser_path: browserPath,
    generated_at: new Date().toISOString(),
    warnings,
    articles,
  };

  if (!articles.length && searchResults.length) {
    result.articles = searchResults.map((article) => ({
      ...article,
      publish_time: '',
      content: '',
      fetch_status: useSogouRelayLinks ? 'relay_link_not_opened' : 'unresolved_url',
    }));
  }

  const rendered = args.format === 'md' ? renderMarkdown(result) : JSON.stringify(result, null, 2);
  if (args.output) {
    fs.writeFileSync(path.resolve(args.output), rendered, 'utf8');
  }
  console.log(rendered);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
