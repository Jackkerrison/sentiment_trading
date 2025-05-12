# src/run_rss_pipeline.py

from .data_ingestion.rss import fetch_rss_entries
from .finbert_prototype import analyse_and_signal
import pandas as pd

def main():
    entries = fetch_rss_entries(limit=15)
    rows = []
    for ent in entries:
        text  = f"{ent['title']}  {ent['description']}"
        score, signal = analyse_and_signal(text)
        rows.append({
            "title":  ent["title"][:60] + "…",
            "score":  round(score, 2),
            "signal": signal,
            "link":   ent["link"]
        })

    df = pd.DataFrame(rows, columns=["title","score","signal","link"])
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
