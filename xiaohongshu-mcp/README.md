# xiaohongshu-mcp

Automate Xiaohongshu (RedNote) content operations using a Python client for the xiaohongshu-mcp server. Use for: searching notes, reading note details and comments, checking feeds, and publishing content.

## Portable Entry Point

- Start here if you are using this repository from a non-Codex agent.
- The original Codex-oriented source remains in `SKILL.md` for reference.
- Run bundled scripts relative to this folder, for example `./xiaohongshu-mcp/scripts/...` from the repo root.

## Adapted Instructions

# Xiaohongshu MCP Skill

This skill talks to a locally running `xiaohongshu-mcp` service through `scripts/xhs_client.py`.

## Setup

1. Download the proper binaries from:
   `https://github.com/xpzouying/xiaohongshu-mcp/releases`
2. Run the login helper and scan the QR code with the Xiaohongshu app.
3. Start the MCP server locally. Default endpoint:
   `http://localhost:18060`

## Commands

```bash
python scripts/xhs_client.py status
python scripts/xhs_client.py search "咖啡"
python scripts/xhs_client.py detail "<feed_id>" "<xsec_token>"
python scripts/xhs_client.py feeds
python scripts/xhs_client.py publish "标题" "正文" "url1,url2"
```

## Notes

- `detail` can optionally pull comments with `--comments`
- the local MCP service must stay logged in
- if the service is unreachable, the script exits with an error

## Resource Map

### Scripts
- `scripts/xhs_client.py`

## Source

- Original skill definition: `SKILL.md`
