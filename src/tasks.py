import json
import redis
from celery import Celery
from .data_ingestion.rss import fetch_rss_entries
from .finbert_prototype import analyse_and_signal

# Redis DB 2 for storing signals by ticker
redis_client = redis.Redis(host='localhost', port=6379, db=2)

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

@app.task
def fetch_and_store_ticker_signals(ticker: str, limit: int = 10):
    entries = fetch_rss_entries(ticker, limit=limit)
    results = []
    for ent in entries:
        # Combine title+description
        text = f"{ent['title']}  {ent['description']}"
        # 1. Relevance filter
        if not is_relevant(text):
            continue   # skip non-Apple items
        # 2. Sentiment
        score, signal = analyse_and_signal(text)
        results.append({
            "ticker": ticker,
            "title":   ent["title"],
            "score":   round(score, 2),
            "signal":  signal,
            "link":    ent["link"],
        })
    # Persist in Redis under key signals_{ticker}
    redis_client.set(f"signals_{ticker}", json.dumps(results))
    redis_client.expire(f"signals_{ticker}", 600)
    return results

# Schedule it every 5 minutes for AAPL
app.conf.beat_schedule = {
    "ticker-aapl-every-5-minutes": {
        "task": "src.tasks.fetch_and_store_ticker_signals",
        "schedule": 300.0,
        "args": ("AAPL", 10),
    },
}
