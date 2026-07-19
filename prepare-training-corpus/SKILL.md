---
name: prepare-training-corpus
description: Builds and freezes deterministic train, validation, and test corpora with provenance, group-safe splits, manifests, hashes, and prompt-leakage checks. Use before teacher labeling, fine-tuning, or comparing models on generated or retrieved examples.
---

# Prepare Training Corpus

Make the corpus reproducible before any expensive labeling or training call.

## Define the contract

Write down:

- the population and approved data sources;
- the unit of an example and the group that must never cross splits;
- target split sizes and distributions;
- input, output, abstention, and identifier schemas;
- required positive, negative, ambiguous, and boundary cases;
- leakage rules for prompts, labels, canonical IDs, and teacher-only metadata.

Separate deterministic scenario generation from teacher labeling. Materialize and validate the entire candidate pool without model calls first.

## Materialize deterministically

1. Pin source snapshots and generator revision.
2. Set and record the random seed.
3. Assign splits by stable group identity, not by individual row.
4. Write a selection manifest before calling a teacher or evaluating a model.
5. Keep opaque request-local identifiers in model-visible inputs when canonical IDs would leak answers.
6. Store teacher/reference fields outside the model prompt.

Do not silently repair generated or teacher-produced rows. Preserve raw failures and derive validated outputs separately.

## Validate and freeze

Use `scripts/build_corpus_manifest.py` for JSONL split invariants:

```sh
python scripts/build_corpus_manifest.py \
  --split train=path/train.jsonl \
  --split validation=path/valid.jsonl \
  --split test=path/test.jsonl \
  --id-field id --group-field deckGroupID \
  --output path/corpus-manifest.json
```

Also run project-specific validators for legality, replay, terminal boundaries, data licenses, and context sufficiency. Fail before labeling if:

- IDs repeat or groups leak across splits;
- requested distributions are wrong;
- prompts contain reference answers or teacher-only information;
- examples rely on unmodeled or unknown state;
- provenance or licenses are incomplete.

Freeze exact JSONL bytes, manifests, source revisions, generator configuration, and SHA-256 hashes. Any schema, prompt, or corpus-membership change creates a new revision and fresh state; never resume incompatible evidence.
