import json
import os
from openai import OpenAI

RUBRIC = {
    "relevance": "Does the reply directly address the customer's issue?",
    "groundedness": "Is the reply supported by the historical evidence?",
    "correctness": "Does it avoid unsupported or fabricated claims?",
    "helpfulness": "Does it provide a useful next step?",
    "tone": "Does it sound appropriate for customer support?",
    "conciseness": "Is it concise enough for Twitter support?",
}

def judge(customer, evidence, reply):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    prompt = f"""Evaluate a customer-support reply.

Customer:
{customer}

Historical evidence:
{evidence}

Reply:
{reply}

Score each dimension from 1 to 5:
{json.dumps(RUBRIC, indent=2)}

Return only JSON:
{{"relevance":1,"groundedness":1,"correctness":1,"helpfulness":1,"tone":1,"conciseness":1,"overall":1,"reason":"brief reason"}}
"""
    r = client.responses.create(model=model, input=prompt)
    return json.loads(r.output_text)
