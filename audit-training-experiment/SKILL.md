---
name: audit-training-experiment
description: Audits an ML training experiment for reproducibility, evidence integrity, leakage, checkpoint identity, evaluation validity, and overclaimed conclusions. Use before accepting results, spending on a longer run, publishing artifacts, or handing work to another agent.
---

# Audit Training Experiment

Audit the claim against the preserved evidence. Do not regenerate missing evidence during the audit unless explicitly asked; identify the gap.

## Reconstruct the experiment

Verify that the record contains:

- hypothesis, acceptance and stop gates, scope, and explicit non-claims;
- source and dataset revisions, split manifests, provenance, licenses, and hashes;
- generator, teacher, prompt, schema, validator, tokenizer, and model revisions;
- exact command/configuration, seed, packages, hardware, runtime, memory, and cost;
- complete logs, checkpoint inventory, best metric and checkpoint identity;
- raw held-out outputs, normalized outputs, per-case validation, and latency.

Confirm that preserved hashes match current artifacts. Distinguish unavailable evidence from failed evidence.

## Challenge validity

Check for:

- row or group leakage across splits;
- labels, canonical identifiers, intent metadata, or teacher answers in prompts;
- outcome-based case selection;
- retries, repairs, remediation, or fallback hidden inside first-attempt metrics;
- test-set use during prompt, corpus, or checkpoint selection;
- evaluation of the final checkpoint while claiming the best checkpoint;
- collapsed labels, goals, lanes, positions, or abstentions;
- untested safety boundaries or unsupported generalization;
- averages that hide per-lane failures;
- loss presented as usefulness or acceptance.

Recompute inexpensive counts and hashes from preserved artifacts. Do not overwrite original reports when correcting them; create a clearly named addendum or new revision.

## Deliver the verdict

List each gate as passed, failed, not run, or not applicable with an evidence path. State the narrowest defensible conclusion and the smallest concrete next fix. Preserve negative evidence and prevent incompatible runs from sharing a state file or revision label.
