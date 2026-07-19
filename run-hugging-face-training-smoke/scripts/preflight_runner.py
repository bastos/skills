#!/usr/bin/env python3
"""Perform cheap deterministic checks on a Python cloud-training runner."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("runner", type=Path)
    parser.add_argument("--require", action="append", default=[])
    parser.add_argument("--forbid", action="append", default=[])
    parser.add_argument("--allow-file-assumption", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    raw = args.runner.read_bytes()
    source = raw.decode("utf-8")
    errors: list[str] = []
    try:
        ast.parse(source, filename=str(args.runner))
    except SyntaxError as error:
        errors.append(f"syntax: {error.msg} at line {error.lineno}")

    missing = [value for value in args.require if value not in source]
    forbidden = [value for value in args.forbid if value in source]
    if missing:
        errors.append(f"missing required text: {missing}")
    if forbidden:
        errors.append(f"found forbidden text: {forbidden}")
    if "__file__" in source and not args.allow_file_assumption:
        errors.append("runner relies on __file__; verify stdin/job execution or allow explicitly")

    report = {
        "runner": str(args.runner.resolve()),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "requiredText": {value: value in source for value in args.require},
        "forbiddenText": {value: value in source for value in args.forbid},
        "usesDunderFile": "__file__" in source,
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
