# cktool command reference

Use the installed tool's help as the source of truth:

```bash
xcrun cktool --help
xcrun cktool help <subcommand>
man cktool
```

This reference reflects `cktool 1.0.23001`, observed with Xcode on 2026-07-21. Recheck flags before generating automation for another Xcode version.

## Contents

- [Global behavior](#global-behavior)
- [Token storage](#token-storage)
- [Schema commands](#schema-commands)
- [Record commands](#record-commands)
- [Team discovery](#team-discovery)
- [Exit status](#exit-status)

## Global behavior

Invoke the tool through `xcrun` so the active Xcode toolchain selects the binary:

```bash
xcrun cktool <subcommand> [options]
```

The command is stateless from the CloudKit server's perspective: each operation becomes a request to the CloudKit API. Local state is limited to optional credential storage.

| Command | Authorization | Mutates remote state |
|---|---|---|
| `save-token` / `remove-token` | None | No; changes local credential storage |
| `get-teams` | Management | No |
| `export-schema` | Management | No |
| `validate-schema` | Management | No |
| `import-schema` | Management | Yes |
| `reset-schema` | Management | Yes; deletes development data |
| `query-records` | User | No |
| `create-record` | User | Yes |
| `delete-record` / `delete-records` | User | Yes |

## Token storage

### `save-token`

```text
cktool save-token [<token>] [--type <management|user>]
                  [--method <file|keychain>] [--force]
```

- Omit `<token>` to enter it through the secure interactive prompt.
- Default storage is the login Keychain.
- File storage uses `~/.config/cktool`.
- Use `--force` only when intentionally replacing an existing token.

Preferred local setup:

```bash
xcrun cktool save-token --type management
xcrun cktool save-token --type user
```

### `remove-token`

```text
cktool remove-token --type <management|user>
                    [--method <file|keychain>] [--force]
```

Match `--method` to the store used by `save-token`.

## Schema commands

### `export-schema`

```text
cktool export-schema [--token <token>]
  --team-id <team-id>
  --container-id <container-id>
  --environment <development|production>
  [--output-file <path>]
```

Without `--output-file`, the schema is written to standard output. Prefer an explicit file when the output will be diffed or committed.

```bash
xcrun cktool export-schema \
  --team-id WWDRTEAMID \
  --container-id iCloud.com.example.MyApp \
  --environment development \
  --output-file CloudKitSchema.ckdb
```

### `validate-schema`

```text
cktool validate-schema [--token <token>]
  --team-id <team-id>
  --container-id <container-id>
  --environment <development|production>
  --file <path>
```

Validation checks schema syntax and whether the schema can be imported into the target container/environment. It does not mutate the schema.

### `import-schema`

```text
cktool import-schema [--token <token>]
  --team-id <team-id>
  --container-id <container-id>
  --environment <development|production>
  [--validate]
  --file <path>
```

Apple's documented automation flow imports into development. Prefer a separate `validate-schema` call when logs should clearly distinguish validation from mutation.

```bash
xcrun cktool import-schema \
  --team-id WWDRTEAMID \
  --container-id iCloud.com.example.MyApp \
  --environment development \
  --validate \
  --file CloudKitSchema.ckdb
```

### `reset-schema`

```text
cktool reset-schema [--token <token>]
  --team-id <team-id>
  --container-id <container-id>
```

This command always targets the development environment, resets its schema to match production, and deletes all data in development. If no schema exists in production, the resulting development schema may be empty.

## Record commands

Record commands require a user token. Database type values are `public`, `private`, or `shared`. Zone defaults to `_defaultZone` where the command permits omission.

### `create-record`

```text
cktool create-record [--token <token>]
  --team-id <team-id>
  --container-id <container-id>
  --environment <development|production>
  --database-type <public|private|shared>
  [--zone-name <zone>]
  --record-type <record-type>
  [--fields-file <path>]
  [--fields-json <json>]
  [--fields-stdin]
  [--asset-files <KEY=path> ...]
```

Use exactly one convenient field-input route. Asset values in the JSON refer to keys supplied by `--asset-files`.

### `query-records`

```text
cktool query-records [--token <token>]
  --team-id <team-id>
  --container-id <container-id>
  --environment <development|production>
  --database-type <public|private|shared>
  [--zone-name <zone>]
  --record-type <record-type>
  [--filters <filter> ...]
  [--sort-by <sort> ...]
  [--requested-fields <field> ...]
  [--limit <1...>]
  [--continuation-token <token>]
```

The default page limit is 200. When more records match, read the top-level `continuationToken` and pass it to the next query with the same target, filters, and sort order.

### `delete-record`

```text
cktool delete-record [--token <token>]
  --container-id <container-id>
  --environment <development|production>
  --database-type <public|private|shared>
  [--zone-name <zone>]
  --record-name <record-name>
  [--yes]
```

The installed command does not accept `--team-id`. Query the record first and preserve the interactive confirmation unless noninteractive deletion is explicitly intended.

### `delete-records`

```text
cktool delete-records [--token <token>]
  --container-id <container-id>
  --environment <development|production>
  --database-type <public|private|shared>
  [--zone-name <zone>]
  --record-type <record-type>
  [--filters <filter> ...]
  [--dry-run <true|false>]
  [--yes]
```

The default is `--dry-run true`, which returns how many records match. Always run the preview first. Repeat filters exactly when changing to `--dry-run false`.

## Team discovery

### `get-teams`

```text
cktool get-teams [--token <token>]
```

This returns the teams available to the management-token owner. Parse the returned identifier rather than matching only on a display name when scripting.

## Exit status

| Code | Meaning |
|---|---|
| `0` | Operation completed successfully |
| `1` | Operational error |
| `64` | Incorrect invocation / usage error |

Invoking help is successful and exits with `0`. Do not treat a zero exit code as proof that the intended remote state is correct; verify by export or query after mutations.
