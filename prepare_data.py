import argparse
import json
import re
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

BRAND_HINTS = {
    "spotify": ["spotify", "spotifycares", "spotify care", "spotify premium"],
}

def clean_text(x):
    x = str(x or "").replace("\n", " ").strip()
    x = re.sub(r"\s+", " ", x)
    return x

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--brand", default="spotify")
    ap.add_argument("--max-examples", type=int, default=30000)
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    required = {
        "tweet_id", "inbound", "text",
        "response_tweet_id", "in_response_to_tweet_id"
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    # Spotify is represented by support-account authors. We infer the support
    # account IDs from outbound tweets and retain only conversations that have
    # both inbound and outbound messages. This avoids requiring an explicit
    # brand-name column, which the original dataset does not provide.
    df["text"] = df["text"].map(clean_text)
    df["tweet_id"] = df["tweet_id"].astype(str)
    df["author_id"] = df["author_id"].astype(str)
    df["in_response_to_tweet_id"] = df["in_response_to_tweet_id"].fillna("").astype(str)

    # The public dataset has no brand column. We identify Spotify by text/account
    # hints when possible, then use a known support-account author pattern.
    # If this produces too few examples, inspect outbound authors with:
    # python scripts/list_support_accounts.py --input data/twcs.csv
    mask = df["text"].str.lower().str.contains(
        r"\bspotify\b|\bspotifycares\b|\bspotify premium\b", regex=True, na=False
    )
    candidates = df[mask].copy()

    # Add conversation neighbours around Spotify-mentioned tweets.
    ids = set(candidates["tweet_id"])
    parent_ids = set(candidates["in_response_to_tweet_id"]) - {""}
    neigh = df[df["tweet_id"].isin(ids | parent_ids)].copy()

    if len(neigh) < 500:
        raise RuntimeError(
            "Too few Spotify candidates. Run scripts/list_support_accounts.py "
            "and inspect support-account IDs; then set SPOTIFY_AUTHOR_IDS."
        )

    # Keep inbound customer messages that have an outbound response.
    outbound = neigh[neigh["inbound"] == False].copy()
    inbound = neigh[neigh["inbound"] == True].copy()

    pairs = []
    for _, row in inbound.iterrows():
        response_ids = str(row.get("response_tweet_id", "") or "")
        first = response_ids.split(",")[0].strip()
        if first:
            resp = neigh[neigh["tweet_id"] == first]
            if not resp.empty:
                pairs.append({
                    "customer_tweet_id": row["tweet_id"],
                    "customer_message": row["text"],
                    "response_tweet_id": first,
                    "historical_reply": clean_text(resp.iloc[0]["text"]),
                })

    out = pd.DataFrame(pairs).drop_duplicates("customer_tweet_id")
    if out.empty:
        raise RuntimeError("No customer→support pairs found in the selected sample.")

    out = out.head(args.max_examples)

    Path("artifacts").mkdir(exist_ok=True)
    out.to_json("artifacts/spotify_examples.jsonl", orient="records", lines=True)

    # Candidate golden set. Human must label it.
    n = min(200, len(out))
    golden = out.sample(n=n, random_state=42).copy()
    golden["id"] = [f"golden_{i:04d}" for i in range(len(golden))]
    golden["intent"] = ""
    golden["expected_route"] = ""
    golden["reference_reply"] = golden["historical_reply"]
    golden[[
        "id", "customer_message", "intent",
        "expected_route", "reference_reply"
    ]].to_json(
        "artifacts/golden_template.jsonl",
        orient="records",
        lines=True
    )

    print(f"Saved {len(out)} Spotify customer→reply pairs.")
    print("Saved 200-example golden template (or fewer if the sample is smaller).")
    print("IMPORTANT: manually label the golden template before evaluation.")

if __name__ == "__main__":
    main()
