#!/usr/bin/env python3
"""Hash JSONL splits and reject duplicate IDs or cross-split group leakage."""

from __future__ import annotations

import argparse
import hashlib
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", action="append", required=True, metavar="NAME=PATH")
    parser.add_argument("--id-field", default="id")
    parser.add_argument("--group-field", default="groupID")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    seen_ids: dict[str, str] = {}
    group_splits: dict[str, set[str]] = {}
    errors: list[str] = []
    splits: dict[str, dict[str, Any]] = {}

    for specification in args.split:
        name, separator, raw_path = specification.partition("=")
        if not separator or not name or not raw_path:
            parser.error(f"invalid --split {specification!r}; expected NAME=PATH")
        if name in splits:
            parser.error(f"duplicate split name {name!r}")
        path = Path(raw_path)
        raw = path.read_bytes()
        count = 0
        groups: set[str] = set()
        for line_number, line in enumerate(raw.decode("utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                row_id = str(field(record, args.id_field))
                group_id = str(field(record, args.group_field))
            except (json.JSONDecodeError, KeyError, TypeError) as error:
                errors.append(f"{name}:{line_number}: {error}")
                continue
            count += 1
            if row_id in seen_ids:
                errors.append(f"duplicate id {row_id!r} in {seen_ids[row_id]} and {name}")
            else:
                seen_ids[row_id] = name
            groups.add(group_id)
            group_splits.setdefault(group_id, set()).add(name)
        splits[name] = {
            "path": str(path.resolve()),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "rows": count,
            "groups": len(groups),
        }
        if count == 0:
            errors.append(f"split {name!r} contains no valid rows")

    leaked = {group: sorted(names) for group, names in group_splits.items() if len(names) > 1}
    if leaked:
        errors.append(f"groups cross splits: {leaked}")
    report = {
        "schemaVersion": 1,
        "idField": args.id_field,
        "groupField": args.group_field,
        "splits": splits,
        "totalRows": sum(item["rows"] for item in splits.values()),
        "uniqueGroups": len(group_splits),
        "groupLeakage": leaked,
        "valid": not errors,
        "errors": errors,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
