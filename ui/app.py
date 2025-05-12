# ui/app.py

import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Stock Sentiment Signals", layout="wide")
st.title("📈 Stock Sentiment Signals")

ticker = st.sidebar.text_input("Ticker symbol", value="AAPL").upper()
limit  = st.sidebar.slider("Number of headlines", 5, 20, 10, 5)

if st.sidebar.button("🚀 Refresh Now"):
    requests.get(f"http://127.0.0.1:8000/refresh?ticker={ticker}&limit={limit}")

# 1. Fetch summary
summary = requests.get(f"http://127.0.0.1:8000/summary?ticker={ticker}").json()
if summary["total"] == 0:
    st.warning("No data yet. Please wait or press 'Refresh Now'.")
else:
    # Display summary
    st.markdown(
        f"### Overall Recommendation for **{ticker}**: {summary['recommendation']}\n"
        f"- BUY signals: {summary['positive']}  \n"
        f"- HOLD signals: {summary['neutral']}  \n"
        f"- SELL signals: {summary['negative']}  \n"
        f"- Total items: {summary['total']}"
    )

    # 2. Fetch detail table
    resp = requests.get(f"http://127.0.0.1:8000/signals?ticker={ticker}")
    df = pd.DataFrame(resp.json())[:limit]
    df = df.rename(columns={
        "title":"Headline", "score":"Score",
        "signal":"Signal", "link":"URL"
    })
    st.dataframe(df, use_container_width=True)
