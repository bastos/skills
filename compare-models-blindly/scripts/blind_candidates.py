#!/usr/bin/env python3
"""Create deterministic per-case candidate blinding and a separate mapping."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def swap(seed: str, case_id: str) -> bool:
    digest = hashlib.sha256(f"{seed}\0{case_id}".encode()).digest()
    return bool(digest[0] & 1)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--id-field", default="id")
    parser.add_argument("--left-field", required=True)
    parser.add_argument("--right-field", required=True)
    parser.add_argument("--seed", required=True)
    parser.add_argument("--cases-output", type=Path, required=True)
    parser.add_argument("--mapping-output", type=Path, required=True)
    args = parser.parse_args()

    cases: list[dict[str, Any]] = []
    mappings: list[dict[str, str]] = []
    seen: set[str] = set()
    for line_number, line in enumerate(args.input.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        case_id = str(record[args.id_field])
        if case_id in seen:
            raise ValueError(f"duplicate case ID {case_id!r} at line {line_number}")
        seen.add(case_id)
        left = record.pop(args.left_field)
        right = record.pop(args.right_field)
        if swap(args.seed, case_id):
            candidate_a, candidate_b = right, left
            identity_a, identity_b = args.right_field, args.left_field
        else:
            candidate_a, candidate_b = left, right
            identity_a, identity_b = args.left_field, args.right_field
        record["candidateA"] = candidate_a
        record["candidateB"] = candidate_b
        cases.append(record)
        mappings.append({"id": case_id, "candidateA": identity_a, "candidateB": identity_b})

    if not cases:
        raise ValueError("input contains no cases")
    write_jsonl(args.cases_output, cases)
    mapping = {"schemaVersion": 1, "seed": args.seed, "cases": mappings}
    args.mapping_output.parent.mkdir(parents=True, exist_ok=True)
    args.mapping_output.write_text(json.dumps(mapping, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(cases), "casesOutput": str(args.cases_output), "mappingOutput": str(args.mapping_output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
