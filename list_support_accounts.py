import argparse
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True)
args = ap.parse_args()

df = pd.read_csv(args.input)
out = df[df["inbound"] == False].groupby("author_id").size().sort_values(ascending=False)
print(out.head(100).to_string())
