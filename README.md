# SocNetScraper

Daily collector for public [Threads](https://www.threads.com) posts about **Narxoz / нархоз**. Ship the repo as-is, or plug it into Claude.

Default schedule: **09:00 Asia/Almaty**. Change `daily_time` in `config.json`.

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\pip install -e .
.venv\Scripts\python -m playwright install chromium
```

Put Instagram / Threads credentials in `.env` (gitignored; copy from `.env.example`):

```
THREADS_USERNAME=your_instagram_username
THREADS_PASSWORD=your_password
```

Then:

```bash
python -m socnetscraper login
python -m socnetscraper scrape --browser
```

## Scrape once

```bash
python -m socnetscraper scrape
```

Results:

- `data/index.html` — HTML dashboard (defaults to last 24 hours)
- `data/posts.jsonl` — full archive, deduped by post id
- `data/posts.csv` — spreadsheet-friendly snapshot
- `data/runs/` — one JSON file per run

Open the dashboard:

```bash
python -m socnetscraper view
```

The page loads **last 7 days** first. Switch to **Last 24 hours** for the daily slice.


If Threads asks you to log in, fill `.env` and run `python -m socnetscraper login`.

## Run every day

Pick one:

1. **GitHub Actions** — enable the workflow and (optional) add secret `THREADS_ACCESS_TOKEN`. Cron is `0 4 * * *` UTC, which is 09:00 in Almaty.
2. **Windows task** — `powershell -File scripts/install-windows-task.ps1 -Time 09:00`
3. **Keep a process running** — `python -m socnetscraper daily --now`
4. **Linux/macOS cron** — `0 9 * * * cd /path/to/SocNetScraper && .venv/bin/python -m socnetscraper scrape`

## Include in Claude

**Claude Code / Claude Project**

- This repo already has `CLAUDE.md` and `.claude/skills/scrape-threads-narxoz/SKILL.md`.
- Copy `skills/scrape-threads-narxoz/` into another project's `.claude/skills/` folder if you want the same behavior elsewhere.

**Claude Desktop MCP**

Merge `integrations/claude-desktop.json` into Claude Desktop config (`claude_desktop_config.json`). Set `cwd` to this repo and use the venv Python if you have one:

```json
{
  "mcpServers": {
    "narxoz-threads": {
      "command": "C:/path/to/SocNetScraper/.venv/Scripts/python.exe",
      "args": ["-m", "socnetscraper.mcp_server"],
      "cwd": "C:/path/to/SocNetScraper"
    }
  }
}
```

Tools Claude gets:

- `scrape_narxoz_threads`
- `latest_narxoz_threads`

## Official API vs browser

If `THREADS_ACCESS_TOKEN` is present, keyword search uses [Meta's Threads Keyword Search API](https://developers.facebook.com/docs/threads/keyword-search/). That is the most stable option to ship. Without a token, the scraper opens Threads search in Chromium and saves public posts.

Needed API permissions: `threads_basic`, `threads_keyword_search`.
