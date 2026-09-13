import json
import os
from pathlib import Path

from .config import INTENTS

def keyword_baseline(text):
    t = text.lower()
    rules = [
        (["refund", "money back", "refunded"], "refund"),
        (["charged", "charge", "payment", "billing", "bill"], "billing_payment"),
        (["cancel", "cancellation"], "subscription_cancel"),
        (["premium", "subscription", "plan"], "subscription_plan"),
        (["login", "log in", "sign in", "password"], "account_login"),
        (["hack", "hacked", "stolen", "security"], "account_security"),
        (["premium not", "premium isn't", "premium doesn't"], "premium_not_working"),
        (["can't play", "cannot play", "playback", "song won't play"], "playback_problem"),
        (["app", "crash", "bug", "error"], "app_technical_problem"),
        (["playlist", "song", "artist", "music"], "playlist_music_problem"),
        (["family", "student"], "family_student_plan"),
        (["gift", "voucher", "code"], "gift_code"),
        (["feature", "please add", "would love"], "feature_request"),
        (["angry", "terrible", "worst", "unacceptable"], "general_complaint"),
    ]
    for words, label in rules:
        if any(w in t for w in words):
            return label
    return "other"

def llm_intent(text):
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    prompt = f"""Classify this Spotify customer-support message into exactly one intent.

Allowed intents:
{json.dumps(INTENTS)}

Customer message:
{text}

Return only JSON:
{{"intent":"one_allowed_intent","confidence":0.0}}
"""
    r = client.responses.create(model=model, input=prompt)
    data = json.loads(r.output_text)
    if data["intent"] not in INTENTS:
        return "other", 0.0
    return data["intent"], float(data.get("confidence", 0.0))
