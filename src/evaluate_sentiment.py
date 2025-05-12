# src/evaluate_sentiment.py

from datasets import load_dataset
from sklearn.metrics import classification_report
from .finbert_prototype import analyzer    # the HF pipeline you already loaded

def map_label_to_int(label: str) -> int:
    """Convert string labels to integers."""
    return {"positive": 0, "neutral": 1, "negative": 2}[label]

if __name__ == "__main__":
    # 1. Load the full Financial PhraseBank (all-agree subset)
    dataset = load_dataset(
        "financial_phrasebank",
        "sentences_allagree",
        split="train"
    )

    y_true = []
    y_pred = []

    for example in dataset:
        text = example["sentence"]
        # ground-truth is already an int (0,1,2)
        y_true.append(example["label"])

        # get model’s raw label
        out = analyzer(text[:512])[0]
        label_str = out["label"].lower()
        y_pred.append(map_label_to_int(label_str))

    # 2. Print classification metrics
    report = classification_report(
        y_true, y_pred,
        target_names=["positive", "neutral", "negative"]
    )
    print("FinBERT Evaluation on Financial PhraseBank (all-agree subset)\n")
    print(report)