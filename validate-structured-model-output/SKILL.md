---
name: validate-structured-model-output
description: Validates JSON or tool-call model outputs without repair, separating parse, schema, supplied-identifier, semantic, replay, and safety failures. Use for first-attempt benchmarks, teacher-label pipelines, and bounded model tool selection.
---

# Validate Structured Model Output

Treat model output as untrusted input. Preserve raw bytes and validate a normalized copy through ordered gates.

## Validation order

1. **Transport:** A native structured response or the required JSON payload exists.
2. **Parse:** Decode exactly once. In acceptance benchmarks, do not extract JSON from prose or retry malformed output.
3. **Schema:** Enforce required fields, types, controlled values, and cardinality.
4. **Identifiers:** Reject unknown, duplicate, overlapping, invented, or off-request IDs.
5. **Semantics:** Reject equivalent choices where distinctness is required and verify classifications against supplied facts.
6. **Execution:** Replay or otherwise validate the selected operation with the deterministic kernel.
7. **Safety:** Reject continuation through terminal, unresolved, random, hidden, or otherwise unsupported effects.

Keep failure categories separate. A parse failure is not an abstention, and a legal identifier is not proof of a safe or useful result.

## Validate JSONL ID contracts

Use the bundled validator when each row contains supplied, ranked, and optional alternative IDs:

```sh
python scripts/validate_jsonl_outputs.py results.jsonl \
  --supplied-field request.planIDs \
  --ranked-field response.rankedPlanIDs \
  --alternative-field response.alternativePlanIDs \
  --max-ranked 3 --output validation-report.json
```

It checks duplicate IDs within arrays, overlap between ranked and alternatives, unknown IDs, rank length, and alternatives without a ranked selection. Add project validators after this generic layer.

## Benchmark discipline

For first-attempt acceptance, generate once and validate without repair, remediation, or deterministic fallback. Test production remediation separately. Persist raw output, normalized output, every gate result, timing, prompt/config revision, and validator revision so failures remain auditable.
