# src/preprocessing/filter_relevance.py

import spacy
from transformers import pipeline

# 1. Load spaCy NER model
_nlp = spacy.load("en_core_web_sm")

# 2. Load zero-shot classifier
_zero_shot = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=-1
)

def mentions_company(text: str, company_names=("Apple", "AAPL")) -> bool:
    """
    Returns True if spaCy NER finds an ORG or PRODUCT matching any of company_names.
    """
    doc = _nlp(text)
    for ent in doc.ents:
        if ent.label_ in ("ORG", "PRODUCT"):
            if ent.text.lower() in {n.lower() for n in company_names}:
                return True
    return False

def zero_shot_relevant(text: str, company="Apple") -> bool:
    """
    Zero-shot classify whether `text` is about `company`.
    Returns True if the probability for the `company` label ≥ 0.6.
    """
    candidate_labels = [company, "Other"]
    out = _zero_shot(text, candidate_labels)
    # out = {'labels':['Apple','Other'], 'scores':[0.72,0.28], ...}
    probs = dict(zip(out["labels"], out["scores"]))
    return probs.get(company, 0) >= 0.60

def is_relevant(text: str) -> bool:
    """
    Composite check: spaCy NER OR zero-shot must pass.
    """
    if mentions_company(text):
        return True
    return zero_shot_relevant(text)
