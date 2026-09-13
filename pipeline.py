import argparse
import json
import os

from dotenv import load_dotenv

from .intent import keyword_baseline, llm_intent
from .retriever import Retriever
from .router import route
from .generator import generate_reply

load_dotenv()


def run(message):
    retriever = Retriever()

    # Retrieve historically similar Spotify conversations
    examples = retriever.search(message, k=5)

    # Use LLM classification when an API key is available.
    # Otherwise use the keyword baseline.
    if os.getenv("OPENAI_API_KEY"):
        intent, confidence = llm_intent(message)
    else:
        intent = keyword_baseline(message)
        confidence = 0.0

    # Similarity of the best historical example
    best_similarity = (
        examples[0]["similarity"]
        if examples
        else 0.0
    )

    # Decide AUTO vs ESCALATE
    decision, reason = route(
        intent,
        best_similarity,
        message
    )

    # Generate the support reply
    reply = generate_reply(
        message,
        intent,
        examples
    )

    return {
        "intent": intent,
        "confidence": confidence,
        "reply": reply,
        "decision": decision,
        "reason": reason,
        "evidence": [
            {
                "customer": e["customer_message"],
                "historical_reply": e["historical_reply"],
                "similarity": round(
                    e["similarity"],
                    3
                ),
            }
            for e in examples
        ],
    }


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--message",
        required=True,
        help="Customer message to process"
    )

    args = parser.parse_args()

    result = run(args.message)

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )