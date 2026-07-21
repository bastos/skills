# Official sources and verification notes

Use these sources to refresh behavior when Xcode, CloudKit Console, or the API changes.

## Apple documentation

- [Using cktool](https://developer.apple.com/icloud/ck-tool/)
- [Automating CloudKit Development](https://developer.apple.com/icloud/cloudkit/automating/)
- [CloudKit](https://developer.apple.com/icloud/cloudkit/)
- [Integrating a Text-Based Schema into Your Workflow](https://developer.apple.com/documentation/cloudkit/integrating_a_text-based_schema_into_your_workflow)

## Apple sessions

- [Automate CloudKit tests with cktool and declarative schema — WWDC21 10118](https://developer.apple.com/videos/play/wwdc2021/10118/)
- [Meet CloudKit Console — WWDC21 10117](https://developer.apple.com/videos/play/wwdc2021/10117/)
- [Meet CKTool JS — WWDC22 10116](https://developer.apple.com/videos/play/wwdc2022/10116/)

## Apple samples

- [CloudKit tooling sample repository](https://github.com/apple/sample-cloudkit-tooling)
- [cktool CLI samples](https://github.com/apple/sample-cloudkit-tooling/tree/main/cktool-cli)
- [Schema-management sample](https://github.com/apple/sample-cloudkit-tooling/tree/main/cktool-cli/schema-management)
- [Record-operation sample](https://github.com/apple/sample-cloudkit-tooling/tree/main/cktool-cli/record-operations)
- [Filter syntax sample](https://github.com/apple/sample-cloudkit-tooling/blob/main/cktool-cli/Arguments/Filters.md)

## Local verification snapshot

Verified on 2026-07-21:

- `xcrun --find cktool` resolved inside `/Applications/Xcode.app`.
- `xcrun cktool --version` returned `1.0.23001`.
- The installed command surface contained token save/remove, schema export/import/validate/reset, record create/query/delete, and team discovery.

Refresh with:

```bash
xcrun --find cktool
xcrun cktool --version
xcrun cktool --help
xcrun cktool help <subcommand>
man cktool
```

Treat this snapshot as evidence about the inspected Xcode, not a permanent version guarantee.
