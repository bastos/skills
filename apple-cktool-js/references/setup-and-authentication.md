# Setup and authentication

## Contents

- [Package layout](#package-layout)
- [Version selection](#version-selection)
- [Dependency and type-check health](#dependency-and-type-check-health)
- [Node.js setup](#nodejs-setup)
- [Browser setup](#browser-setup)
- [Security keys](#security-keys)
- [Secret handling](#secret-handling)

## Package layout

CKTool JS is modular:

| Package | Purpose |
|---|---|
| `@apple/cktool.database` | `PromisesApi`, CloudKit models, enums, operations, and field factories |
| `@apple/cktool.target.nodejs` | Node request implementation, `createConfiguration`, `Blob`, and `File` |
| `@apple/cktool.target.browser` | Browser request implementation and `createConfiguration` |

The database package pulls in Apple's core and generated API packages. Do not install those internal packages directly unless a narrowly justified advanced use case requires it.

## Version selection

Check the registry at implementation time:

```bash
npm view @apple/cktool.database version dist-tags --json
npm view @apple/cktool.target.nodejs version dist-tags --json
npm view @apple/cktool.target.browser version dist-tags --json
```

Install matching exact versions for reproducibility, then commit the lockfile:

```bash
CKTOOL_JS_VERSION=$(npm view @apple/cktool.database version)
npm install --save-exact \
  "@apple/cktool.database@$CKTOOL_JS_VERSION" \
  "@apple/cktool.target.nodejs@$CKTOOL_JS_VERSION"
```

Before using the shell snippet in automation, verify the target adapter exposes the same version. A repository may prefer its package manager's native version pinning command.

Apple's sample repository may pin an older release. Treat samples as API-shape guidance, not as proof of the current latest version.

## Dependency and type-check health

Run the consuming repository's security audit and strict type-check after installation:

```bash
npm audit
npm exec tsc -- --noEmit
```

In a clean install of the matching `1.3.2` packages on 2026-07-21:

- npm reported a moderate advisory through CKTool JS's transitive `uuid` dependency;
- the latest TypeScript reported errors inside CKTool JS dependency declarations with `skipLibCheck: false`, including a missing `content-type` declaration and a `bignumber.js` default-type mismatch.

Treat this as a dated prompt to recheck, not as a permanent package assessment. Prefer a patched, matching Apple release when available. If no release fixes an advisory, evaluate whether the affected call path is reachable, keep the automation runner narrowly privileged, and document any temporary risk acceptance. Do not force incompatible transitive versions without compiling and exercising the workflow.

For declaration-only failures, first confirm the errors originate under `node_modules` rather than in application code. Prefer compatible package and TypeScript releases or an upstream fix. A documented `skipLibCheck: true` can be a temporary workaround, but it suppresses checking for all dependency declarations; it does not justify casts or ignored errors in the automation's own source.

## Node.js setup

```typescript
import { PromisesApi } from "@apple/cktool.database";
import { createConfiguration } from "@apple/cktool.target.nodejs";

const configuration = createConfiguration();
const api = new PromisesApi({
  configuration,
  security: {
    ManagementTokenAuth: process.env.CKTOOL_MGMT_TOKEN!,
  },
});
```

Replace the non-null assertion with runtime validation in production scripts. TypeScript's `!` silences the compiler but does not prevent `undefined` at runtime.

The package supports CommonJS examples as well:

```javascript
const { PromisesApi } = require("@apple/cktool.database");
const { createConfiguration } = require("@apple/cktool.target.nodejs");
```

Follow the consuming repository's module system; do not convert the whole project merely for CKTool JS.

## Browser setup

```typescript
import { PromisesApi } from "@apple/cktool.database";
import { createConfiguration } from "@apple/cktool.target.browser";

const configuration = createConfiguration();
const api = new PromisesApi({ configuration });
```

Browser authentication depends on the trusted application and CloudKit access model. Do not insert management or reusable user tokens into source code, HTML, build-time public environment variables, local storage, or downloadable bundles. Use a protected server-side path for management operations.

## Security keys

Use the exact generated scheme names:

```typescript
const security = {
  ManagementTokenAuth: managementToken,
  UserTokenAuth: userToken,
};
```

Do **not** use:

```typescript
const security = {
  managementToken,
  userToken,
};
```

The generated API also defines `CloudKitAPITokenAuth` and `CloudKitWebAuthTokenAuth` for applicable browser/data access flows. Use them only when the surrounding CloudKit authentication design explicitly calls for those schemes; they are not substitutes for a management token on schema operations.

### Token roles

- `ManagementTokenAuth`: team/container discovery and schema management.
- `UserTokenAuth`: database work on behalf of an iCloud user.
- Management tokens do not grant private record-data access.
- User tokens are short-lived and may require interactive reauthentication.

## Secret handling

Use a small runtime guard:

```typescript
function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required environment variable: ${name}`);
  return value;
}
```

Prefer a 1Password Developer Environment, local environment mount, or encrypted CI secrets. Avoid:

- committing token-bearing `.env` files;
- printing `process.env` during debugging;
- logging the `security` object or `PromisesApi` internals;
- passing tokens as CLI arguments to wrapper scripts;
- embedding secrets in source maps or browser bundles.

Keep team ID and container ID separate from credentials. They are identifiers, but still validate them so automation cannot silently hit a wrong container.
