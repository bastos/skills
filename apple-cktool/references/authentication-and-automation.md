# Authentication and automation

## Token roles

| Token | Scope and purpose | Typical commands |
|---|---|---|
| Management | Long-lived; tied to the developer/team context; no record-data access | `get-teams`, schema export/validate/import/reset |
| User | Short-lived; represents an iCloud user; accesses public/private/shared records as that user | create/query/delete records |

Generate tokens in CloudKit Console. A token may only be shown once, may expire, and may be revoked. Do not store either token in source control.

## Credential lookup and precedence

The local man page documents this effective order:

1. Explicit `--token`
2. Environment variable
3. File store at `~/.config/cktool`
4. Login Keychain

Schema commands read `CLOUDKIT_MANAGEMENT_TOKEN`. Record commands read `CLOUDKIT_USER_TOKEN`.

Avoid the explicit command-line token because it can appear in shell history, process inspection, terminal recordings, and CI logs.

## Local development

Prefer the secure interactive flow, which avoids placing the token in the command:

```bash
xcrun cktool save-token --type management
xcrun cktool save-token --type user
```

Keychain is the default. Use file storage only when its weaker plaintext/file-access properties are understood:

```bash
xcrun cktool save-token --type management --method file
```

Remove obsolete credentials from the same store:

```bash
xcrun cktool remove-token --type management
xcrun cktool remove-token --type user
```

## CI and secret managers

Inject tokens only for the process that needs them. Prefer a 1Password Developer Environment, a local environment mount, or the CI provider's encrypted secret mechanism. Do not create a committed `.env` file.

Example shape:

```bash
CLOUDKIT_MANAGEMENT_TOKEN="$INJECTED_MANAGEMENT_TOKEN" \
  xcrun cktool validate-schema \
    --team-id "$TEAM_ID" \
    --container-id "$CONTAINER_ID" \
    --environment development \
    --file Schema.ckdb
```

Do not enable shell tracing (`set -x`) around secret injection. Redact environment dumps and command diagnostics.

Use a user token cautiously in CI: Apple documents user tokens as short-lived and interactively generated, which limits unattended data workflows. Design tests to fail clearly when reauthentication is required.

## Xcode integration-test setup

A deterministic development test pipeline commonly performs:

1. Select the expected Xcode and verify `cktool`.
2. Reset the development schema to production when a clean baseline is truly required.
3. Validate the repository's `.ckdb` file.
4. Import the schema into development.
5. Seed uniquely identifiable test records.
6. Run integration tests.
7. Delete only records labeled for that test run, or reset the isolated development container when authorized.

Prefer a dedicated development container or test namespace. Parallel jobs can race when they reset or seed the same container.

When adding a Run Script build phase or scheme pre-action:

- Resolve paths from stable project variables rather than the caller's current directory.
- Quote every path and identifier.
- Make a `cktool` failure stop the test run.
- Never echo tokens.
- Avoid resetting a shared container on every developer build.

## Production controls

- Keep production writes out of default CI branches and pull-request jobs.
- Require environment protection and explicit approval for a production record mutation.
- Log target identifiers and operation metadata, never credentials or private record contents.
- Prefer read-only verification and bounded queries.
- Treat schema deployment to production as a separate release action from development schema import.

## Authentication troubleshooting

- Management operation rejected: verify a management token is injected and the account belongs to the target team.
- Record operation rejected: verify a current user token and access to the selected container/database/zone.
- Works locally but not in CI: confirm the CI shell receives the environment variable and tracing does not redact it into an empty value.
- Wrong account behavior: remove stale tokens from the selected store and save the intended token again.
- Intermittent user-token failures: expect expiration and create a clear reauthentication path instead of retrying indefinitely.
