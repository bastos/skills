---
name: apple-cktool-js
description: Builds and troubleshoots CloudKit automation with Apple's CKTool JS packages, including `@apple/cktool.database`, `@apple/cktool.target.nodejs`, and `@apple/cktool.target.browser`. Use when Codex needs typed JavaScript or TypeScript for CloudKit schema import, export, validation, or reset; container and team discovery; record queries, creation, updates, or deletion; Node.js or browser configuration; Promise-based API calls; CI integration; token injection; or migration from `xcrun cktool` shell scripts. Use `apple-cktool` alongside this skill for the Xcode-bundled macOS CLI.
---

# Apple CKTool JS

Use CKTool JS to embed CloudKit Console API operations in JavaScript or TypeScript automation. Prefer TypeScript and Node.js for schema management and CI because they provide strong parameter checks without exposing long-lived credentials to browser bundles.

## Choose the right companion

| Need | Use |
|---|---|
| Typed, reusable automation or non-macOS CI | This skill |
| Browser-targeted CKTool JS integration | This skill, with the browser credential rules |
| One-off shell commands on a Mac | `apple-cktool` |
| Xcode scheme or Run Script integration | Usually `apple-cktool` |

Use both skills when maintaining equivalent local CLI and portable CI paths. Keep CloudKit target identifiers, schema files, token roles, and destructive-operation guards consistent.

## Follow the implementation workflow

1. **Inspect the project.** Determine package manager, module system, TypeScript configuration, Node/browser target, existing environment-variable conventions, and test runner. Reuse the repository's patterns.

2. **Verify package versions.** Query the registry instead of copying versions from an old sample:

   ```bash
   npm view @apple/cktool.database version
   npm view @apple/cktool.target.nodejs version
   npm view @apple/cktool.target.browser version
   ```

   Keep `@apple/cktool.database` and the selected target package on the same exact release when possible. Read `references/setup-and-authentication.md`.

3. **Select one target adapter.** Install `@apple/cktool.target.nodejs` for Node.js or `@apple/cktool.target.browser` for browser execution. Import `createConfiguration` from that adapter.

4. **Resolve the CloudKit target.** Make team ID, container ID, environment, database type, zone, schema path, and record type explicit. Default to `CKEnvironment.DEVELOPMENT`.

5. **Configure exact security keys.** CKTool JS expects `ManagementTokenAuth` and `UserTokenAuth`. Do not invent shorthand keys such as `managementToken` or `userToken`.

6. **Create one `PromisesApi`.** Inject `configuration` and only the credentials required by the operations. Do not log the `security` object.

7. **Implement bounded operations.** Validate before import, preserve query pagination, use field-value factories, pass `recordChangeTag` on updates, and dry-run batch deletion.

8. **Fail clearly.** Catch errors at the process boundary, log a minimal safe message by default, and set a nonzero exit code or rethrow for CI. Use `configuration.jsonStringify` only in protected diagnostics after checking the payload for sensitive data.

9. **Verify remote state.** Re-export schemas or re-query records after mutations. Keep production writes behind explicit authorization and environment protection.

## Initialize Node.js safely

Install the main package and Node adapter:

```bash
npm install @apple/cktool.database @apple/cktool.target.nodejs
```

Use a strict environment reader so a missing value fails before any request:

```typescript
import {
  CKEnvironment,
  PromisesApi,
} from "@apple/cktool.database";
import { createConfiguration } from "@apple/cktool.target.nodejs";

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required environment variable: ${name}`);
  return value;
}

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
```

Add `UserTokenAuth` only when record operations need it. Prefer a 1Password Developer Environment, local environment mount, or CI secret injection. Never commit `.env` credentials.

## Protect browser builds

Install the browser adapter only for browser execution:

```bash
npm install @apple/cktool.database @apple/cktool.target.browser
```

Import `createConfiguration` from `@apple/cktool.target.browser`. Never bundle a management token or reusable user token into public JavaScript. Use Node.js or a protected server-side service for schema operations. Read `references/ci-and-browser.md` before implementing browser authentication.

## Map tasks to methods

| Task | `PromisesApi` method | Token |
|---|---|---|
| List teams / containers | `getTeams`, `getContainers` | Management |
| Export / validate / import schema | `exportSchema`, `validateSchema`, `importSchema` | Management |
| Reset development state | `resetToProduction` | Management |
| Query or fetch records | `queryRecords`, `getRecord`, `lookupRecords` | User |
| Create or update a record | `createRecord`, `updateRecord` | User |
| Delete records | `deleteRecord`, `deleteRecordsByQuery` | User |
| Manage zones | `getZone`, `getZones`, `createZone`, `deleteZone` | User |

Read `references/api-reference.md` for the complete method and enum index.

## Apply schema changes

Use `File` from the target adapter for schema upload:

```typescript
import { readFile } from "node:fs/promises";
import { File } from "@apple/cktool.target.nodejs";

