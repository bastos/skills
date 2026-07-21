# Records, field JSON, filters, and deletion

Read this reference before generating record fixtures, queries, sorts, pagination loops, or deletion commands.

## Contents

- [Target model](#target-model)
- [Field JSON](#field-json)
- [Assets](#assets)
- [Filters](#filters)
- [Sorts and indexes](#sorts-and-indexes)
- [Pagination](#pagination)
- [Safe deletion](#safe-deletion)

## Target model

A record operation must resolve:

- `container-id`, such as `iCloud.com.example.MyApp`
- `environment`: `development` or `production`
- `database-type`: `public`, `private`, or `shared`
- `zone-name`, defaulting to `_defaultZone`
- `record-type` for creation, query, or bulk deletion
- `record-name` for single deletion

Private and shared data access is performed on behalf of the user represented by the user token. Do not assume the token has access to another user's data.

## Field JSON

Supply fields as a JSON object whose keys are field names and whose values contain a CloudKit field type and value:

```json
{
  "title": { "type": "stringType", "value": "The Mysterious Island" },
  "pageCount": { "type": "int64Type", "value": 1464 },
  "rating": { "type": "doubleType", "value": 4.8 },
  "publishedOn": {
    "type": "timestampType",
    "value": "1875-09-12T21:12:42Z"
  },
  "fixtureRun": { "type": "stringType", "value": "run-123" },
  "tags": { "type": "stringListType", "value": ["fixture", "classic"] }
}
```

Prefer a checked-in fixture file and `--fields-file` for repeatable test data:

```bash
jq empty fixtures/book.json
xcrun cktool create-record \
  --team-id "$TEAM_ID" \
  --container-id "$CONTAINER_ID" \
  --environment development \
  --database-type public \
  --record-type Book \
  --fields-file fixtures/book.json
```

Avoid interpolating untrusted text into `--fields-json`. Build JSON with a real encoder such as `jq` and pass it through standard input or a file.

## Assets

Represent an asset field with an asset key, then map that key to a local path:

```json
{
  "authorImage": { "type": "assetType", "value": "AUTHOR_IMAGE" },
  "covers": {
    "type": "assetListType",
    "value": ["COVER_FRONT", "COVER_BACK"]
  }
}
```

```bash
xcrun cktool create-record \
  --team-id "$TEAM_ID" \
  --container-id "$CONTAINER_ID" \
  --environment development \
  --database-type public \
  --record-type Book \
  --fields-file fixtures/book-with-assets.json \
  --asset-files \
    AUTHOR_IMAGE=fixtures/author.jpg \
    COVER_FRONT=fixtures/front.jpg \
    COVER_BACK=fixtures/back.jpg
```

Verify every asset path exists and is suitable for upload before executing.

## Filters

Write each filter as one shell argument:

```text
FIELD_NAME OPERATOR VALUE
```

Example:

```bash
--filters "pageCount >= 1000" "title == stringType:The Mysterious Island"
```

Common operators supported by the CLI include:

- `==` / `EQUALS`
- `!=` / `NOT_EQUALS`
- `<` / `LESS_THAN`
- `<=` / `LESS_THAN_OR_EQUALS`
- `>` / `GREATER_THAN`
- `>=` / `GREATER_THAN_OR_EQUALS`
- `NEAR`
- `CONTAINS_ALL_TOKENS`
- `CONTAINS_ANY_TOKENS`
- `LIST_CONTAINS_ANY`
- `LIST_NOT_CONTAINS_ANY`

The CLI attempts to infer bare values. Examples from Apple's sample parser include numbers, timestamps, and locations. Make ambiguous values explicit:

```text
stringType:2021-01-01
int64Type:123
doubleType:6.123
```

Quote the complete filter so the shell does not interpret `<`, `>`, spaces, or wildcard-like characters. Verify the exact accepted field types with the installed man page when using references, locations, lists, or timestamps.

## Sorts and indexes

Pass each sort descriptor as its own argument and inspect `man cktool` for the installed syntax. Keep sorting deterministic when paginating, ideally with a stable tie-breaker.

CloudKit queries depend on schema indexes:

- Fields used in filters need a Queryable index.
- Fields used in sorting need a Sortable index.
- An unfiltered query may require `___recordID` to be Queryable.

Do not work around a missing index by broad-fetching production data. Update and deploy the schema intentionally.

## Pagination

`query-records` returns at most the selected limit, defaulting to 200. When the JSON response contains a top-level `continuationToken`:

1. Preserve the exact container, environment, database, zone, record type, filters, requested fields, and sorts.
2. Add `--continuation-token <value>` to the next call.
3. Continue until no continuation token is returned or the user's requested bound is reached.
4. Track seen tokens and stop with an error if CloudKit returns the same continuation token twice.
5. Never print a continuation token unnecessarily in public logs; treat it as transient request state.

Use `jq` to extract fields without losing errors:

```bash
response=$(xcrun cktool query-records ...)
printf '%s\n' "$response" | jq -e '.records // .result.records'
continuation=$(printf '%s\n' "$response" | jq -r '.continuationToken // empty')
```

Adapt the JSON path to the installed tool's actual response. Do not suppress a nonzero `cktool` exit status inside a pipeline.

## Safe deletion

### Single record

1. Query or otherwise resolve the exact `recordName`.
2. Confirm container, environment, database, and zone.
3. Run `delete-record` without `--yes` for interactive local work.
4. Re-query to confirm absence.

### Multiple records

1. Require one or more narrow filters even if the parser permits omission.
2. Run with `--dry-run true`.
3. Record the returned match count.
4. Re-read the exact command and filters.
5. Run with `--dry-run false`; add `--yes` only in an authorized noninteractive flow.
6. Re-run the dry run to confirm zero remaining matches when that is the intended state.

Never bulk-delete production records as a cleanup convenience. Establish an explicit recovery or backup story first.
