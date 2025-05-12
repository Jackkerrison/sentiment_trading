# src/run_pipeline.py
from .load_dummy import load_articles
from .finbert_prototype import analyse_and_signal
import pandas as pd

def main():
    articles = load_articles()
    rows = []
    for art in articles:
        score, signal = analyse_and_signal(art["text"])
        rows.append({
            "ticker": art["ticker"],
            "text":   art["text"],
            "score":  round(score, 2),
            "signal": signal
        })
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
