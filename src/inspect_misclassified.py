# src/inspect_misclassified.py

import csv
from datasets import load_dataset
from .finbert_prototype import analyzer

# Mapping ground-truth integers → strings
INT2LABEL = {0: "positive", 1: "neutral", 2: "negative"}

def inspect(num_to_save=50, output_path="misclassified.csv"):
    # Load the entire corpus
    dataset = load_dataset(
        "financial_phrasebank",
        "sentences_allagree",
        split="train"
    )

    mis = []
    for example in dataset:
        text = example["sentence"]
        true_int = example["label"]
        true_lbl = INT2LABEL[true_int]

        # Get raw pipeline output
        out = analyzer(text[:512])[0]
        pred_lbl = out["label"].lower()
        score    = out["score"]

        if pred_lbl != true_lbl:
            mis.append([true_lbl, pred_lbl, f"{score:.2f}", text])
        if len(mis) >= num_to_save:
            break

    # Write to CSV for easy viewing
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["true_label","predicted_label","score","sentence"])
        writer.writerows(mis)

    print(f"Saved {len(mis)} misclassified examples to {output_path}")

if __name__ == "__main__":
    inspect()
