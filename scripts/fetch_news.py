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
    {"name": "自由 3C 科技", "url": "https://3c.ltn.com.tw/",
     "site": "https://3c.ltn.com.tw/", "type": "html"},
    {"name": "AI 人工智慧", "url": "https://technews.tw/category/ai/feed/",
     "site": "https://technews.tw/category/ai/", "type": "rss"},
    {"name": "半導體", "url": "https://technews.tw/category/semiconductor/feed/",
     "site": "https://technews.tw/category/semiconductor/", "type": "rss"},
    {"name": "零組件", "url": "https://technews.tw/category/component/feed/",
     "site": "https://technews.tw/category/component/", "type": "rss"},
    {"name": "CCC 追新聞", "url": "https://ccc.technews.tw/feed/",
     "site": "https://ccc.technews.tw/", "type": "rss"},
]

MAX_PER_FEED = 12
TIMEOUT = 15
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
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

def parse_html_ltn_3c(html_bytes):
    html = html_bytes.decode('utf-8', errors='ignore')
    items = []
    blocks = re.findall(r'<div class="box boxnews">.*?</div>', html, re.DOTALL)
    for block in blocks:
        match_tit = re.search(r'<a class="tit" href="([^"]+)"[^>]*><h3[^>]*>(.*?)</h3>', block)
        match_p = re.search(r'<p>(.*?)</p>', block, re.DOTALL)
        match_date = re.search(r'<span>(.*?)</span>', block, re.DOTALL)
        if match_tit:
            link = match_tit.group(1).strip()
            if not link.startswith('http'):
                link = 'https://3c.ltn.com.tw/' + link
            items.append({
                "title": clean_html(match_tit.group(2)),
                "link": link,
                "date": clean_html(match_date.group(1)) if match_date else "",
                "summary": clean_html(match_p.group(1))[:160] if match_p else "",
            })
    return items

def main():
    sources = []
    for feed in FEEDS:
        entry = {"name": feed["name"], "site": feed["site"], "items": []}
        try:
            raw_bytes = fetch_feed(feed["url"])
            if feed.get("type") == "html":
                entry["items"] = parse_html_ltn_3c(raw_bytes)[:MAX_PER_FEED]
            else:
                entry["items"] = parse_rss(raw_bytes)[:MAX_PER_FEED]
        except Exception as e:
            entry["error"] = str(e)
            print(f"[warn] {feed['name']} 抓取失敗: {e}", file=sys.stderr)
        sources.append(entry)

    data = {
        "updated": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M"),
        "sources": sources,
    }
    total = sum(len(s["items"]) for s in sources)
    out = Path(__file__).resolve().parent.parent / "tech-news.json"
    # 全部來源失敗時不覆蓋舊資料，避免把線上正常內容換成一頁錯誤
    if total == 0 and out.exists():
        print("[error] 所有來源皆抓取失敗，保留現有的 tech-news.json", file=sys.stderr)
        sys.exit(1)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: 共 {total} 則新聞 -> {out}")


if __name__ == "__main__":
    main()
