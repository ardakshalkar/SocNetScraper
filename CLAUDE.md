This repo collects public Threads posts about Narxoz University (нархоз, narxoz).

When asked for Threads mentions, use the TypeScript MCP tools (`scrape_narxoz_threads`, then `latest_narxoz_threads`). Do not run Python and do not build a second scraper. Prefer last 7 days (and last 24 hours if any). If login is required, call `login_narxoz_threads`. If MCP is missing, tell the user to run `cd plugins/mcp && npm install && npm run build` then `cd ../claude && npm install`.

Python CLI (`python -m socnetscraper`) is only for cron / Windows Task Scheduler, not for Claude.
