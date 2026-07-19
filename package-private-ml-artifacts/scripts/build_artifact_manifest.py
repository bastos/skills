#!/usr/bin/env python3
"""Inventory artifacts and reject likely credentials before private upload."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


SENSITIVE_NAME = re.compile(r"(^|[._-])(\.env|credential|credentials|secret|secrets|token|tokens)([._-]|$)", re.IGNORECASE)
SENSITIVE_CONTENT = [
    re.compile(rb"hf_[A-Za-z0-9]{20,}"),
    re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-file-mb", type=float, default=5000)
    args = parser.parse_args()

    root = args.root.resolve()
    output = args.output.resolve()
    errors: list[str] = []
    files: list[dict[str, object]] = []
    limit = int(args.max_file_mb * 1024 * 1024)
    for path in sorted(item for item in root.rglob("*") if item.is_file() and item.resolve() != output):
        relative = path.relative_to(root).as_posix()
        size = path.stat().st_size
        if size > limit:
            errors.append(f"oversized file: {relative} ({size} bytes)")
        if SENSITIVE_NAME.search(path.name):
            errors.append(f"suspicious credential filename: {relative}")
        with path.open("rb") as handle:
            sample = handle.read(min(size, 2 * 1024 * 1024))
        if any(pattern.search(sample) for pattern in SENSITIVE_CONTENT):
            errors.append(f"suspicious credential content: {relative}")
        files.append({"path": relative, "bytes": size, "sha256": sha256(path)})
    if not files:
        errors.append("artifact root contains no files")

    report = {
        "schemaVersion": 1,
        "root": str(root),
        "fileCount": len(files),
        "totalBytes": sum(int(item["bytes"]) for item in files),
        "files": files,
        "valid": not errors,
        "errors": errors,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
