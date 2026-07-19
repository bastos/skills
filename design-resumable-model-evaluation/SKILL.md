---
name: design-resumable-model-evaluation
description: Designs strict model benchmarks that persist per-case evidence, resume without repeating completed work, separate first-attempt behavior from remediation, and stop early only when failure is mathematically certain. Use for slow, costly, or interruptible evaluations.
---

# Design Resumable Model Evaluation

Make interruption cheap and evidence comparable.

## Freeze an evaluation revision

Create a unique revision for every combination of corpus membership, model, prompt/instructions, schema, decoder settings, validator, run count, and thresholds. Hash this configuration into the state file. Never seed a new revision from incompatible results.

Write the case manifest before inference. Select cases from stable metadata, not previous outcomes.

## Persist atomically

Use an append-only result stream or atomically replace a small state file after every case/run. Store:

- case and run IDs;
- frozen configuration hash;
- raw and normalized output;
- parse, identifier, semantic, execution, and safety gate results;
- abstention and generation-failure status;
- start/end timestamps and latency;
- interruption and retry metadata.

On resume, validate the configuration hash, scan completed keys, and execute only missing `(case, run)` pairs. Deduplicate safely if a crash occurred after writing output but before updating summary state.

## Preserve benchmark semantics

Evaluate first-attempt output with exactly one generation when that is the product question. Do not call production remediation, repair malformed JSON, or deterministically choose a fallback. Exercise remediation in a separate test and metric series.

Keep required run counts and thresholds unchanged. A resumable evaluator improves execution efficiency, not acceptance criteria.

## Stop only on safe math

For a minimum rate `t` over `N` required trials, fail early only when even winning every remaining trial cannot reach the required successes:

`successes + remaining < ceil(t * N)`

For maximum-failure gates, stop only once the allowed failure count is irreversibly exceeded. Apply the same reasoning separately to each gate and subgroup. Do not early-pass unless all required trials are complete.

## Report

Report completed and required runs, completed fixtures/cases, failures, abstentions, gate numerators and denominators, distribution/diversity gates, p50/p95 latency, interruptions, resumptions, and exact automated gate results. State which human, device, energy, usefulness, or product gates remain untested.
