# Official MikroTik Documentation

Last checked: 2026-04-24.

Use official MikroTik documentation as the source of truth when a command, property, or RouterOS version behavior matters. RouterOS changes over time, so verify current docs for high-risk or version-sensitive work.

## Primary Sources

| Topic | URL | Use for |
|-------|-----|---------|
| MikroTik home | https://mikrotik.com/ | Product and vendor context. |
| RouterOS documentation root | https://help.mikrotik.com/docs/ | Current RouterOS manual and navigation. |
| RouterOS overview | https://help.mikrotik.com/docs/spaces/ROS/pages/328059/RouterOS | Latest-stable RouterOS manual scope and offline docs. |
| Command Line Interface | https://help.mikrotik.com/docs/spaces/ROS/pages/328134/Command+Line+Interface | Terminal navigation, paths, item names/numbers, general commands, completion. |
| Scripting | https://help.mikrotik.com/docs/spaces/ROS/pages/47579229/Scripting | Script syntax, variables, functions, arrays, script repository, permissions. |
| Configuration Management | https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management | Safe mode, exports, imports, auto-import, reset, import troubleshooting. |
| Backup | https://help.mikrotik.com/docs/spaces/ROS/pages/40992852/Backup | Binary backup behavior, same-device restore caveats, encryption. |
| Device-mode | https://help.mikrotik.com/docs/spaces/ROS/pages/93749258/Device-mode | RouterOS v7 feature restrictions such as scheduler, fetch, sniffer, container, proxy. |

## Version Notes

- The RouterOS docs state they apply to the latest stable RouterOS version. Do not assume older v6 devices support v7-only behavior.
- The scripting page checked on 2026-04-24 was updated on 2026-04-15.
- The CLI page checked on 2026-04-24 was updated on 2025-01-03.
- The configuration management page checked on 2026-04-24 documented import `dry-run`, safe mode, and reset behavior.
- Device-mode is relevant for RouterOS v7.17 and later factory defaults. Some features may be disabled by mode.

## Verification Prompts

Ask for or run these read-only commands before version-sensitive work:

```routeros
/system/package/update/print
/system/resource/print
/system/routerboard/print
/system/device-mode/print
```

Use `/system/device-mode/print` when a script, scheduler, fetch, container, proxy, sniffer, traffic generator, or other restricted feature unexpectedly fails.
