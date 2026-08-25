import { existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export function scraperRoot(): string {
  const fromEnv = process.env.NARXOZ_SCRAPER_ROOT?.trim();
  if (fromEnv && existsSync(join(fromEnv, "pyproject.toml"))) {
    return resolve(fromEnv);
  }
  const here = dirname(fileURLToPath(import.meta.url));
  const bundled = resolve(here, "..", "..", "..");
  if (existsSync(join(bundled, "pyproject.toml"))) {
    return bundled;
  }
  let dir = process.cwd();
  for (let i = 0; i < 8; i += 1) {
    if (existsSync(join(dir, "pyproject.toml"))) {
      return dir;
    }
    const parent = dirname(dir);
    if (parent === dir) {
      break;
    }
    dir = parent;
  }
  throw new Error(
    "Cannot find SocNetScraper. Set NARXOZ_SCRAPER_ROOT to the repo path."
  );
}

export function postsPath(root: string): string {
  return join(root, "data", "posts.jsonl");
}

