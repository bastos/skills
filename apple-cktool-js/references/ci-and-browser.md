# CI and browser integration

## Node.js CI pattern

Use Node.js for schema automation and other operations requiring management credentials.

1. Pin matching CKTool JS package versions and commit the lockfile.
2. Inject `CKTOOL_MGMT_TOKEN`, team ID, and container ID through encrypted secrets.
3. Validate all inputs before constructing the workflow target.
4. Force `CKEnvironment.DEVELOPMENT` for pull-request and ordinary test jobs.
5. Serialize reset/import work per container.
6. Rethrow failures or set `process.exitCode = 1`.
7. Export an after-state schema or query after mutations.

Apple's GitHub Action sample uses `CKTOOL_MGMT_TOKEN`, `TEAM_ID`, `CONTAINER_ID`, and an optional `SCHEMA_FILE`. Follow the repository's naming conventions if they already exist, but keep credential names clearly separate from identifiers.

## Avoid false-success jobs

This helper is unsafe for CI because it swallows the error:

```typescript
async function importSchema(): Promise<void> {
  try {
    await api.importSchema(params);
  } catch (error) {
    console.error(error);
  }
}
```

Prefer:

```typescript
async function importSchema(): Promise<void> {
  try {
    await api.importSchema(params);
  } catch (error) {
    const message = error instanceof Error
      ? `${error.name}: ${error.message}`
      : "CKTool JS schema import failed with a non-Error value";
    console.error(message);
    throw error;
  }
}
```

Or let the top-level boundary handle the error once. Reserve `configuration.jsonStringify` for protected diagnostics after reviewing and redacting its output.

## Concurrency and isolation

Reset and import operate on shared server state. Two jobs targeting the same development container can interleave:

```text
job A reset -> job B reset -> job A import -> job B import
```

Prevent this with one or more of:

- a dedicated container per environment or test suite;
- CI concurrency groups keyed by container ID;
- a fixture namespace/run ID when a full reset is unnecessary;
- read-only validation in pull requests and reset/import only on protected branches.

Record cleanup should filter on a unique run identifier and preview batch deletion before applying it.

## Production controls

- Keep production credentials out of pull-request jobs.
- Use environment protection and explicit approval.
- Make the requested environment visible in logs while keeping tokens secret.
- Refuse production by default in code:

  ```typescript
  if (target.environment === CKEnvironment.PRODUCTION && !approvedProductionRun) {
    throw new Error("Production CloudKit operation requires explicit approval");
  }
  ```

- Treat schema deployment as a release action distinct from development import.

## Browser boundary

The browser target provides transport support, not permission to expose secrets.

Never ship:

- `ManagementTokenAuth` in a bundle;
- a reusable `UserTokenAuth` hardcoded at build time;
- tokens in public `NEXT_PUBLIC_*`, `VITE_*`, or similar variables;
- credentials in source maps, local storage, analytics, or client error reports.

For a browser tool:

1. Define the CloudKit web authentication model explicitly.
2. Use only credentials intended for that client flow.
3. Keep management operations server-side.
4. Scope Content Security Policy and allowed origins.
5. Avoid displaying private record payloads in diagnostics.
6. Expire browser sessions and support reauthentication.

If the task is merely to run automation from a non-macOS CI runner, use the Node target, not the browser target.
