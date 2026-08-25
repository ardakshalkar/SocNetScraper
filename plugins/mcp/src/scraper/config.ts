import { existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { scraperRoot } from "../repo.js";

export type AppConfig = {
  keywords: string[];
  hashtags: string[];
  timezone: string;
  daily_time: string;
  lookback_hours: number;
  week_hours: number;
  max_scrolls: number;
  max_posts_per_query: number;
  headless: boolean;
  search_filters: string[];
};

const DEFAULTS: AppConfig = {
  keywords: ["нархоз", "narxoz"],
  hashtags: ["narxoz", "нархоз"],
  timezone: "Asia/Almaty",
  daily_time: "09:00",
  lookback_hours: 24,
  week_hours: 168,
  max_scrolls: 10,
  max_posts_per_query: 80,
  headless: true,
  search_filters: ["recent", "default"],
};

export function loadDotEnv(root: string): void {
  const file = join(root, ".env");
  if (!existsSync(file)) {
    return;
  }
  for (const raw of readFileSync(file, "utf8").split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) {
      continue;
    }
    const idx = line.indexOf("=");
    if (idx < 1) {
      continue;
    }
    const key = line.slice(0, idx).trim();
    let value = line.slice(idx + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    if (!(key in process.env)) {
      process.env[key] = value;
    }
  }
}

export function paths(root = scraperRoot()) {
  const data = join(root, "data");
  mkdirSync(data, { recursive: true });
  mkdirSync(join(root, "logs"), { recursive: true });
  mkdirSync(join(data, "runs"), { recursive: true });
  return {
    root,
    data,
    config: join(root, "config.json"),
    postsJsonl: join(data, "posts.jsonl"),
    postsCsv: join(data, "posts.csv"),
    storageState: join(data, "storage_state.json"),
    browserProfile: join(data, "browser_profile"),
    runs: join(data, "runs"),
  };
}

export function loadConfig(root = scraperRoot()): AppConfig {
  loadDotEnv(root);
  const cfg = { ...DEFAULTS };
  const file = paths(root).config;
  if (existsSync(file)) {
    Object.assign(cfg, JSON.parse(readFileSync(file, "utf8")) as Partial<AppConfig>);
  }
  return cfg;
}

export function searchQueries(cfg: AppConfig): string[] {
  const queries: string[] = [];
  const seen = new Set<string>();
  for (const raw of [...cfg.keywords, ...cfg.hashtags.map((tag) => `#${tag.replace(/^#/, "")}`)]) {
    const query = String(raw).trim();
    const key = query.toLowerCase();
    if (query && !seen.has(key)) {
      seen.add(key);
      queries.push(query);
    }
  }
  return queries;
}

export function apiToken(): string | undefined {
  return process.env.THREADS_ACCESS_TOKEN?.trim() || undefined;
}

export function threadsCredentials(): { username: string; password: string } | undefined {
  const username = process.env.THREADS_USERNAME?.trim() || "";
  const password = process.env.THREADS_PASSWORD?.trim() || "";
  if (username && password) {
    return { username, password };
  }
  return undefined;
}
