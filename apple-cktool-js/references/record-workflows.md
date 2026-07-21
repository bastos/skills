# Record workflows

## Contents

- [Database target](#database-target)
- [Field-value factories](#field-value-factories)
- [Query and pagination](#query-and-pagination)
- [Create](#create)
- [Update](#update)
- [Delete](#delete)
- [Assets](#assets)

## Database target

Record operations use a user token and do not take `teamId` in their request path:

```typescript
import {
  CKDatabaseType,
  CKEnvironment,
  PromisesApi,
} from "@apple/cktool.database";
import { createConfiguration } from "@apple/cktool.target.nodejs";

const configuration = createConfiguration();
const api = new PromisesApi({
  configuration,
  security: {
    UserTokenAuth: requireEnv("CKTOOL_USER_TOKEN"),
  },
});

const databaseTarget = {
  containerId: requireEnv("CLOUDKIT_CONTAINER_ID"),
  environment: CKEnvironment.DEVELOPMENT,
  databaseType: CKDatabaseType.PUBLIC,
  zoneName: "_defaultZone",
};
```

Use `containerId` with a lowercase `d`. Verify the private/shared database and zone are accessible to the token's iCloud user.

## Field-value factories

Use `makeRecordFieldValue` instead of hand-building wire dictionaries:

```typescript
import {
  CKDBRecordReferenceAction,
  makeRecordFieldValue,
} from "@apple/cktool.database";

const fields = {
  title: makeRecordFieldValue.string("The Mysterious Island"),
  pageCount: makeRecordFieldValue.int64(1464),
  rating: makeRecordFieldValue.double(4.8),
  publishedOn: makeRecordFieldValue.timestamp(new Date("1875-09-12T21:12:42Z")),
  author: makeRecordFieldValue.reference({
    recordName: "AUTHOR_RECORD_NAME",
    action: CKDBRecordReferenceAction.NONE,
  }),
};
```

Factories validate types and numeric ranges before sending. Available groups include scalar and list variants for strings, Int64, doubles, timestamps, locations, bytes, references, and assets, plus encrypted variants where CloudKit supports them. Inspect the installed TypeScript declarations for the exact version.

## Query and pagination

```typescript
import {
  type CKDBQueryRecordsRequestBody,
  CKDBQueryFilterType,
  CKDBQuerySortOrder,
  makeRecordFieldValue,
  toInt32,
} from "@apple/cktool.database";

async function queryAllTestBooks() {
  const records = [];
  let continuationToken: string | undefined;
  const seenContinuationTokens = new Set<string>();

  do {
    const body: CKDBQueryRecordsRequestBody = {
      query: {
        recordType: "Book",
        filters: [{
          fieldName: "fixtureRun",
          fieldValue: makeRecordFieldValue.string("run-123"),
          type: CKDBQueryFilterType.EQUALS,
        }],
        sorts: [{
          fieldName: "title",
          order: CKDBQuerySortOrder.ASC,
        }],
      },
      requestedFields: ["title", "fixtureRun"],
      resultsLimit: toInt32(200),
    };

    // With exactOptionalPropertyTypes, omit the property until a token exists.
    if (continuationToken !== undefined) {
      body.continuationToken = continuationToken;
    }

    const response = await api.queryRecords({
      ...databaseTarget,
      body,
    });

    records.push(...response.result.records);

    const nextToken = response.result.continuationToken;
    if (nextToken && seenContinuationTokens.has(nextToken)) {
      throw new Error("CloudKit returned a repeated continuation token");
    }
    if (nextToken) seenContinuationTokens.add(nextToken);
    continuationToken = nextToken;
  } while (continuationToken !== undefined);

  return records;
}
```

Adapt the continuation-token response path to the installed declaration if it differs. Keep the query stable between pages. Query and sort fields require matching CloudKit schema indexes.

## Create

```typescript
const response = await api.createRecord({
  ...databaseTarget,
  body: {
    recordType: "Book",
    fields: {
      title: makeRecordFieldValue.string("The Mysterious Island"),
      fixtureRun: makeRecordFieldValue.string("run-123"),
    },
  },
});

const created = response.result.record;
```

Omit `recordName` to let the server assign a UUID, or supply a deterministic unique name when the fixture strategy explicitly requires idempotency.

## Update

Use the server `recordChangeTag` for optimistic concurrency:

```typescript
const response = await api.updateRecord({
  ...databaseTarget,
  recordName: created.recordName,
  body: {
    recordType: "Book",
    recordChangeTag: created.recordChangeTag,
    fields: {
      title: makeRecordFieldValue.string("The Mysterious Island — Updated"),
      fixtureRun: makeRecordFieldValue.string("run-123"),
    },
  },
});
```

Refetch and reconcile on a change-tag conflict. Avoid `force: true` unless overwriting concurrent changes is intentional and explicitly authorized.

## Delete

Single record:

```typescript
await api.deleteRecord({
  ...databaseTarget,
  recordName: created.recordName,
});
```

Batch preview:

```typescript
const preview = await api.deleteRecordsByQuery({
  ...databaseTarget,
  body: {
    recordType: "Book",
    filters: [{
      fieldName: "fixtureRun",
      fieldValue: makeRecordFieldValue.string("run-123"),
      type: CKDBQueryFilterType.EQUALS,
    }],
    dryRun: true,
    resultsLimit: toInt32(200),
  },
});
```

Review the count and continuation behavior before repeating with `dryRun: false`. Batch deletion is limited to 200 records per operation; use the returned continuation token deliberately. Re-query after deletion.

## Assets

CKTool JS record bodies cannot upload arbitrary local files inline. For asset fields:

1. Call `createAssetUploadUrl` with the asset metadata.
2. Upload bytes to the returned URL as required by CloudKit.
3. Build the asset field value with the returned asset information.
4. Call `createRecord` or `updateRecord`.

Do not improvise the upload protocol. Read the installed declarations and current Apple documentation because asset request/response fields are version-sensitive.
