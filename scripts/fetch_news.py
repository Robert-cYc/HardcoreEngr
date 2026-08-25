#!/usr/bin/env python3
"""抓取科技新聞 RSS，生成 tech-news.json 供 tech-news.html 顯示。

只用 Python 標準庫，無需安裝依賴：
    python3 scripts/fetch_news.py

輸出：專案根目錄的 tech-news.json
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

FEEDS = [
    {"name": "AI 人工智慧", "url": "https://technews.tw/category/ai/feed/",
     "site": "https://technews.tw/category/ai/"},
    {"name": "半導體", "url": "https://technews.tw/category/semiconductor/feed/",
     "site": "https://technews.tw/category/semiconductor/"},
    {"name": "零組件", "url": "https://technews.tw/category/component/feed/",
     "site": "https://technews.tw/category/component/"},
    {"name": "CCC 追新聞", "url": "https://ccc.technews.tw/feed/",
     "site": "https://ccc.technews.tw/"},
]

MAX_PER_FEED = 12
TIMEOUT = 15
UA = {"User-Agent": "Mozilla/5.0 (compatible; HardcoreEngr-news/1.0)"}
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def fetch_feed(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def clean_html(text):
    text = TAG_RE.sub("", text or "")
    return WS_RE.sub(" ", text).strip()


def parse_date(raw):
    try:
        return parsedate_to_datetime(raw).astimezone().strftime("%Y-%m-%d %H:%M")
    except Exception:
        return (raw or "").strip()


def parse_rss(xml_bytes):
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.iter("item"):
        get = lambda tag: (item.findtext(tag) or "").strip()
        items.append({
            "title": get("title"),
            "link": get("link"),
            "date": parse_date(get("pubDate")),
            "summary": clean_html(get("description"))[:160],
        })
    return items


def main():
    sources = []
    for feed in FEEDS:
        entry = {"name": feed["name"], "site": feed["site"], "items": []}
        try:
            entry["items"] = parse_rss(fetch_feed(feed["url"]))[:MAX_PER_FEED]
        except Exception as e:
            entry["error"] = str(e)
            print(f"[warn] {feed['name']} 抓取失敗: {e}", file=sys.stderr)
        sources.append(entry)

    data = {
        "updated": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M"),
        "sources": sources,
    }
    out = Path(__file__).resolve().parent.parent / "tech-news.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(len(s["items"]) for s in sources)
    print(f"OK: 共 {total} 則新聞 -> {out}")


if __name__ == "__main__":
    main()
