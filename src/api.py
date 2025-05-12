# src/api.py

from fastapi import FastAPI
import json
import redis
from collections import Counter

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=2)

@app.get("/signals")
def get_signals(ticker: str = "AAPL"):
    data = redis_client.get(f"signals_{ticker}")
    if not data:
        return []
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return []

@app.get("/summary")
def get_summary(ticker: str = "AAPL"):
    """
    Returns count of each signal and a final aggregated
    recommendation: BUY if ≥60% BUY, SELL if ≥60% SELL, else HOLD.
    """
    raw = get_signals(ticker)
    if not raw:
        return {"total": 0, "positive": 0, "neutral": 0, "negative": 0, "recommendation": "HOLD"}

    # Count BUY / SELL / HOLD
    counts = Counter([item["signal"] for item in raw])
    total = sum(counts.values())
    pos_frac = counts["BUY"] / total
    neg_frac = counts["SELL"] / total

    if pos_frac >= 0.6:
        rec = "BUY"
    elif neg_frac >= 0.6:
        rec = "SELL"
    else:
        rec = "HOLD"

    return {
        "total": total,
        "positive": counts["BUY"],
        "neutral": counts["HOLD"],
        "negative": counts["SELL"],
        "recommendation": rec
    }

@app.get("/refresh")
def refresh(ticker: str = "AAPL", limit: int = 10):
    from .tasks import fetch_and_store_ticker_signals
    fetch_and_store_ticker_signals.delay(ticker, limit)
    return {"message": f"Refreshing signals for {ticker}"}
