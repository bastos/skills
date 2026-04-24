# RouterOS Configuration Change Workflows

Use this reference before recommending live changes, imports, resets, backups, or rollback.

## Preflight for Live Changes

Run read-only discovery first:

```routeros
/system/resource/print
/system/routerboard/print
/system/package/update/print
/system/identity/print
/interface/print terse
/ip/address/print terse
/ip/route/print terse
/ip/firewall/filter/print terse
/ip/firewall/nat/print terse
```

For management-sensitive changes, also capture the current management path:

```routeros
/ip/service/print
/user/active/print
/tool/mac-server/print
/tool/mac-server/mac-winbox/print
```

## Export vs Backup

Use both when possible:

```routeros
/export terse file=pre-change
/system/backup/save name=pre-change password="REPLACE_WITH_STRONG_BACKUP_PASSWORD"
```

Important distinctions:

- `export` creates readable commands and is useful for review, migration, and partial restore.
- `export` omits user passwords, SSH keys, certificates, Dude, and User Manager databases.
- `/system backup` creates a binary clone that includes sensitive device configuration and MAC-related state. Use it primarily for same-device, same-version restore.
- Encrypt backups and keep the password out of chat logs and tickets.

Avoid `show-sensitive` unless the user explicitly needs it.

## Safe Mode

Use CLI safe mode for risky remote work that may cut off access:

- Press `Ctrl+X` or `F4` in the terminal to enter safe mode.
- Exit normally to keep changes.
- Use `Ctrl+D` to exit without saving changes.
- Keep each safe-mode batch small; RouterOS history has a limited number of actions for rollback tracking.

Safe mode is best for interactive terminal sessions. For non-interactive SSH or imports, design a separate rollback path because automation may not preserve the session behavior you expect.

## Change Ordering

For firewall and management changes:

1. Add allow lists and accept rules first.
2. Verify the allow rule matches the current management source.
3. Add or tighten drop/reject rules after allow rules.
4. Verify services and logs.
5. Remove temporary compatibility rules last.

For bridge, VLAN, and route changes:

1. Create new objects disabled or unused where possible.
2. Add VLAN/interface membership before moving IP services.
3. Add routes before removing old routes.
4. Keep an out-of-band or MAC WinBox recovery path when available.
5. Verify from both router and client side before deleting old config.

## Import Workflow

For generated `.rsc` files:

```routeros
/file/print where name="config.rsc"
import file-name=config.rsc verbose=yes dry-run
import file-name=config.rsc verbose=yes
```

`dry-run` is available only with verbose import on documented RouterOS versions. If the device rejects `dry-run`, stop and validate on a lab device or split the import into smaller manual sections.

Auto-import is triggered by uploading a file ending in `.auto.rsc` through FTP or SFTP. RouterOS writes a matching `.auto.log` file with the result. Use auto-import only when unattended execution is intentional.

## Reset Workflow

Reset commands are destructive and reboot the router:

```routeros
/system/reset-configuration
/system/reset-configuration no-defaults=yes
/system/reset-configuration no-defaults=yes run-after-reset=config.rsc
```

Before reset:

- Save an export and encrypted backup.
- Confirm how you will reconnect after reboot.
- Confirm default credentials for that exact model and RouterOS version.
- Confirm whether a Netinstall-provided initial script will run again after reset.

Do not add `skip-backup=yes` unless the user explicitly wants to skip RouterOS' automatic pre-reset backup.

## Rollback Patterns

Small command rollback:

```routeros
/ip/firewall/filter/remove [find comment="managed: temporary input drop"]
/ip/firewall/address-list/remove [find list="mgmt-allow" comment~"managed:"]
```

Safe-mode rollback:

```text
Press Ctrl+D before leaving safe mode.
```

Export/manual rollback:

1. Compare current config to `pre-change.rsc`.
2. Reapply only the affected section.
3. Avoid blindly importing a full export over a live router unless the target was reset or the diff is fully understood.

Binary backup restore is a same-device recovery path:

```routeros
/system/backup/load name=pre-change.backup password="REPLACE_WITH_BACKUP_PASSWORD"
```

Restoring a backup reboots and may restore old MAC/interface-specific state.
