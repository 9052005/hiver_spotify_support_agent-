import json
from collections import Counter
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

from src.intent import keyword_baseline

def load_gold():
    path = Path("artifacts/golden_set.jsonl")
    if not path.exists():
        raise FileNotFoundError("Create artifacts/golden_set.jsonl by manually labeling the template.")
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def main():
    rows = load_gold()
    texts = [r["customer_message"] for r in rows]
    y = [r["intent"] for r in rows]

    majority = Counter(y).most_common(1)[0][0]
    majority_pred = [majority] * len(y)

    keyword_pred = [keyword_baseline(x) for x in texts]

    print("=== Majority baseline ===")
    print("Accuracy:", accuracy_score(y, majority_pred))
    print("Macro-F1:", f1_score(y, majority_pred, average="macro", zero_division=0))

    print("=== Keyword baseline ===")
    print("Accuracy:", accuracy_score(y, keyword_pred))
    print("Macro-F1:", f1_score(y, keyword_pred, average="macro", zero_division=0))

if __name__ == "__main__":
    main()
