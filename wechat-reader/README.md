# wechat-reader

Read WeChat public account (微信公众号) articles. Activate when the user shares a mp.weixin.qq.com link, asks to read/summarize a WeChat article, or mentions 公众号/微信文章. These pages are JS-rendered and blocked by simple web fetch, so use the local Chrome/Edge rendering path instead.

## Portable Entry Point

- Start here if you are using this repository from a non-Codex agent.
- The original Codex-oriented source remains in `SKILL.md` for reference.
- Run bundled scripts relative to this folder, for example `./wechat-reader/scripts/...` from the repo root.

## Adapted Instructions

# WeChat Article Reader

## Why This Skill Exists

微信公众号文章（`mp.weixin.qq.com/s/...`）经常是动态渲染页面，简单抓取只能拿到标题或残缺内容。这个 skill 现在优先走本机 Chrome/Edge 渲染脚本，而不是旧的 `browser(...)` 伪接口。

## Preferred Path

1. 识别用户消息里的 `mp.weixin.qq.com` 链接
2. 直接运行本地脚本：

```bash
node scripts/read_wechat_article.js --url "https://mp.weixin.qq.com/s/..."
```

3. 如果用户要 Markdown 输出：

```bash
node scripts/read_wechat_article.js --url "https://mp.weixin.qq.com/s/..." -f md
```

4. 如果需要可视化浏览器：

```bash
node scripts/read_wechat_article.js --url "https://mp.weixin.qq.com/s/..." --headful
```

5. 读取脚本输出，向用户总结或翻译正文

## Fallback Path

如果本地脚本不可用，再使用当前环境里的 Chrome DevTools 工具：

1. `mcp__chrome_devtools__new_page` 打开文章链接
2. 等待标题或正文容器出现
3. `mcp__chrome_devtools__evaluate_script` 提取 `#activity-name`、`#publish_time`、`#js_name`、`#js_content`
4. 如果页面显示登录墙、违规移除、或“请在微信客户端打开链接”，直接告知用户

## Tips

- 已知真实 `mp.weixin.qq.com` 链接时，不要再走搜狗中转
- 多篇文章顺序处理，避免同时拉起多个浏览器实例
- 如果文章过长，优先输出结构化摘要，不必原样回传全文
- 如果页面显示“此内容因违规无法查看”或需要登录，不要尝试绕过验证

## Resource Map

### Scripts
- `scripts/read_wechat_article.js`

## Source

- Original skill definition: `SKILL.md`
