#!/usr/bin/env python3
"""Summarize categorical JSONL fields and expose dominant values."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any


def field(record: dict[str, Any], dotted: str) -> Any:
    value: Any = record
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            raise KeyError(dotted)
        value = value[part]
    return value


def label(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--field", action="append", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    counters = {name: Counter() for name in args.field}
    missing = Counter()
    rows = 0
    errors: list[str] = []
    for line_number, line in enumerate(args.input.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        rows += 1
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"line {line_number}: {error}")
            continue
        for name in args.field:
            try:
                counters[name][label(field(record, name))] += 1
            except KeyError:
                missing[name] += 1

    summaries: dict[str, Any] = {}
    for name, counter in counters.items():
        observed = sum(counter.values())
        top_value, top_count = counter.most_common(1)[0] if counter else (None, 0)
        summaries[name] = {
            "observed": observed,
            "missing": missing[name],
            "uniqueValues": len(counter),
            "counts": dict(sorted(counter.items())),
            "dominantValue": top_value,
            "dominantCount": top_count,
            "dominantShare": (top_count / observed) if observed else None,
        }
    if rows == 0:
        errors.append("input contains no rows")
    report = {"rows": rows, "fields": summaries, "valid": not errors, "errors": errors}
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
