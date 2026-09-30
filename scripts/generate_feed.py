#!/usr/bin/env python3
"""生成本站 RSS 2.0 Feed (feed.xml)。

用法：
    python3 scripts/generate_feed.py

輸出：專案根目錄的 feed.xml
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEARCH_INDEX = ROOT / "search-index.json"
OUTPUT = ROOT / "feed.xml"

BASE_URL = "https://ai-hardcore-engineer.com"
CHANNEL_TITLE = '"AI" 硬核工程師'
CHANNEL_DESC = "專注於前端開發、後端技術、Git 與 AI 開發的技術博客。分享實用的指令教學與開發心得。"
CHANNEL_LANG = "zh-TW"


def escape_xml(text: str) -> str:
    """Escape XML special characters."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
    )


def get_lastmod_from_html(url: str) -> str:
    """Try to extract date from the article HTML file."""
    html_path = ROOT / url
    if not html_path.exists():
        return datetime.now(timezone.utc).strftime("%a, %d %b %Y 00:00:00 +0000")
    content = html_path.read_text(encoding="utf-8", errors="replace")
    # Look for <lastmod>YYYY-MM-DD</lastmod> or <span>YYYY-MM-DD</span>
    m = re.search(r'<span>(\d{4}-\d{2}-\d{2})</span>', content)
    if m:
        try:
            dt = datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return dt.strftime("%a, %d %b %Y 00:00:00 +0000")
        except ValueError:
            pass
    return datetime.now(timezone.utc).strftime("%a, %d %b %Y 00:00:00 +0000")


def main():
    if not SEARCH_INDEX.exists():
        print(f"[error] {SEARCH_INDEX} not found", flush=True)
        raise SystemExit(1)

    articles = json.loads(SEARCH_INDEX.read_text(encoding="utf-8"))

    now_rfc822 = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

    items_xml = ""
    for art in articles:
        title = art.get("title", "（無標題）")
        url = art.get("url", "")
        excerpt = art.get("excerpt", "")
        tags = art.get("tags", [])
        pub_date = get_lastmod_from_html(url)
        link = f"{BASE_URL}/{url}"

        categories = "".join(f"    <category>{escape_xml(t)}</category>\n" for t in tags)

        items_xml += f"""  <item>
    <title>{escape_xml(title)}</title>
    <link>{link}</link>
    <guid isPermaLink="true">{link}</guid>
    <description>{escape_xml(excerpt)}</description>
    <pubDate>{pub_date}</pubDate>
{categories}  </item>
"""

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape_xml(CHANNEL_TITLE)}</title>
    <link>{BASE_URL}/</link>
    <description>{escape_xml(CHANNEL_DESC)}</description>
    <language>{CHANNEL_LANG}</language>
    <lastBuildDate>{now_rfc822}</lastBuildDate>
    <atom:link href="{BASE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
    <image>
      <url>{BASE_URL}/og-image.png</url>
      <title>{escape_xml(CHANNEL_TITLE)}</title>
      <link>{BASE_URL}/</link>
    </image>
{items_xml}  </channel>
</rss>
"""

    OUTPUT.write_text(feed, encoding="utf-8")
    sys.stdout.buffer.write(f"OK: {len(articles)} articles -> {OUTPUT}\n".encode("utf-8"))


if __name__ == "__main__":
    main()
