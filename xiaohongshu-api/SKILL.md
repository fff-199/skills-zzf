---
name: xiaohongshu-api
description: 小红书数据 API。通过 TikHub 获取公开帖子、搜索结果和热门内容。
metadata:
  version: 1.0.0
---

# Xiaohongshu API

Use this skill when you want Xiaohongshu public data without running a local browser session.

## Capabilities

- fetch post details
- search posts by keyword
- fetch trending posts

## Requirements

- a TikHub API key from `https://api.tikhub.io`

## Commands

```bash
python scripts/xiaohongshu.py --post-id <帖子ID> --api-key <key>
python scripts/xiaohongshu.py --search <关键词> --api-key <key>
python scripts/xiaohongshu.py --trending --api-key <key>
```

## Notes

- only public data is available
- respect TikHub and Xiaohongshu terms
