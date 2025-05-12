# src/debug_rss.py

import json
from .data_ingestion.rss import fetch_rss_entries

if __name__ == "__main__":
    entries = fetch_rss_entries(limit=5)
    print(f"Fetched {len(entries)} entries:")
    print(json.dumps(entries, indent=2))