const bytes = await readFile("CloudKitSchema.ckdb");
const schemaBytes = Uint8Array.from(bytes).buffer;
const schemaFile = () => new File([schemaBytes], "CloudKitSchema.ckdb");

await api.validateSchema({ ...schemaTarget, file: schemaFile() });
await api.importSchema({ ...schemaTarget, file: schemaFile() });
```

Read `references/schema-workflows.md` for export, validation, reset/import ordering, file handling, and verification.

## Query and mutate records

Use exact enum values and field-value factories:

```typescript
import {
  CKDatabaseType,
  CKDBQueryFilterType,
  makeRecordFieldValue,
  toInt32,
} from "@apple/cktool.database";

const databaseTarget = {
  containerId: requireEnv("CLOUDKIT_CONTAINER_ID"),
  environment: CKEnvironment.DEVELOPMENT,
  databaseType: CKDatabaseType.PUBLIC,
  zoneName: "_defaultZone",
};

const response = await api.queryRecords({
  ...databaseTarget,
  body: {
    query: {
      recordType: "Book",
      filters: [{
        fieldName: "fixtureRun",
        fieldValue: makeRecordFieldValue.string("run-123"),
        type: CKDBQueryFilterType.EQUALS,
      }],
    },
    resultsLimit: toInt32(50),
  },
});

const records = response.result.records;
```

Match the factory to the CloudKit field's real type; the string example above assumes `fixtureRun` is a string field. Read `references/record-workflows.md` for typed field factories, queries, pagination, optimistic updates, assets, and deletion.

## Handle errors at the boundary

```typescript
async function main(): Promise<void> {
  // Run the requested workflow.
}

main().catch((error: unknown) => {
  const message = error instanceof Error
    ? `${error.name}: ${error.message}`
    : "CKTool JS request failed with a non-Error value";
  console.error(message);
  process.exitCode = 1;
});
```

Do not catch and merely print errors inside helpers used by CI; that can produce a false-success exit status. Do not serialize the API instance, configuration headers, environment, security object, or private record payloads into shared logs.

## Apply safety invariants

- Default to development and require explicit authorization for production writes.
- Remember that resetting to production state can delete all development records.
- Validate a `.ckdb` file before importing it.
- Do not put schema-management credentials in browser bundles.
- Use `recordChangeTag` for normal updates; use `force: true` only when intentionally overriding optimistic concurrency.
- Set `dryRun: true` for `deleteRecordsByQuery` first and verify the count/continuation before deletion.
- Continue paginated queries and batch deletions deliberately, and reject repeated continuation tokens; CKTool JS does not make a multi-page operation atomic.
- Avoid hardcoding the version from Apple's older sample repository. Verify registry versions and inspect installed `.d.ts` declarations when exact types matter.
- Use `containerId`, not `containerID`, in API parameter objects.

## Load references on demand

- Read `references/setup-and-authentication.md` for packages, Node/browser adapters, exact security keys, environment validation, and secret handling.
- Read `references/schema-workflows.md` for export, validate, import, reset, and schema CI examples.
- Read `references/record-workflows.md` for queries, field values, create/update/delete, assets, and pagination.
- Read `references/api-reference.md` for methods, enums, response shapes, cancellation, and error types.
- Read `references/ci-and-browser.md` for process failure, GitHub Actions-style setup, concurrency, and browser credential boundaries.
- Read `references/sources.md` for Apple documentation, packages, samples, and the version snapshot.
