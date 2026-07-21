# Schema workflows

## Contents

- [Target and file setup](#target-and-file-setup)
- [Export](#export)
- [Validate and import](#validate-and-import)
- [Reset and reapply](#reset-and-reapply)
- [CI verification](#ci-verification)

## Target and file setup

Use a management-token API instance and a development target:

```typescript
import { CKEnvironment, PromisesApi } from "@apple/cktool.database";
import { File, createConfiguration } from "@apple/cktool.target.nodejs";
import { readFile, writeFile } from "node:fs/promises";
import { basename } from "node:path";

const configuration = createConfiguration();
const api = new PromisesApi({
  configuration,
  security: {
    ManagementTokenAuth: requireEnv("CKTOOL_MGMT_TOKEN"),
  },
});

const schemaTarget = {
  teamId: requireEnv("CLOUDKIT_TEAM_ID"),
  containerId: requireEnv("CLOUDKIT_CONTAINER_ID"),
  environment: CKEnvironment.DEVELOPMENT,
};

async function schemaFile(path: string): Promise<File> {
  const bytes = await readFile(path);
  return new File([Uint8Array.from(bytes).buffer], basename(path));
}
```

Copy the Node `Buffer` into an `ArrayBuffer` to satisfy current `BlobPart` types. Resolve paths using the repository's stable module or workspace root. Avoid assuming the caller's current working directory in reusable CI actions.

## Export

`exportSchema` returns the schema payload as a blob-like result:

```typescript
async function exportSchema(path: string): Promise<void> {
  const response = await api.exportSchema(schemaTarget);
  const arrayBuffer = await response.result.arrayBuffer();
  await writeFile(path, Buffer.from(arrayBuffer));
}
```

Use export to:

- capture a baseline before mutation;
- compare server state with a checked-in `.ckdb` file;
- verify an import produced the intended schema.

Do not overwrite a repository schema silently. Write to a temporary or explicitly requested path and review the diff.

## Validate and import

```typescript
async function validateAndImport(path: string): Promise<void> {
  const fileForValidation = await schemaFile(path);
  await api.validateSchema({ ...schemaTarget, file: fileForValidation });

  // Create a fresh File so behavior does not depend on reuse of a consumed body.
  const fileForImport = await schemaFile(path);
  await api.importSchema({ ...schemaTarget, file: fileForImport });
}
```

Separate validation and import when logs or approvals need a clear boundary. Validation confirms syntax and importability for the target; it does not make production deployment safe automatically.

## Reset and reapply

`resetToProduction` changes the selected environment to the production baseline. In the documented development workflow, it can delete all development data:

```typescript
async function resetAndApply(path: string): Promise<void> {
  if (schemaTarget.environment !== CKEnvironment.DEVELOPMENT) {
    throw new Error("Refusing to reset a non-development environment");
  }

  await api.resetToProduction(schemaTarget);
  await validateAndImport(path);
}
```

Use an explicit sequence with `await`; do not launch reset and import concurrently. If the production schema is empty, reset may remove all development record types before import.

Only reset when a clean test baseline is intended. A shared development container can be disrupted by another developer or parallel CI job.

## CI verification

A robust schema job should:

1. Validate all required environment variables before any network call.
2. Print the non-secret target identifiers and schema path.
3. Confirm the environment equals `DEVELOPMENT` for reset/import jobs.
4. Validate the schema.
5. Reset only when the workflow contract requires it.
6. Import.
7. Export the effective schema to a temporary artifact.
8. Compare or retain the artifact for diagnostics.
9. Exit nonzero on every API failure.

Example boundary:

```typescript
async function main(): Promise<void> {
  const action = process.argv[2];
  if (action === "validate") {
    await api.validateSchema({
      ...schemaTarget,
      file: await schemaFile("CloudKitSchema.ckdb"),
    });
    return;
  }

  if (action === "reset-and-apply") {
    await resetAndApply("CloudKitSchema.ckdb");
    return;
  }

  throw new Error(`Unsupported action: ${action ?? "<missing>"}`);
}

main().catch((error: unknown) => {
  const message = error instanceof Error
    ? `${error.name}: ${error.message}`
    : "CKTool JS schema workflow failed with a non-Error value";
  console.error(message);
  process.exitCode = 1;
});
```

Do not copy a helper that catches and logs internally without rethrowing; CI may otherwise report success after a failed CloudKit operation. Use `configuration.jsonStringify` only in protected diagnostics after reviewing and redacting the serialized output.
