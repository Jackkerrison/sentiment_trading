# src/finbert_prototype.py

import re
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Paths and constants
LOCAL_MODEL_DIR = Path(__file__).resolve().parent.parent / "finetuned-model"
DEFAULT_MODEL    = "yiyanghkust/finbert-tone"

# Globals for lazy loading
_tokenizer = None
_model     = None
_analyzer  = None

def _get_pipeline():
    """
    Lazily load tokenizer, model, and pipeline inside the worker
    to ensure proper CPU-only execution and avoid MPS in pre-fork.
    """
    global _tokenizer, _model, _analyzer
    if _analyzer is None:
        # Choose local fine-tuned if exists, else default
        load_path = LOCAL_MODEL_DIR if LOCAL_MODEL_DIR.exists() else DEFAULT_MODEL

        # Load tokenizer and model (on CPU by default)
        _tokenizer = AutoTokenizer.from_pretrained(load_path)
        _model     = AutoModelForSequenceClassification.from_pretrained(load_path)

        # Create a CPU-only pipeline
        _analyzer = pipeline(
            "sentiment-analysis",
            model=_model,
            tokenizer=_tokenizer,
            device=-1      # CPU
        )
    return _analyzer

def clean_text(text: str) -> str:
    """Basic cleaning of URLs, mentions, non-alphanumeric chars."""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"[^A-Za-z0-9.,!? ]+", "", text)
    return text.strip()

def analyse_and_signal(text: str):
    """
    Perform sentiment analysis on `text`, returning (score, signal).
    Signal is BUY if positive ≥0.70, SELL if negative ≥0.70, else HOLD.
    """
    analyzer = _get_pipeline()
    clean    = clean_text(text)[:512]
    out      = analyzer(clean)[0]

    label = out["label"].lower()
    score = out["score"]

    if label == "positive" and score >= 0.70:
        return score, "BUY"
    if label == "negative" and score >= 0.70:
        return score, "SELL"
    return score, "HOLD"
