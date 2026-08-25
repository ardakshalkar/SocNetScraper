# Plugins

TypeScript plugins for **Claude Code** and **OpenAI Codex**. Both scrape Threads with **Node.js + Playwright**. Python is not required.

```
plugins/
  mcp/                 TypeScript MCP + scraper source
  claude/              Claude Code plugin
  codex/               Codex plugin
```

Build the bundled server (once, after changing TypeScript):

```bash
cd plugins/mcp
npm install
npx playwright install chromium
npm run build
```

That writes `plugins/claude/server/index.js` and `plugins/codex/server/index.js`. Playwright stays external, so also:

```bash
cd plugins/claude
npm install
```

(same for `plugins/codex`). Set `NARXOZ_SCRAPER_ROOT` if the agent is opened outside this repo. Credentials stay in `.env` (`THREADS_USERNAME` / `THREADS_PASSWORD` or `THREADS_ACCESS_TOKEN`).

## Claude Code

```text
/plugin marketplace add ardakshalkar/SocNetScraper
/plugin install narxoz-threads@narxoz-threads-marketplace
```

Or open this repo: `.mcp.json` already starts `node plugins/claude/server/index.js`.

Then call `login_narxoz_threads` once, then `scrape_narxoz_threads`.

## Codex

Install `plugins/codex`. After copying, run `npm install` there.
