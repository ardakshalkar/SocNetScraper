---
name: scrape-threads-narxoz
description: Scrapes public Threads posts about Narxoz University with the TypeScript MCP tools (no Python). Use when the user asks for Threads mentions of нархоз or narxoz, a daily Narxoz social listening run, or to summarize collected Threads posts.
---

# Scrape Threads for Narxoz

Collect public Threads posts that mention **нархоз** or **narxoz**. Use this repo's MCP tools. Do **not** call Python. Do not invent a second scraper.

## Tools

- `scrape_narxoz_threads` — collect posts (`browser: true` skips the official API)
- `login_narxoz_threads` — save a Threads session from `.env` (`THREADS_USERNAME` / `THREADS_PASSWORD`)
- `latest_narxoz_threads` — read saved posts (`hours: 168` or `24`)
- `narxoz_threads_data_path` — path to `data/posts.jsonl`

If MCP is not connected, tell the user to install Node 18+, then:

```bash
cd plugins/mcp && npm install && npm run build
cd ../claude && npm install
```

## After a scrape

1. Prefer last 7 days; mention last 24 hours if any posts exist.
2. Summarize: author, time, permalink, short quote.
3. Replies should be shown with their parent question.
4. Ignore anesthesia false positives (наркоз written as нархоз).
5. If `found` is 0, report scrape errors instead of guessing.

## Daily job

Default time is 09:00 in `config.json` (`Asia/Almaty`). That path is the Python/Windows task, not Claude.
