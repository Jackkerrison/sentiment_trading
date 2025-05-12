# src/fine_tune.py

import os
from datasets import load_dataset, DatasetDict
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)

MODEL_NAME = "yiyanghkust/finbert-tone"
OUTPUT_DIR = "finetuned-model"


def preprocess(example, tokenizer):
    tokens = tokenizer(
        example["sentence"],
        truncation=True,
        max_length=128
    )
    tokens["label"] = example["label"]
    return tokens


def main():
    # 1. Load dataset
    raw = load_dataset(
        "financial_phrasebank",
        "sentences_allagree",
        split="train"
    )

    # 2. Split into train/validation (80/20)
    split_ds = raw.train_test_split(test_size=0.2, seed=42)
    ds = DatasetDict({
        "train": split_ds["train"],
        "validation": split_ds["test"]
    })

    # 3. Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=3
    )

    # 4. Preprocess datasets
    ds = ds.map(
        lambda ex: preprocess(ex, tokenizer),
        batched=True,
        remove_columns=["sentence"]
    )

    # 5. Data collator for dynamic padding
    collator = DataCollatorWithPadding(tokenizer)

    # 6. Training arguments (omit unsupported evaluation params)
    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=1,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        learning_rate=2e-5,
        weight_decay=0.01,
        logging_steps=50,
        logging_dir=f"{OUTPUT_DIR}/logs"
    )

    # 7. Initialize Trainer
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=ds["train"],
        eval_dataset=ds["validation"],
        tokenizer=tokenizer,
        data_collator=collator
    )

    # 8. Fine-tune the model
    trainer.train()

    # 9. Evaluate after training
    eval_results = trainer.evaluate()
    print("Evaluation results after fine-tuning:", eval_results)

    # 10. Save the fine-tuned model
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    trainer.save_model(OUTPUT_DIR)
    print(f"Model saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
