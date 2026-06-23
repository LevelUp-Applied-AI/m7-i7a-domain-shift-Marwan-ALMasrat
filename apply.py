"""
Module 7 Week A — Integration Task: Domain-Shift Analysis.

Load a fine-tuned classifier from Hugging Face Hub and apply it to a corpus
of tech / entertainment / digital-culture news articles. The model id is read
from the environment (MODEL_HUB_ID), so the same code runs against your real
model locally and a substitute public model in CI.

The model you trained in Lab 7A is an app-review sentiment classifier
(negative / neutral / positive). The news corpus is prose, not consumer
reviews — the gap between the two is the domain shift you analyze.

Reads label names from model.config.id2label — do NOT hard-code class names.
"""

import os

import numpy as np
import pandas as pd
import torch
from dotenv import load_dotenv  # python-dotenv; provided in requirements.txt
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def load_classifier(model_hub_id: str):
    """
    Load model and tokenizer from Hugging Face Hub.

    Returns (model, tokenizer).
    """
    model     = AutoModelForSequenceClassification.from_pretrained(model_hub_id)
    tokenizer = AutoTokenizer.from_pretrained(model_hub_id)
    return model, tokenizer


def predict(text: str, model, tokenizer):
    """
    Predict label and probability for a single string.

    Read the label name from model.config.id2label — do not hard-code.

    Returns (predicted_label_name, predicted_probability).
    """
    # tokenize with truncation, max_length=128, return_tensors="pt"
    inputs = tokenizer(
        text,
        truncation=True,
        max_length=128,
        return_tensors="pt",
    )

    # forward pass under torch.no_grad()
    with torch.no_grad():
        outputs = model(**inputs)

    # softmax the logits along the last dim
    probs = torch.softmax(outputs.logits, dim=-1)

    # get argmax index and the probability at that index
    idx         = int(probs.argmax(dim=-1).item())
    probability = float(probs[0, idx].item())

    # convert index to label name using model.config.id2label
    label_name = model.config.id2label[idx]

    return label_name, probability


def apply_to_corpus(csv_path: str, model_hub_id: str, output_path: str) -> None:
    """
    Read corpus CSV (columns: article_id, text, category_keyword, source),
    predict for every row using the `text` column as model input,
    write predictions to output_path.

    Output columns: article_id, text_excerpt, predicted_label, predicted_probability.
    text_excerpt is the first 200 characters of the article text.
    """
    # load model and tokenizer once (do not re-load per row)
    model, tokenizer = load_classifier(model_hub_id)
    model.eval()

    # read the CSV with pandas
    df = pd.read_csv(csv_path)

    article_ids   = []
    text_excerpts = []
    pred_labels   = []
    pred_probs    = []

    # iterate over rows, calling predict() on the `text` column
    for _, row in df.iterrows():
        text  = str(row["text"])
        label, prob = predict(text, model, tokenizer)

        article_ids.append(row["article_id"])
        text_excerpts.append(text[:200])          # first 200 characters
        pred_labels.append(label)
        pred_probs.append(prob)

    # build DataFrame with the four output columns
    out_df = pd.DataFrame({
        "article_id":           article_ids,
        "text_excerpt":         text_excerpts,
        "predicted_label":      pred_labels,
        "predicted_probability": pred_probs,
    })

    # write to output_path with index=False
    out_df.to_csv(output_path, index=False)


def main() -> None:
    """Read env vars; orchestrate."""
    load_dotenv()  # loads .env if present

    model_hub_id = os.environ.get("MODEL_HUB_ID")
    if not model_hub_id:
        raise SystemExit(
            "MODEL_HUB_ID is not set. Either set it in your environment or copy "
            ".env.example to .env and fill in your Hugging Face Hub model id."
        )

    corpus_path = os.environ.get("CORPUS_PATH", "data/tech_news_articles.csv")
    output_path = os.environ.get("OUTPUT_PATH", "predictions.csv")

    apply_to_corpus(corpus_path, model_hub_id, output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()