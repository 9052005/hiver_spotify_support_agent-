# Hiver Take-Home Report — Spotify Support Agent

## 1. Problem framing

### What good means
- Intent classification should correctly identify the customer's issue.
- Replies should be relevant, historically grounded, and avoid unsupported claims.
- High-risk/account-specific cases should be escalated rather than confidently auto-handled.

### What we did not build
- Live Twitter integration
- Refund/account-changing actions
- Multi-brand support
- Production infrastructure

## 2. Data and sampling

Dataset: Customer Support on Twitter.

Brand: Spotify.

Describe:
- number of rows inspected
- number of Spotify examples
- how conversation pairs were reconstructed
- how the 200-example golden set was sampled
- how leakage was prevented

## 3. Intent taxonomy

List the final intents and give one sentence describing each.

## 4. Results

| System | Accuracy | Macro-F1 |
|---|---:|---:|
| Majority | | |
| Keyword | | |
| LLM zero-shot | | |
| Our agent | | |

Routing:

| System | Accuracy | Macro-F1 |
|---|---:|---:|
| Our agent | | |

Reply judge:

| Metric | Score |
|---|---:|
| Relevance | |
| Groundedness | |
| Correctness | |
| Helpfulness | |
| Tone | |
| Conciseness | |

## 5. LLM judge validation

Human sample size:

Spearman correlation:

Exact agreement:

Within-one-point agreement:

Explain why the judge should not be considered ground truth.

## 6. Top five failure modes

For each:
1. real example
2. expected output
3. actual output
4. hypothesis for failure
5. proposed fix

## 7. What is misleading about my headline number?

Discuss:
- class imbalance
- small golden-set size
- offline evaluation
- judge bias
- retrieval leakage risk
- real-world distribution shift
- fluent but operationally incorrect replies

## 8. One more week

Prioritize:
1. better human-labelled data
2. stronger retrieval/embedding model
3. calibrated routing
4. adversarial evaluation
5. temporal/brand-policy drift analysis
