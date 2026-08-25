from __future__ import annotations

import json
import webbrowser
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from socnetscraper.config import DATA_DIR, INDEX_HTML, load_config
from socnetscraper.store import load_existing, lookback_posts

TEMPLATE = r"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Narxoz · Threads</title>
  <style>
    :root {
      --red: #D50032;
      --dark: #01080A;
      --ink: #1a1a1a;
      --muted: #667085;
      --line: #e8eaed;
      --bg: #F5F5F6;
      --card: #fff;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", system-ui, sans-serif;
      background: var(--bg);
      color: var(--ink);
    }
    header {
      background: var(--dark);
      color: #fff;
      padding: 28px 20px 22px;
    }
    .wrap { max-width: 760px; margin: 0 auto; }
    .kicker {
      color: var(--red);
      font-size: 12px;
      letter-spacing: .12em;
      text-transform: uppercase;
      font-weight: 700;
    }
    h1 { margin: 8px 0 6px; font-size: 28px; font-weight: 650; }
    .sub { color: #c9cdd3; font-size: 14px; }
    .toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      margin-top: -18px;
      padding: 0 20px 18px;
    }
    .toolbar .wrap {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      width: 100%;
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 12px;
      box-shadow: 0 8px 24px rgba(1,8,10,.06);
    }
    .seg { display: flex; background: var(--bg); border-radius: 999px; padding: 4px; }
    .seg button {
      border: 0;
      background: transparent;
      padding: 8px 14px;
      border-radius: 999px;
      cursor: pointer;
      font: inherit;
      color: var(--muted);
    }
    .seg button.active { background: var(--red); color: #fff; }
    input[type="search"] {
      flex: 1;
      min-width: 180px;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 10px 14px;
      font: inherit;
    }
    .stats { color: var(--muted); font-size: 13px; padding: 4px 6px; }
    main { padding: 0 20px 40px; }
    .card, .conversation {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 16px;
      margin: 12px 0;
    }
    .card { padding: 16px 18px; }
    .conversation { overflow: hidden; }
    .conversation .card {
      border: 0;
      border-radius: 0;
      margin: 0;
    }
    .conversation .card.answer {
      border-top: 1px solid var(--line);
      background: #fafafa;
    }
    .label {
      font-size: 11px;
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 8px;
    }
    .card.answer .label { color: var(--red); }
    .meta {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: baseline;
    }
    .user { font-weight: 700; }
    .user a { color: inherit; text-decoration: none; }
    .user a:hover { color: var(--red); }
    .when { color: var(--muted); font-size: 13px; white-space: nowrap; }
    .text {
      white-space: pre-wrap;
      line-height: 1.45;
      margin: 10px 0 12px;
    }
    .media {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      margin: 0 0 12px;
    }
    .media img {
      max-height: 280px;
      max-width: 100%;
      border-radius: 12px;
      border: 1px solid var(--line);
    }
    .foot {
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      color: var(--muted);
      font-size: 13px;
    }
    .foot a { color: #2b6cb0; }
    .empty {
      text-align: center;
      padding: 48px 16px;
      color: var(--muted);
    }
    .empty strong { color: var(--ink); display: block; margin-bottom: 6px; font-size: 18px; }
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <div class="kicker">SocNetScraper</div>
      <h1>Threads · Нархоз</h1>
      <div class="sub" id="generated"></div>
    </div>
  </header>
  <div class="toolbar">
    <div class="wrap">
      <div class="seg">
        <button id="btn24" type="button">Last 24 hours</button>
        <button id="btn7" class="active" type="button">Last 7 days</button>
      </div>
      <input id="q" type="search" placeholder="Search text or @username">
      <div class="stats" id="stats"></div>
    </div>
  </div>
  <main class="wrap" id="feed"></main>
  <script>
    const DATA = __PAYLOAD__;
    const hours24 = DATA.lookback_hours || 24;
    const hours7 = DATA.week_hours || 168;
    let range = "7d";
    const feed = document.getElementById("feed");
    const stats = document.getElementById("stats");
    const search = document.getElementById("q");
    const btn24 = document.getElementById("btn24");
    const btn7 = document.getElementById("btn7");

    document.getElementById("generated").textContent =
      "Updated " + formatWhen(DATA.generated_at) + " · " + DATA.timezone;

    function parseDate(value) {
      if (!value) return null;
      const dt = new Date(value);
      return Number.isNaN(dt.getTime()) ? null : dt;
    }
    function postDate(post) {
      return parseDate(post.published_at);
    }
    function inLastHours(post, hours) {
      const dt = postDate(post);
      return dt ? (Date.now() - dt.getTime()) <= hours * 3600 * 1000 : false;
    }
    function formatWhen(value) {
      const dt = parseDate(value);
      if (!dt) return "";
      return dt.toLocaleString("ru-KZ", { dateStyle: "medium", timeStyle: "short" });
    }
    function escapeHtml(text) {
      return String(text || "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
    }
    function mediaHtml(post) {
      const images = post.images || [];
      if (!images.length) return "";
      return `<div class="media">${images.map((src) => `<img src="${escapeHtml(src)}" alt="">`).join("")}</div>`;
    }
    function postCard(post, extraClass, label) {
      const tag = label ? `<div class="label">${escapeHtml(label)}</div>` : "";
      const name = post.username ? "@" + post.username : "unknown";
      return `
        <article class="card ${extraClass || ""}">
          ${tag}
          <div class="meta">
            <div class="user"><a href="${escapeHtml(post.url || "")}" target="_blank" rel="noopener">${escapeHtml(name)}</a></div>
            <div class="when">${escapeHtml(formatWhen(post.published_at))}</div>
          </div>
          <div class="text">${escapeHtml(post.text)}</div>
          ${mediaHtml(post)}
          <div class="foot">
            <span>♥ ${post.like_count ?? 0}</span>
            <span>💬 ${post.reply_count ?? 0}</span>
            <span>🔁 ${post.repost_count ?? 0}</span>
            <a href="${escapeHtml(post.url || "")}" target="_blank" rel="noopener">Open in Threads</a>
          </div>
        </article>
      `;
    }
    function groupFeed(posts) {
      const used = new Set();
      const blocks = [];
      for (const post of posts) {
        const parent = post.parent;
        if (!parent || !(parent.text || parent.username)) continue;
        if (used.has(post.code || post.url)) continue;
        const replies = posts.filter((item) => {
          const p = item.parent || {};
          return (p.code && p.code === parent.code) || (p.text && p.text === parent.text && p.username === parent.username);
        });
        blocks.push({ parent, replies });
        used.add(post.code || post.url);
        used.add(parent.code || parent.url);
        replies.forEach((item) => used.add(item.code || item.url));
      }
      for (const post of posts) {
        if (!used.has(post.code || post.url)) blocks.push({ post });
      }
      return blocks;
    }
    function render() {
      const needle = search.value.trim().toLowerCase();
      const hours = range === "24h" ? hours24 : hours7;
      let posts = DATA.posts.filter((post) => inLastHours(post, hours));
      if (needle) {
        posts = posts.filter((post) => (`@${post.username} ${post.text} ${post.parent ? post.parent.text : ""}`).toLowerCase().includes(needle));
      }
      stats.textContent = posts.length + (range === "24h" ? " in last 24 hours" : " in last 7 days");
      if (!posts.length) {
        feed.innerHTML = `<div class="empty"><strong>No Threads posts in this range</strong>Try the other tab, or run a new scrape.</div>`;
        return;
      }
      feed.innerHTML = groupFeed(posts).map((block) => {
        if (block.replies) {
          return `<div class="conversation">
            ${postCard(block.parent, "question", "Вопрос")}
            ${block.replies.map((reply) => postCard(reply, "answer", "Ответ")).join("")}
          </div>`;
        }
        return postCard(block.post);
      }).join("");
    }
    btn24.onclick = () => { range = "24h"; btn24.classList.add("active"); btn7.classList.remove("active"); render(); };
    btn7.onclick = () => { range = "7d"; btn7.classList.add("active"); btn24.classList.remove("active"); render(); };
    search.oninput = render;
    render();
  </script>
</body>
</html>
"""


def _view_post(post: dict[str, Any]) -> dict[str, Any]:
    parent = post.get("parent") if isinstance(post.get("parent"), dict) else None
    return {
        "code": post.get("code") or "",
        "username": post.get("username") or "",
        "verified": bool(post.get("verified")),
        "avatar": post.get("avatar") or "",
        "images": post.get("images") or [],
        "text": post.get("text") or "",
        "url": post.get("url") or "",
        "published_at": post.get("published_at"),
        "scraped_at": post.get("scraped_at"),
        "like_count": post.get("like_count") or 0,
        "reply_count": post.get("reply_count") or 0,
        "repost_count": post.get("repost_count") or 0,
        "is_reply": bool(post.get("is_reply")),
        "parent": {
            "code": parent.get("code") or "",
            "username": parent.get("username") or "",
            "text": parent.get("text") or "",
            "url": parent.get("url") or "",
            "avatar": parent.get("avatar") or "",
            "images": parent.get("images") or [],
            "published_at": parent.get("published_at"),
            "verified": bool(parent.get("verified")),
            "like_count": parent.get("like_count") or 0,
            "reply_count": parent.get("reply_count") or 0,
            "repost_count": parent.get("repost_count") or 0,
        } if parent and (parent.get("text") or parent.get("username")) else None,
    }


def dashboard_payload(hours: int | None = None) -> dict[str, Any]:
    cfg = load_config()
    lookback = int(hours if hours is not None else cfg.get("lookback_hours") or 24)
    week_hours = int(cfg.get("week_hours") or 168)
    posts = list(load_existing().values())
    posts.sort(key=lambda item: str(item.get("published_at") or item.get("scraped_at") or ""), reverse=True)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "timezone": cfg.get("timezone") or "Asia/Almaty",
        "lookback_hours": lookback,
        "week_hours": week_hours,
        "recent_count": len(lookback_posts(posts, lookback)),
        "week_count": len(lookback_posts(posts, week_hours)),
        "total_count": len(posts),
        "posts": [_view_post(post) for post in posts],
    }


def render_html(hours: int | None = None) -> str:
    payload = json.dumps(dashboard_payload(hours), ensure_ascii=False)
    payload = payload.replace("<", "\\u003c")
    return TEMPLATE.replace("__PAYLOAD__", payload)


def write_html(hours: int | None = None) -> Path:
    INDEX_HTML.parent.mkdir(parents=True, exist_ok=True)
    INDEX_HTML.write_text(render_html(hours), encoding="utf-8")
    return INDEX_HTML


def serve_dashboard(port: int = 8765, open_browser: bool = True) -> None:
    write_html()

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=str(DATA_DIR), **kwargs)

        def do_GET(self) -> None:  # noqa: N802
            if self.path in ("/", "/index.html"):
                body = render_html().encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            super().do_GET()

        def log_message(self, format: str, *args: Any) -> None:
            print(format % args)

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"Dashboard: {url}")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped dashboard")
