from .config import HIGH_RISK_INTENTS, AUTO_INTENTS

def route(intent, similarity, text):
    t = text.lower()

    if intent in HIGH_RISK_INTENTS:
        return "ESCALATE", "Financial, refund, or account-security issues can require account-level verification."

    if any(x in t for x in ["fraud", "scam", "stolen", "hacked", "legal", "lawyer", "chargeback"]):
        return "ESCALATE", "The message contains a high-risk financial, security, or legal concern."

    if similarity < 0.18:
        return "ESCALATE", "No sufficiently similar historical support example was retrieved."

    if intent in AUTO_INTENTS:
        return "AUTO", "The issue matches a known low-risk support intent with historical precedent."

    return "ESCALATE", "The issue is not sufficiently safe for automatic handling."
