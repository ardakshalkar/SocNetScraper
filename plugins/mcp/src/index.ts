import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { recentPosts } from "./posts.js";
import { postsPath, scraperRoot } from "./repo.js";
import { loadConfig } from "./scraper/config.js";
import { saveLoginSession } from "./scraper/browser.js";
import { scrapeOnce } from "./scraper/run.js";

const server = new McpServer({
  name: "narxoz-threads",
  version: "0.2.0",
});

server.tool(
  "scrape_narxoz_threads",
  "Scrape public Threads posts about Narxoz / нархоз using the TypeScript engine (no Python).",
  { browser: z.boolean().optional().describe("Skip the official API and use the browser session") },
  async ({ browser }) => {
    const root = scraperRoot();
    const summary = await scrapeOnce(root, Boolean(browser));
    return { content: [{ type: "text" as const, text: JSON.stringify(summary, null, 2) }] };
  }
);

server.tool(
  "login_narxoz_threads",
  "Open a browser and save a Threads/Instagram login session from .env credentials.",
  {},
  async () => {
    const root = scraperRoot();
    loadConfig(root);
    const path = await saveLoginSession(root);
    return { content: [{ type: "text" as const, text: `Saved session to ${path}` }] };
  }
);

server.tool(
  "latest_narxoz_threads",
  "Return saved Threads posts. hours=168 is last 7 days; hours=0 is the full archive.",
  {
    limit: z.number().int().min(1).max(100).optional(),
    hours: z.number().int().min(0).max(8760).optional(),
  },
  async ({ limit, hours }) => {
    const posts = recentPosts(scraperRoot(), hours ?? 168, limit ?? 25);
    return { content: [{ type: "text" as const, text: JSON.stringify(posts, null, 2) }] };
  }
);

server.tool(
  "narxoz_threads_data_path",
  "Return the path to the JSONL archive of collected Threads posts.",
  {},
  async () => {
    return { content: [{ type: "text" as const, text: postsPath(scraperRoot()) }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
