---
name: close-out-ml-experiment
description: Preserves positive or negative ML experiment evidence, reconciles report discrepancies, records the canonical decision and limitations, and prepares a concise handoff. Use when stopping an experiment, rejecting a prompt/model, or freezing a result before the next iteration.
---

# Close Out ML Experiment

End the experiment without erasing what it taught.

## Freeze evidence first

Stop active inference or training when requested, but preserve completed outputs. Do not regenerate, relabel, overwrite, move, or reinterpret raw evidence. Hash baseline and final artifacts and verify expected files before editing summaries.

Inventory:

- corpus, manifests, provenance, and exact splits;
- commands, configs, prompts, schemas, revisions, and seeds;
- logs, checkpoints, adapters, raw/normalized outputs, latency, and validator results;
- blinded packets, both judging passes, identity mappings, and reports.

## Reconcile the record

Recalculate inexpensive totals from per-case artifacts. If a report omits a category or case, preserve its measured values and add a clearly named correction or addendum. Explain the discrepancy; do not rewrite history or rerun inference to make totals agree.

## Record the decision

State:

- what changed and what stayed canonical;
- exact result deltas and hard safety failures;
- passed, failed, untested, and not-applicable gates;
- dataset and judging limitations;
- whether the evidence is a smoke, automated evaluation, model-as-judge review, or human study;
- the smallest justified next experiment or fix.

Do not claim model, product, strategic, human, device, energy, or production acceptance from narrower evidence.

## Hand off durably

Write a concise reproducible report beside the experiment evidence. If the project uses an issue tracker, add one high-signal comment with decision, metrics, artifact locations/hashes, limitations, and next step. Keep broader qualification issues open when only one subexperiment ended. Commit only explicitly authorized, scoped source or documentation changes; never commit credentials, datasets, weights, checkpoints, adapters, or unrelated files.
