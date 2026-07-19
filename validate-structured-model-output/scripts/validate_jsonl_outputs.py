#!/usr/bin/env python3
"""Validate supplied, ranked, and alternative identifier arrays in JSONL."""

from __future__ import annotations

import argparse
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


def ids(record: dict[str, Any], dotted: str) -> list[str]:
    value = field(record, dotted)
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise TypeError(f"{dotted} must be an array of strings")
    return value


def duplicates(values: list[str]) -> list[str]:
    return sorted({value for value in values if values.count(value) > 1})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--supplied-field", default="suppliedIDs")
    parser.add_argument("--ranked-field", default="rankedIDs")
    parser.add_argument("--alternative-field")
    parser.add_argument("--max-ranked", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    failures: list[dict[str, Any]] = []
    rows = 0
    for line_number, line in enumerate(args.input.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        rows += 1
        row_errors: list[str] = []
        try:
            record = json.loads(line)
            supplied = ids(record, args.supplied_field)
            ranked = ids(record, args.ranked_field)
            alternatives = ids(record, args.alternative_field) if args.alternative_field else []
            for label, values in (("supplied", supplied), ("ranked", ranked), ("alternatives", alternatives)):
                repeated = duplicates(values)
                if repeated:
                    row_errors.append(f"duplicate {label} IDs: {repeated}")
            if len(ranked) > args.max_ranked:
                row_errors.append(f"ranked length {len(ranked)} exceeds {args.max_ranked}")
            unknown = sorted((set(ranked) | set(alternatives)) - set(supplied))
            if unknown:
                row_errors.append(f"unknown IDs: {unknown}")
            overlap = sorted(set(ranked) & set(alternatives))
            if overlap:
                row_errors.append(f"ranked/alternative overlap: {overlap}")
            if alternatives and not ranked:
                row_errors.append("alternatives require at least one ranked selection")
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            row_errors.append(str(error))
        if row_errors:
            failures.append({"line": line_number, "errors": row_errors})

    if rows == 0:
        failures.append({"line": None, "errors": ["input contains no rows"]})
    report = {"rows": rows, "validRows": max(0, rows - len(failures)), "invalidRows": len(failures), "valid": not failures, "failures": failures}
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
