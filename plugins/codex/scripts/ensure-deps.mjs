import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const plugin = join(dirname(fileURLToPath(import.meta.url)), "..");
const playwright = join(plugin, "node_modules", "playwright", "package.json");
if (existsSync(playwright)) {
  process.exit(0);
}
const result = spawnSync("npm", ["install", "--omit=dev"], {
  cwd: plugin,
  stdio: "inherit",
  shell: true,
});
process.exit(result.status ?? 1);
