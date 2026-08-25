---
name: scrape-threads-narxoz
description: Scrapes public Threads posts about Narxoz University with the TypeScript plugin (no Python). Use when the user asks for Threads mentions of нархоз or narxoz.
---

# Scrape Threads for Narxoz

Use this plugin's MCP tools. Do **not** call Python.

## Tools

- `scrape_narxoz_threads` — collect posts (`browser: true` skips the official API)
- `login_narxoz_threads` — save a Threads session from `.env` (`THREADS_USERNAME` / `THREADS_PASSWORD`)
- `latest_narxoz_threads` — read saved posts (`hours: 168` or `24`)
- `narxoz_threads_data_path` — path to `data/posts.jsonl`

## Setup on this machine

1. Node 18+
2. In `plugins/claude` or `plugins/mcp`: `npm install` (installs Playwright Chromium)
3. `.env` in the SocNetScraper repo with Threads login, or `THREADS_ACCESS_TOKEN`
4. If the open folder is not this repo, set `NARXOZ_SCRAPER_ROOT`

## After a scrape

Prefer last 7 days. Show replies with their parent question. Ignore anesthesia false positives (наркоз written as нархоз).
