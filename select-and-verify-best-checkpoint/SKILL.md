---
name: select-and-verify-best-checkpoint
description: Proves that evaluation ran at the intended cadence, the tracked metric selected the true best checkpoint, and held-out inference loaded that checkpoint. Use with Hugging Face Trainer or compatible training-state artifacts before trusting test metrics.
---

# Select and Verify Best Checkpoint

Treat checkpoint identity as an evidence requirement, not a configuration assumption.

## Configure selection explicitly

Set evaluation and saving to compatible cadences. Specify the metric, whether greater is better, and best-model loading. Ensure the configured metric name matches the emitted evaluation key; account for frameworks that add an `eval_` prefix.

## Verify trainer state

After training, run:

```sh
python scripts/verify_checkpoint.py output/trainer_state.json \
  --metric eval_loss \
  --expected-eval-steps 50,100,150 \
  --evaluation-manifest held-out-run.json \
  --loaded-checkpoint-field loadedCheckpoint \
  --output checkpoint-proof.json
```

The script fails unless:

- the expected evaluation steps are present;
- `best_metric` and `best_model_checkpoint` are non-null;
- the recorded metric equals the optimum in evaluation history;
- the best checkpoint step matches the optimum step;
- the held-out manifest identifies that exact checkpoint.

Use `--greater-is-better` for maximized metrics and repeat `--required-file` to require adapter or model files inside the best checkpoint.

## Preserve proof

Record the trainer state hash, checkpoint path and hash inventory, best metric and step, evaluation manifest, and evaluation command. If ties exist, report the framework's selected tied checkpoint rather than pretending the optimum is unique. Never claim held-out results came from the best checkpoint without an explicit load identity.
