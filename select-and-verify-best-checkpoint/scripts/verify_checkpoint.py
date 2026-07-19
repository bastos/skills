#!/usr/bin/env python3
"""Verify Trainer best-checkpoint tracking and explicit held-out reload identity."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def field(record: dict[str, Any], dotted: str) -> Any:
    value: Any = record
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            raise KeyError(dotted)
        value = value[part]
    return value


def resolved(path: str | Path, base: Path) -> Path:
    candidate = Path(path)
    return (candidate if candidate.is_absolute() else base / candidate).resolve()


def training_path(path: str | Path, root: Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate.resolve()
    choices = [root / candidate]
    if candidate.parts and candidate.parts[0] == root.name:
        choices.insert(0, root.parent / candidate)
    return next((choice.resolve() for choice in choices if choice.exists()), choices[0].resolve())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trainer_state", type=Path)
    parser.add_argument("--metric", default="eval_loss")
    parser.add_argument("--greater-is-better", action="store_true")
    parser.add_argument("--expected-eval-steps")
    parser.add_argument("--training-root", type=Path)
    parser.add_argument("--evaluation-manifest", type=Path, required=True)
    parser.add_argument("--loaded-checkpoint-field", default="loadedCheckpoint")
    parser.add_argument("--required-file", action="append", default=[])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    state = json.loads(args.trainer_state.read_text(encoding="utf-8"))
    errors: list[str] = []
    history = [entry for entry in state.get("log_history", []) if args.metric in entry and "step" in entry]
    steps = [int(entry["step"]) for entry in history]
    if args.expected_eval_steps:
        expected = [int(value) for value in args.expected_eval_steps.split(",") if value]
        missing = sorted(set(expected) - set(steps))
        if missing:
            errors.append(f"missing evaluation steps: {missing}")
    if not history:
        errors.append(f"no log history entries emit {args.metric!r}")

    best_metric = state.get("best_metric")
    best_path_raw = state.get("best_model_checkpoint")
    if best_metric is None:
        errors.append("best_metric is null")
    if not best_path_raw:
        errors.append("best_model_checkpoint is null")

    optimum_entry = None
    if history:
        optimum_entry = (max if args.greater_is_better else min)(history, key=lambda item: float(item[args.metric]))
        if best_metric is not None and not math.isclose(float(best_metric), float(optimum_entry[args.metric]), rel_tol=1e-9, abs_tol=1e-12):
            errors.append(f"recorded best_metric {best_metric} != observed optimum {optimum_entry[args.metric]}")

    training_root = (args.training_root or args.trainer_state.parent).resolve()
    best_path = training_path(best_path_raw, training_root) if best_path_raw else None
    if best_path and optimum_entry and best_path.name != f"checkpoint-{int(optimum_entry['step'])}":
        errors.append(f"best checkpoint {best_path.name} does not match optimum step {optimum_entry['step']}")
    if best_path:
        for relative in args.required_file:
            if not (best_path / relative).is_file():
                errors.append(f"best checkpoint missing required file: {relative}")

    manifest = json.loads(args.evaluation_manifest.read_text(encoding="utf-8"))
    try:
        loaded_raw = field(manifest, args.loaded_checkpoint_field)
        loaded_path = resolved(str(loaded_raw), args.evaluation_manifest.parent)
    except KeyError:
        loaded_path = None
        errors.append(f"evaluation manifest lacks {args.loaded_checkpoint_field!r}")
    if best_path and loaded_path and best_path != loaded_path:
        errors.append(f"held-out loaded {loaded_path}, expected {best_path}")

    report = {
        "metric": args.metric,
        "greaterIsBetter": args.greater_is_better,
        "evaluationSteps": steps,
        "bestMetric": best_metric,
        "observedOptimum": optimum_entry,
        "bestCheckpoint": str(best_path) if best_path else None,
        "heldOutLoadedCheckpoint": str(loaded_path) if loaded_path else None,
        "valid": not errors,
        "errors": errors,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
