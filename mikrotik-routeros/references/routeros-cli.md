# RouterOS CLI Reference

Use this reference when generating terminal commands, SSH one-liners, or `.rsc` imports.

## Command Syntax

RouterOS command lines follow this shape:

```routeros
[prefix] [path] command [unnamed-parameter] [param=value] ...
```

Practical rules:

- `:` starts scripting/global commands such as `:local`, `:if`, `:log`, and `:put`.
- `/` starts an absolute menu path from the root.
- Menu words can be separated by spaces or slashes. Prefer slashes in generated instructions: `/ip/firewall/filter/print`.
- End commands with a newline or `;`. Use semicolons inside one-line scripts when needed.
- Do not put whitespace around `param=value`, `from=`, `to=`, `step=`, `in=`, `do=`, or `else=`.

## Navigation

```routeros
/ip/route/print          # absolute path
/                       # return to root in an interactive terminal
..                      # move one menu level up
/ping 10.0.0.1          # run a root command from another menu
```

Generated automation should use absolute paths so it does not depend on the operator's current prompt.

## General Commands

Most configurable menus support:

| Command | Purpose |
|---------|---------|
| `print` | Show items or status. |
| `add` | Create an item. |
| `set` | Change an item. |
| `remove` | Delete an item. |
| `find` | Return internal IDs matching a filter. |
| `get` | Return one property from one item. |
| `enable` / `disable` | Toggle items. |
| `comment` | Set comments. |
| `move` | Reorder list items. |
| `export` | Emit configuration commands. |

Useful print forms:

```routeros
/interface/print terse
/ip/address/print detail
/ip/firewall/filter/print stats
/ip/route/print where dst-address=0.0.0.0/0
/interface/print count-only
```

## Item Targeting

Prefer stable names and filters over printed numbers.

Good:

```routeros
/interface/set [find default-name=ether1] name=wan
/ip/address/set [find interface=bridge-lan] disabled=no
/ip/firewall/filter/disable [find comment="managed: temporary rule"]
```

Avoid:

```routeros
/ip/firewall/filter/remove 3
```

Printed numbers are assigned by the CLI session and can change after another `print` or concurrent edit. They are acceptable for interactive troubleshooting only after showing the relevant `print` output.

When using `set [find ...]`, make sure the filter matches exactly one item. If unsure, first show:

```routeros
/ip/firewall/filter/print where comment="managed: input allow"
```

## Quoting

- Quote strings with spaces: `comment="allow admin SSH"`.
- Quote comments and generated labels consistently; comments make future edits safer.
- Escape `$` inside a script stored as a RouterOS string, because `$` otherwise expands during the outer command.
- For shell SSH examples, single-quote the RouterOS command and use double quotes inside RouterOS:

```bash
ssh admin@192.0.2.1 '/ip/firewall/address-list/print where list="mgmt-allow"'
```

If the RouterOS script itself needs single quotes or complex quoting, write it as a `.rsc` file and import it instead of building an unreadable SSH one-liner.

## Completion and Abbreviations

RouterOS accepts unambiguous abbreviations and offers tab completion interactively. Generated instructions should avoid abbreviations so they are readable and portable.

## Common Read-Only Discovery

```routeros
/system/resource/print
/system/routerboard/print
/system/package/update/print
/interface/print terse
/ip/address/print terse
/ip/route/print terse
/ip/dns/print
/ip/firewall/filter/print terse
/ip/firewall/nat/print terse
/log/print where topics~"error|critical|warning"
```

## Remote Execution

For one-off read-only checks:

```bash
ssh admin@router.example '/system/resource/print'
```

For multi-line changes:

1. Save commands in a `.rsc` file.
2. Upload with SFTP or paste into the terminal.
3. Run `import file-name=name.rsc verbose=yes dry-run` when supported.
4. Run the import without `dry-run` only after the dry run is clean.

Avoid sending long high-risk changes as a single SSH command; diagnostics and rollback are poor if the connection drops.
