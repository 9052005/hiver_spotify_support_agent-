import json
from pathlib import Path

from sklearn.metrics import accuracy_score, f1_score, classification_report

from src.intent import keyword_baseline
from src.pipeline import run
from .baselines import load_gold

def main():
    rows = load_gold()
    texts = [r["customer_message"] for r in rows]
    y = [r["intent"] for r in rows]

    keyword = [keyword_baseline(x) for x in texts]
    print("\n=== BASELINE: KEYWORDS ===")
    print("Accuracy:", round(accuracy_score(y, keyword), 4))
    print("Macro-F1:", round(f1_score(y, keyword, average="macro", zero_division=0), 4))

    pred = []
    routes = []
    expected_routes = []
    for r in rows:
        result = run(r["customer_message"])
        pred.append(result["intent"])
        routes.append(result["decision"])
        expected_routes.append(r["expected_route"])

    print("\n=== AGENT INTENT ===")
    print("Accuracy:", round(accuracy_score(y, pred), 4))
    print("Macro-F1:", round(f1_score(y, pred, average="macro", zero_division=0), 4))
    print(classification_report(y, pred, zero_division=0))

    if all(expected_routes):
        print("\n=== ROUTING ===")
        print("Accuracy:", round(accuracy_score(expected_routes, routes), 4))
        print("Macro-F1:", round(f1_score(expected_routes, routes, average="macro", zero_division=0), 4))

if __name__ == "__main__":
    main()
