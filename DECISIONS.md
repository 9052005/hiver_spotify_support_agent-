# Decision Log

1. **Selected Spotify as the single brand.** It has a recognizable support identity and enough public support conversations to make retrieval and intent analysis practical.

2. **Used a compact 15-intent taxonomy.** A smaller taxonomy is easier to evaluate reliably than dozens of highly granular labels.

3. **Made Macro-F1 the primary intent metric.** Customer-support intent distributions are naturally imbalanced.

4. **Built a majority baseline.** It establishes how much performance comes simply from class imbalance.

5. **Built a keyword baseline.** It measures whether an LLM system actually beats a simple interpretable approach.

6. **Used retrieval before generation.** The assignment asks for replies grounded in historical resolutions, so historical evidence is explicitly passed to generation.

7. **Used TF-IDF retrieval first.** It is inexpensive, deterministic, easy to reproduce, and provides a strong enough baseline before adding embeddings.

8. **Made escalation conservative.** Incorrect auto-handling can be more damaging than sending an extra case to a human.

9. **Escalate financial/security issues.** These commonly require account-specific verification.

10. **Do not allow the generator to invent completed actions.** A fluent reply claiming that money was refunded when it was not would be a serious support failure.

11. **Held out the golden set from retrieval.** This prevents exact or near-exact test leakage.

12. **Validate the LLM judge against humans.** An LLM score is not ground truth.

13. **Do not build Twitter API integration.** It adds engineering complexity without improving the offline evidence required by the assignment.

14. **Do not build autonomous account actions.** The dataset contains conversations, not authenticated account state or transaction tools.

15. **Prefer reproducibility over a UI.** A command-line pipeline makes the headline experiment easier for reviewers to reproduce.
