---
name: apple-cktool
description: Operates Apple's Xcode-bundled `cktool` command-line utility for CloudKit development automation on macOS. Use when Codex needs to run, script, explain, or troubleshoot `xcrun cktool`; manage `.ckdb` schemas with export, validate, import, or reset; discover CloudKit teams; create, query, or delete test records; configure management or user tokens in Keychain or CI; or prepare CloudKit-backed integration tests. For equivalent typed JavaScript or TypeScript automation, use `apple-cktool-js` with this skill.
---

# Apple cktool

Use the stateless `cktool` CLI distributed with Xcode to manage CloudKit schemas and test data from macOS. Keep the target explicit and default all development automation to the development environment.

## Choose the right companion

| Need | Use |
|---|---|
| Shell commands, Xcode schemes, or a macOS runner | This skill |
| TypeScript, Node.js, browser tooling, or non-macOS CI | `apple-cktool-js` |
| A shell wrapper around a few stable commands | This skill |
| Reusable branching logic, typed models, updates, or richer error handling | `apple-cktool-js` |

Use both skills when a repository exposes a simple local `cktool` path and a portable CKTool JS CI path. Keep the same team, container, environment, schema file, and safety policy across both implementations.

## Follow the operating workflow

1. **Inspect the local tool.** Run:

   ```bash
   xcode-select -p
   xcrun --find cktool
   xcrun cktool --version
   xcrun cktool --help
   xcrun cktool help <subcommand>
   ```

   Treat local help as authoritative for the installed Xcode. Use `man cktool` for field formats, token precedence, and examples. Do not assume flags from a different Xcode release.

2. **Resolve the complete target.** Record the team ID, container ID, environment, database type, zone, record type, and schema path that apply. Do not infer a production target from an app bundle identifier. Use `get-teams` when the team ID is unknown.

3. **Select the token class.** Use a management token for team/container discovery and schema operations. Use a user token for record operations on behalf of an iCloud user. Read `references/authentication-and-automation.md` before configuring tokens or CI.

4. **Prepare a reversible command.** Export before schema changes, validate before import, query before a single-record deletion, and use the default dry run before bulk deletion. Treat reset, import, creation, and deletion as remote mutations.

5. **Confirm destructive scope.** Before a destructive operation, state the exact container, environment, database, zone, record type or record name, and expected effect. Require explicit user authorization for production writes, schema reset, or permanent deletion unless that exact operation is already the user's request.

6. **Execute without exposing credentials.** Prefer interactive Keychain storage for local work and environment injection from a secret manager for CI. Never print, paste into logs, commit, or pass a token in a command when a safer mechanism is available.

7. **Verify the result.** Check the exit status, capture structured JSON when the command returns it, re-export a changed schema, or re-query affected records. Report the resolved target and outcome, with tokens redacted.

## Apply safety invariants

- Default to `development`. Treat any `production` record mutation as high impact.
- Remember that `reset-schema` resets the development schema to production **and deletes all development data**.
- Remember that exporting a schema backs up schema text, not record data.
- Do not assume schema import to production is a normal deployment path merely because a local parser accepts an environment value. Apple's documented workflow imports into development and deploys schema to production through the supported CloudKit workflow.
- Run `validate-schema` before `import-schema`; use `import-schema --validate` only when one combined step is appropriate.
- Run `delete-records` with its default `--dry-run true` first. Use `--dry-run false --yes` only after reviewing the match count and filters.
- Prefer `--fields-file` or `--fields-stdin` over large inline JSON. This reduces quoting errors and accidental shell expansion.
- Do not use command-line `--token` in shared shells, process listings, CI logs, or recorded terminal sessions.
- Preserve pagination. If `query-records` returns `continuationToken`, continue until the requested scope is complete and stop on a repeated token.
- Expect indexed-query requirements. A queried or sorted field must have the appropriate CloudKit index; an unfiltered query may require `___recordID` to be Queryable.

## Use common schema recipes

### Export a baseline

```bash
xcrun cktool export-schema \
  --team-id "$TEAM_ID" \
  --container-id "$CONTAINER_ID" \
  --environment development \
  --output-file Schema.ckdb
```

Keep `.ckdb` schema files in version control when the repository uses declarative CloudKit schema management. Review the diff before importing.

### Validate, then import

```bash
xcrun cktool validate-schema \
  --team-id "$TEAM_ID" \
  --container-id "$CONTAINER_ID" \
  --environment development \
  --file Schema.ckdb

xcrun cktool import-schema \
  --team-id "$TEAM_ID" \
  --container-id "$CONTAINER_ID" \
  --environment development \
  --file Schema.ckdb
```

After import, export again and compare the effective schema when exact server state matters.

### Reset test state

```bash
xcrun cktool reset-schema \
  --team-id "$TEAM_ID" \
  --container-id "$CONTAINER_ID"
```

Use this only when deleting all development data is intended. Reapply the tested schema and seed data in a deterministic order before integration tests.

## Use common record recipes

### Query with a bounded result

```bash
xcrun cktool query-records \
  --team-id "$TEAM_ID" \
  --container-id "$CONTAINER_ID" \
  --environment development \
  --database-type public \
  --zone-name _defaultZone \
  --record-type Book \
  --filters "pageCount >= int64Type:1000" \
  --requested-fields title pageCount \
  --limit 50
```

Read `references/records-and-filters.md` before composing field JSON, filters, sorts, assets, pagination, or deletions.

### Create from a file

```bash
xcrun cktool create-record \
  --team-id "$TEAM_ID" \
  --container-id "$CONTAINER_ID" \
  --environment development \
  --database-type public \
  --zone-name _defaultZone \
  --record-type Book \
  --fields-file fixtures/book.json
```

### Preview a bulk deletion

```bash
xcrun cktool delete-records \
  --container-id "$CONTAINER_ID" \
  --environment development \
  --database-type public \
  --zone-name _defaultZone \
  --record-type Book \
  --filters "fixtureRun == stringType:run-123" \
  --dry-run true
```

Do not change the dry run to `false` until the returned count and target are verified.

## Diagnose failures

- If `xcrun` cannot find `cktool`, inspect `xcode-select -p`, verify Xcode 13 or newer is installed, and select the intended Xcode developer directory.
- If authentication fails, verify the operation uses the correct token class and check token expiration or revocation. User tokens are short-lived.
- If a query fails, inspect record type spelling, field types, zone, database, and Queryable/Sortable indexes.
- If JSON parsing fails, move inline fields to a file and validate the JSON separately.
- If the CLI reports usage error 64, re-read `xcrun cktool help <subcommand>` for the installed version.
- If CloudKit rejects a schema, run `validate-schema`, inspect the `.ckdb` diff, and verify the environment/container pair.

## Load references on demand

- Read `references/command-reference.md` for the complete command surface, required flags, exit codes, and examples.
- Read `references/records-and-filters.md` for field JSON, assets, filters, sorts, indexes, pagination, and safe deletion.
- Read `references/authentication-and-automation.md` for token precedence, Keychain, environment variables, Xcode test setup, and CI patterns.
- Read `references/sources.md` for Apple documentation, WWDC sessions, samples, and the verification snapshot.
