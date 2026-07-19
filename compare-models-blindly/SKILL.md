---
name: compare-models-blindly
description: Creates seeded blinded model-comparison packets and evaluates candidate outputs twice with reversed order to control identity and presentation bias. Use when two models or prompts produce different valid answers that require qualitative judging.
---

# Compare Models Blindly

Compare usable outputs without revealing model identity, teacher answers, latency, or prior scores to the judge.

## Freeze the comparison set

Select cases by predefined metadata and stable input order before inspecting outcomes. Record the manifest. Reuse saved inference when available; do not rerun a model merely to prepare judging.

Validate candidates independently before strategic or qualitative judging. A candidate that fails identifier, replay, terminal-boundary, or other safety gates cannot win.

## Build the blinded packet

Input rows should contain shared case context and two candidate fields. Run:

```sh
python scripts/blind_candidates.py disagreements.jsonl \
  --id-field id --left-field modelOne --right-field modelTwo \
  --seed experiment-v1 \
  --cases-output blinded-cases.jsonl \
  --mapping-output identity-mapping.json
```

Store the mapping separately. Do not consult it during judging. The script uses a SHA-256-derived assignment per case, so reruns with the same seed and IDs are stable.

## Judge twice

1. Judge Candidate A and Candidate B using only supplied context and a fixed controlled rubric.
2. Create a second pass with candidate order reversed.
3. Keep explanations compact and evidence-grounded; do not request chain-of-thought.
4. Translate both verdicts to underlying candidate identity.

Award a preference only when both orders select the same underlying candidate. Otherwise classify the case as order-sensitive. Preserve ties, both-poor outcomes, insufficient-context cases, and differing valid answers for later review.

## Report narrowly

Unblind only after both passes are complete. Report validation failures by model, stable wins, ties, inconclusive and order-sensitive cases, controlled score averages, and relevant metadata groups. Call automated judging what it is; do not claim human preference, product usefulness, or model acceptance.
