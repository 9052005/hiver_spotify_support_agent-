import json
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Retriever:
    def __init__(self, path="artifacts/spotify_examples.jsonl"):
        self.rows = [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines()]
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            min_df=2,
            max_features=60000,
            sublinear_tf=True,
        )
        self.matrix = self.vectorizer.fit_transform(
            [r["customer_message"] for r in self.rows]
        )

    def search(self, query, k=5):
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix).ravel()
        idx = np.argsort(-scores)[:k]
        return [
            {**self.rows[i], "similarity": float(scores[i])}
            for i in idx
        ]
