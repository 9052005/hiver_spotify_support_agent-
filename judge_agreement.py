import os
import pandas as pd
from scipy.stats import spearmanr

# human_judge.csv columns:
# id,human_overall,llm_overall
path = "artifacts/human_judge.csv"

if not os.path.exists(path):
    raise SystemExit(
        "Create artifacts/human_judge.csv after manually rating generated replies."
    )

df = pd.read_csv(path)
rho, p = spearmanr(df["human_overall"], df["llm_overall"])

within_one = (
    (df["human_overall"] - df["llm_overall"]).abs() <= 1
).mean()

exact = (
    df["human_overall"] == df["llm_overall"]
).mean()

print("Spearman correlation:", round(float(rho), 4))
print("p-value:", round(float(p), 4))
print("Exact agreement:", round(float(exact), 4))
print("Agreement within 1 point:", round(float(within_one), 4))
