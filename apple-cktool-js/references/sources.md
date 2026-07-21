# Official sources and verification notes

## Apple documentation

- [CKTool JS](https://developer.apple.com/documentation/cktooljs/)
- [Integrating CloudKit access into JavaScript automation scripts](https://developer.apple.com/documentation/cktooljs/integrating-cloudkit-access-into-your-javascript-automation-scripts)
- [Automating CloudKit Development](https://developer.apple.com/icloud/cloudkit/automating/)
- [Integrating a Text-Based Schema into Your Workflow](https://developer.apple.com/documentation/cloudkit/integrating_a_text-based_schema_into_your_workflow)

## Apple sessions

- [Meet CKTool JS — WWDC22 10116](https://developer.apple.com/videos/play/wwdc2022/10116/)
- [Automate CloudKit tests with cktool and declarative schema — WWDC21 10118](https://developer.apple.com/videos/play/wwdc2021/10118/)
- [Meet CloudKit Console — WWDC21 10117](https://developer.apple.com/videos/play/wwdc2021/10117/)

## Apple samples

- [CloudKit tooling sample repository](https://github.com/apple/sample-cloudkit-tooling)
- [CKTool JS schema-management sample](https://github.com/apple/sample-cloudkit-tooling/tree/main/CKTool-JS/schema-mgmt)
- [CKTool JS GitHub Action sample](https://github.com/apple/sample-cloudkit-tooling/tree/main/CKTool-JS/github-action)
- [GitHub Action sample README](https://github.com/apple/sample-cloudkit-tooling/blob/main/CKTool-JS/github-action/README.md)
- [Schema-management sample README](https://github.com/apple/sample-cloudkit-tooling/blob/main/CKTool-JS/schema-mgmt/README.md)

## npm packages

- [`@apple/cktool.database`](https://www.npmjs.com/package/@apple/cktool.database)
- [`@apple/cktool.target.nodejs`](https://www.npmjs.com/package/@apple/cktool.target.nodejs)
- [`@apple/cktool.target.browser`](https://www.npmjs.com/package/@apple/cktool.target.browser)

## Verification snapshot

Verified from npm and package declarations on 2026-07-21:

- The latest tag for all three public packages resolved to `1.3.2`.
- `PromisesApi` uses exact security property names `ManagementTokenAuth` and `UserTokenAuth`.
- The public method surface included team/container discovery, schema operations, record CRUD/query, zones, sharing, session user, assets, and cancellation.
- Apple's sample repository still pinned `1.2.341`, so its package version is historical even though its overall workflow remains useful.
- A clean install reported a moderate transitive `uuid` advisory, and full dependency declaration checking exposed `content-type` and `bignumber.js` declaration errors with the latest TypeScript.

Refresh before implementation:

```bash
npm view @apple/cktool.database version dist-tags --json
npm view @apple/cktool.target.nodejs version dist-tags --json
npm view @apple/cktool.target.browser version dist-tags --json
```

Then inspect the installed type declarations under each package's `dist/types` directory. Treat the snapshot as dated evidence, not a promise that `1.3.2` remains latest.
