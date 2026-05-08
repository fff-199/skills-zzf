# wechat-article-search

搜索微信公众号文章技能。通过关键词检索公众号文章列表，并返回标题、摘要、来源与可访问链接。当用户需要查找公众号文章、整理参考资料或快速定位可读的微信文章直链时使用此技能。

## Portable Entry Point

- Start here if you are using this repository from a non-Codex agent.
- The original Codex-oriented source remains in `SKILL.md` for reference.
- Run bundled scripts relative to this folder, for example `./wechat-article-search/scripts/...` from the repo root.

## Adapted Instructions

# 微信公众号文章搜索说明

## 适用场景

- 用户说“帮我搜某个关键词的公众号文章/最近文章”
- 需要快速拿到：标题、摘要、公众号名称、可访问链接
- 后续还要继续抓取 `mp.weixin.qq.com` 正文

## 当前策略

- 默认 provider 为 `Sogou`
- 搜索阶段直接抓搜狗结果页里的标题、摘要和中转链接
- 抓正文时，不直接请求中转链接；而是在同一个浏览器会话里先打开搜狗搜索页，再打开结果链接，让页面自然跳转到真实 `mp.weixin.qq.com`
- `Brave` 和 `auto` 仍然保留为可选 provider，但不再作为默认路径
- 不要尝试自动绕过验证码；如果页面要求验证，直接要求用户提供真实文章链接或改为单篇直读

## 工作流程

### 步骤1: 确认关键词与数量
1、确认用户关键词  
2、确认需要返回几篇

### 步骤2: 执行搜索命令

```bash
node scripts/search_wechat.js "关键词"
```

## 特殊流程（可选）

1) 限制返回数量

```bash
node scripts/search_wechat.js "关键词" -n 15
```

2) 保存结果到文件

```bash
node scripts/search_wechat.js "关键词" -n 20 -o result.json
```

3) 显式指定 `Sogou` 作为搜索来源

```bash
node scripts/search_wechat.js "关键词" -p sogou
```

4) 尝试自动选择 provider

```bash
node scripts/search_wechat.js "关键词" -p auto
```

5) 显式指定 `Brave` 作为搜索来源

```bash
node scripts/search_wechat.js "关键词" -p brave
```

6) 需要尝试把搜狗中转链接解析成真实链接时

```bash
node scripts/search_wechat.js "关键词" -p sogou -r
```

7) 一键搜索并抓取公众号正文

```bash
node scripts/fetch_wechat_content.js "关键词" -n 3 -o articles.json
```

8) 输出 Markdown 版本

```bash
node scripts/fetch_wechat_content.js "关键词" -n 3 -f md -o articles.md
```

9) 已知真实公众号链接时直接抓正文

```bash
node scripts/fetch_wechat_content.js --url "https://mp.weixin.qq.com/s/..."
```

10) 搜索结果不理想时，显式指定正文抓取阶段使用某个 provider

```bash
node scripts/fetch_wechat_content.js "关键词" -n 3 -p sogou
```

## 参数说明

- `query`：搜索关键词（必填）
- `-n, --num`：返回数量（默认 10，最大 50）
- `-o, --output`：输出 JSON 文件路径（可选）
- `-p, --provider`：搜索来源，支持 `auto`、`brave`、`sogou`
- `-r, --resolve-url`：尝试把搜狗中转链接解析成真实链接（仅对 `sogou` 有意义）
- `fetch_wechat_content.js`：先搜索文章列表，再用本机 Chrome/Edge 在同一会话里打开搜狗结果页和文章页，最后提取正文
- 默认 `sogou` 路径不再依赖单独的中转链接解析请求，因此比过去稳定

## 输出字段（文章对象）

文章标题、文章地址、文章概要、发布时间、来源公众号名称

## 常见问题处理

- 结果为空：尝试更换关键词、更少的特殊字符、或稍后重试
- 搜狗真实 URL 解析失败：优先改用 `fetch_wechat_content.js`，它会在浏览器会话里处理跳转
- 正文抓不到：优先改用 `--url` 直接读取真实 `mp.weixin.qq.com` 链接
- 页面提示登录或违规：直接向用户说明，不要尝试绕过验证或验证码

## 注意事项

- 本工具仅用于学习和研究目的，请勿用于商业用途或大规模爬取。
- 使用本工具时请遵守相关网站的使用条款和规定。
- 过度使用可能导致 IP 被封禁，请谨慎使用。

## Resource Map

### Scripts
- `scripts/fetch_wechat_content.js`
- `scripts/search_wechat.js`

## Source

- Original skill definition: `SKILL.md`
