---
name: scrape-threads-narxoz
description: Scrapes public Threads posts about Narxoz University using the local socnetscraper CLI or MCP tools. Use when the user asks for Threads mentions of нархоз or narxoz, a daily Narxoz social listening run, or to summarize collected Threads posts.
---

# Scrape Threads for Narxoz

Collect public Threads posts that mention **нархоз** or **narxoz**. Prefer the local package in this repo; do not invent a new scraper.

## Run

From the repo root:

```bash
python -m socnetscraper scrape
```

If Threads shows a login wall:

```bash
python -m socnetscraper login
python -m socnetscraper scrape --browser
```

If `THREADS_ACCESS_TOKEN` is set, the official Keyword Search API is used first.

## After a scrape

1. Prefer posts from the last 7 days by default, with a last-24-hours filter.
2. Open or regenerate the HTML dashboard with `python -m socnetscraper view`.
3. Summarize new posts: author, time, permalink, short quote.
4. If last-24h is empty, say so and show last 7 days instead.
5. If `found` is 0, report `data/runs/*.json` errors instead of guessing.

## MCP

If the `narxoz-threads` MCP server is connected, use:

- `scrape_narxoz_threads` to run a collection
- `latest_narxoz_threads` to read saved posts

## Daily job

Default time is 09:00 in `config.json` (`Asia/Almaty`). Change `daily_time` there, then use GitHub Actions, `python -m socnetscraper daily --now`, or `scripts/install-windows-task.ps1`.
