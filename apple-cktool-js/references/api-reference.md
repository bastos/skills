# CKTool JS API reference

This index reflects the TypeScript declarations in npm release `1.3.2`, inspected on 2026-07-21. Query npm and inspect the installed `.d.ts` files before relying on exact shapes in another release.

## Contents

- [PromisesApi methods](#promisesapi-methods)
- [Core enums](#core-enums)
- [Field factories](#field-factories)
- [Response and error behavior](#response-and-error-behavior)
- [Cancellation](#cancellation)

## PromisesApi methods

### Team and container discovery

| Method | Purpose | Typical auth |
|---|---|---|
| `getTeams` | Fetch teams available to the developer | Management |
| `getContainers` | Fetch/search containers for a team | Management |

### Schema and configuration

| Method | Purpose | Typical auth |
|---|---|---|
| `exportSchema` | Download CloudKit Schema Language text | Management |
| `validateSchema` | Validate an uploaded `.ckdb` file | Management |
| `importSchema` | Apply an uploaded `.ckdb` file | Management |
| `resetToProduction` | Reset an environment's schema/state to production | Management |
| `resetConfigToProduction` | Reset configuration to production | Management |

### Records

| Method | Purpose | Typical auth |
|---|---|---|
| `getRecord` | Fetch one record | User |
| `lookupRecords` | Fetch multiple named records | User |
| `queryRecords` | Query records with filters, sorts, and pagination | User |
| `queryRecordChanges` | Fetch record changes | User |
| `createRecord` | Create one record | User |
| `updateRecord` | Update one record | User |
| `resolveRecord` | Resolve a record conflict | User |
| `deleteRecord` | Delete one record | User |
| `deleteRecordsByQuery` | Dry-run or delete matching records in pages | User |
| `createAssetUploadUrl` | Prepare a CloudKit asset upload | User |

### Zones, sharing, and session

| Method | Purpose | Typical auth |
|---|---|---|
| `getZone` | Fetch one zone | User |
| `getZones` | Fetch zones | User |
| `createZone` | Create a zone | User |
| `deleteZone` | Delete a zone | User |
| `acceptRecord` | Accept a shared record | User |
| `getSessionUser` | Fetch the authenticated session user | User |

Consult the generated operation type for required parameters. Methods accept a single parameter object and return a `CancellablePromise` resolving to a response wrapper.

## Core enums

```typescript
CKEnvironment.DEVELOPMENT
CKEnvironment.PRODUCTION

CKDatabaseType.PUBLIC
CKDatabaseType.PRIVATE
CKDatabaseType.SHARED
```

Query filters in 1.3.2 include:

- `EQUALS`, `NOT_EQUALS`
- `LESS_THAN`, `LESS_THAN_OR_EQUALS`
- `GREATER_THAN`, `GREATER_THAN_OR_EQUALS`
- `NEAR`
- `CONTAINS_ALL_TOKENS`, `CONTAINS_ANY_TOKENS`
- `IN`, `NOT_IN`
- `LIST_CONTAINS`, `LIST_NOT_CONTAINS`
- `LIST_CONTAINS_ANY`, `LIST_NOT_CONTAINS_ANY`
- `LIST_CONTAINS_ALL`, `NOT_LIST_CONTAINS_ALL`
- `BEGINS_WITH`, `NOT_BEGINS_WITH`
- `LIST_MEMBER_BEGINS_WITH`, `NOT_LIST_MEMBER_BEGINS_WITH`

Sort order:

```typescript
CKDBQuerySortOrder.ASC
CKDBQuerySortOrder.DESC
```

Reference actions:

```typescript
CKDBRecordReferenceAction.NONE
CKDBRecordReferenceAction.DELETE_SELF
CKDBRecordReferenceAction.VALIDATE
```

Use `DELETE_SELF` only when the intended CloudKit relationship semantics require it.

## Field factories

`makeRecordFieldValue` aliases `CKRecordFieldValue.make`. Common scalar factories include:

```typescript
makeRecordFieldValue.string(value)
makeRecordFieldValue.int64(value)
makeRecordFieldValue.double(value)
makeRecordFieldValue.timestamp(value)
makeRecordFieldValue.location(value)
makeRecordFieldValue.bytes(value)
makeRecordFieldValue.reference(value)
makeRecordFieldValue.asset(value)
```

List, encrypted, and encrypted-list variants are available. Use editor completion or inspect:

```text
node_modules/@apple/cktool.database/dist/types/field-values/
```

Factory validation can throw before a request when the input type or range is invalid. Use Int64 and double factories instead of relying on untyped JavaScript numbers.

Generated request types brand bounded integers. Convert limits explicitly in strict TypeScript:

```typescript
import { toInt32 } from "@apple/cktool.database";

const resultsLimit = toInt32(200);
```

## Response and error behavior

Successful methods return a response wrapper. Common payload paths include:

```typescript
response.result.record
response.result.records
response.result.continuationToken
```

Schema export returns a blob-like `response.result` that supports `arrayBuffer()`.

CKTool JS exposes generated request, authentication, validation, length, range, fetch, and cancellation errors. Log only a minimal safe message by default:

```typescript
const message = error instanceof Error
  ? `${error.name}: ${error.message}`
  : "CKTool JS request failed with a non-Error value";
console.error(message);
```

Still rethrow or set a nonzero exit status. `configuration.jsonStringify(error, null, 2)` can provide richer diagnostics, but use it only in protected logs after checking the serialized shape and redacting tokens, request headers, and private record fields.

## Cancellation

API methods return `CancellablePromise`, which behaves like a Promise and exposes cancellation:

```typescript
const request = api.queryRecords(params);

// Later, when the surrounding operation is aborted:
request.cancel();
```

Wire cancellation to the caller's abort/lifecycle policy. A canceled client request does not imply rollback of a server mutation that already completed.
