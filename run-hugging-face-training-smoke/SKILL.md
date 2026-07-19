---
name: run-hugging-face-training-smoke
description: Runs one bounded, private Hugging Face training smoke with immutable inputs, local preflight checks, explicit stop gates, checkpoint verification, and reproducible evidence. Use before spending cloud compute on a longer fine-tuning run.
---

# Run Hugging Face Training Smoke

Run the smallest experiment that can disprove the training setup. Treat a passing smoke as permission to consider a longer run, never as model or product acceptance.

## Establish the boundary

1. Record the hypothesis, maximum optimizer steps, hardware, timeout, budget, seed, and stop gates.
2. Freeze dataset splits, model revision, tokenizer revision, prompt contract, held-out manifest, and validator revision. Hash local inputs before renting compute.
3. Confirm the user has authorized paid compute and any artifact upload. Keep repositories private unless explicitly told otherwise.
4. Load credentials from the authorized environment without printing or copying them into commands, logs, manifests, or source.

## Preflight locally

Run `scripts/preflight_runner.py` against the exact submitted runner:

```sh
python scripts/preflight_runner.py path/to/runner.py \
  --require "load_best_model_at_end" \
  --forbid "print(os.environ"
```

Then execute the runner's cheapest supported dry run or stdin simulation. Verify:

- imports and argument parsing succeed;
- dataset and model revisions resolve;
- chat/template formatting produces completion-only labels as intended;
- the output directory and private Hub target are explicit;
- evaluation occurs at the intended cadence;
- the metric used for best-model selection matches the emitted metric;
- held-out evaluation explicitly reloads the recorded best checkpoint;
- incremental logs and results survive job termination.

Do not rely on `load_best_model_at_end` alone as proof of the evaluated checkpoint.

## Launch exactly one bounded job

Submit the already-preflighted command. Record the job ID and immutable command immediately. Monitor only long enough to detect startup, data, memory, loss, or checkpoint failures. Do not automatically retry a paid job; preserve the failure and obtain new authorization when another paid attempt is needed.

Stop when any project-defined gate fails. Never relax parsing, supplied-ID, legality, replay, safety, or quality thresholds because the loss curve looks healthy.

## Evaluate and report

Evaluate the frozen held-out cases once, without repair or retry, using the recorded best-validation checkpoint. Preserve:

- exact command, configuration, revisions, hashes, seed, package versions, GPU, runtime, peak memory, and estimated cost;
- train/evaluation loss history and best metric, step, and checkpoint;
- proof of the checkpoint loaded for held-out inference;
- raw and normalized outputs, validator results, latency, and domain gates;
- artifact locations and hashes.

State the narrowest justified conclusion. A smoke can prove that the pipeline trains and obeys a contract; it cannot establish strategic usefulness or production acceptance.
