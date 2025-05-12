# src/run_ticker_pipeline.py

import argparse
import pandas as pd
from .data_ingestion.rss import fetch_rss_entries
from .finbert_prototype import analyse_and_signal

def main():
    parser = argparse.ArgumentParser("Run sentiment pipeline for one stock ticker")
    parser.add_argument("ticker", help="e.g. AAPL")
    parser.add_argument("--limit", type=int, default=10, help="How many news items")
    args = parser.parse_args()

    entries = fetch_rss_entries(args.ticker, limit=args.limit)
    rows = []
    for ent in entries:
        text  = f"{ent['title']}  {ent['description']}"
        score, signal = analyse_and_signal(text)
        rows.append({
            "ticker": args.ticker,
            "title":   ent["title"],
            "score":   round(score, 2),
            "signal":  signal,
            "link":    ent["link"],
        })

    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
