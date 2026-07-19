---
name: package-private-ml-artifacts
description: Inventories, hashes, scans, and verifies datasets, adapters, checkpoints, logs, and evaluation evidence before an explicitly approved private upload. Use when ephemeral jobs or handoffs require durable ML artifacts without exposing credentials or unapproved data.
---

# Package Private ML Artifacts

Preserve reproducibility while keeping credentials, restricted sources, and large assets out of source control.

## Confirm authorization and scope

Obtain explicit approval before uploading datasets, weights, adapters, checkpoints, or other large artifacts. Confirm the destination is private and list exactly what will be uploaded. Never infer that permission to train also grants permission to publish artifacts.

Classify each artifact by source, license, sensitivity, retention need, and whether it belongs in Git, private object storage, or a private model/dataset repository.

## Build a manifest

Run:

```sh
python scripts/build_artifact_manifest.py experiment-output \
  --output experiment-output/artifact-manifest.json \
  --max-file-mb 5000
```

The script records relative paths, byte sizes, and SHA-256 hashes and fails on suspicious credential filenames/content or oversized files. Review flagged paths; do not weaken the scan merely to complete an upload.

Include reproduction inputs: commands, configuration, revisions, seed, packages, hardware, source/split manifests, logs, raw outputs, normalized results, validators, and reports. Do not include environment files, tokens, caches, or unrelated workspace data.

## Upload and verify

1. Create or verify the private destination before transfer.
2. Upload the manifest with the artifacts.
3. Record destination repository, revision/commit, upload command, and timestamp.
4. Re-list or download enough data to prove remote sizes and hashes match.
5. Keep local evidence until remote verification succeeds.

Report omissions and why they were omitted. Do not call an upload complete when only a mutable branch name, partial logs, or unverified files remain.
