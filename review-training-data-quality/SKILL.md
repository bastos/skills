---
name: review-training-data-quality
description: Audits a candidate or labeled training corpus for distribution collapse, ambiguity, context sufficiency, hard-negative quality, abstention behavior, leakage, and stable label defensibility. Use before scaling teacher calls or starting fine-tuning.
---

# Review Training Data Quality

Test whether the dataset teaches the intended capability rather than merely producing an easy loss curve.

## Inspect deterministic distributions

Summarize every product-relevant axis by split and overall: source group, task lane, goal, format, label, abstention, difficulty, candidate count, sequence length, terminal state, role, and preferred-answer position.

Use the generic JSONL summary helper:

```sh
python scripts/summarize_jsonl_fields.py corpus.jsonl \
  --field split --field lane --field goal --field label \
  --output quality-distributions.json
```

Look beyond equal row counts. Verify group-safe splits, distinct source groups, reasonable joint distributions, and enough examples at safety boundaries. Flag any category whose dominance would let the model ignore important context.

## Review candidate and label quality

Check that:

- positives are legal, plausible, and supported by supplied context;
- hard negatives are tempting but wrong for an explainable reason;
- multiple acceptable answers are preserved when evidence supports them;
- abstention is available and labeled only when warranted;
- teacher outputs use supplied identifiers and validate without silent repair;
- prompts exclude reference answers and teacher-only metadata;
- every lane has sufficient facts to make a defensible choice.

Run a small balanced teacher preflight before labeling the full corpus. Stop on identifier, replay, legality, terminal-boundary, context, or label-collapse failures.

## Test label defensibility

Blind-review difficult representative cases twice with candidate order reversed. Select cases from metadata, not label outcomes. Count a judgment as stable only when both orders choose the same underlying answer. Preserve ties, ambiguity, both-poor, and insufficient-context results.

Define the stability threshold before review. If the threshold fails, fix the smallest corpus or rubric defect before scaling. More examples of the same biased lane are not evidence of broader capability.
