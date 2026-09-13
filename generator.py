import os

def generate_reply(message, intent, examples):
    if not os.getenv("OPENAI_API_KEY"):
        if examples:
            return examples[0]["historical_reply"]
        return "Thanks for reaching out. We’d like to look into this and help you further."

    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    evidence = "\n\n".join(
        f"Customer: {x['customer_message']}\nBrand reply: {x['historical_reply']}"
        for x in examples
    )

    prompt = f"""You are Spotify customer support.

Customer message:
{message}

Detected intent:
{intent}

Historical Spotify support examples:
{evidence}

Write one concise Twitter-style reply.

Rules:
- Ground the response in the historical examples.
- Never claim that a refund, account change, or investigation has already happened unless the evidence explicitly supports that exact claim.
- Do not invent policies.
- Ask for a DM only when account-specific information is needed.
- Be empathetic and concise.
- Return only the reply text.
"""
    r = client.responses.create(model=model, input=prompt)
    return r.output_text.strip()
