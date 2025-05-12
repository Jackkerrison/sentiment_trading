# src/data_ingestion/rss.py

import feedparser

def fetch_rss_entries(ticker: str, limit: int = 10):
    """
    Fetch the latest `limit` entries from Yahoo Finance RSS for a given ticker.
    """
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    feed = feedparser.parse(url)
    entries = []
    for e in feed.entries[:limit]:
        entries.append({
            "title":       e.get("title", ""),
            "link":        e.get("link", ""),
            "description": e.get("description", "")
        })
    return entries
