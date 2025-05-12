# src/load_dummy.py
import json
import os
from pathlib import Path

def load_articles():
    # Determine project root (two levels up from this file)
    project_root = Path(__file__).resolve().parent.parent
    data_path    = project_root / "data" / "sample_articles.json"
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)
