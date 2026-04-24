# RouterOS Scripting Reference

Use this reference for `/system script`, Scheduler, Netwatch, mode-button hooks, lease scripts, and `.rsc` automation.

## Script Structure

```routeros
# comments use hash and end at the physical line
{
    :local name "router01";
    :log info ("starting maintenance on " . $name);
}
```

Rules:

- RouterOS has single-line comments only.
- Use `{ ... }` to group commands and control scope.
- A command line ends at newline or `;`.
- A physical line can be joined with trailing `\`, but avoid that in generated code unless RouterOS requires it.
- Use indentation for humans; RouterOS does not require it.

## Variables and Scope

```routeros
:local iface "ether1";
:global persistentFlag true;
:put $iface;
```

- Declare variables before using them.
- Prefer `:local` inside scripts. Use `:global` only for intentional cross-script state.
- Each terminal line is treated as local scope, so a `:local` created on one interactive line is not visible on the next line.
- Variable names are case-sensitive.
- Avoid variable names that collide with RouterOS properties such as `type`, `name`, `address`, or `interface`.
- Quote variable names that contain special characters: `:local "lease-mac"`.

## Conditions and Loops

```routeros
:if ([:len [/ip/address/find interface="bridge-lan"]] = 0) do={
    :log warning "bridge-lan has no IP address";
} else={
    :log info "bridge-lan address exists";
}

:foreach item in=[/ip/firewall/filter/find where comment~"managed:"] do={
    :put [/ip/firewall/filter/get $item comment];
}
```

Common loop forms:

```routeros
:for i from=1 to=5 do={ :put $i }
:local waits 0;
:while (($waits < 30) && ([:len [/interface/find where running=no]] > 0)) do={
    :delay 1s;
    :set waits ($waits + 1);
}
```

Use bounded loops for startup waits so scripts cannot hang forever.

## Functions

RouterOS functions are stored in variables:

```routeros
:global ensureAddressList do={
    :local listName $list;
    :local entryAddress $address;
    :if ([:len [/ip/firewall/address-list/find list=$listName address=$entryAddress]] = 0) do={
        /ip/firewall/address-list/add list=$listName address=$entryAddress comment=$comment;
    }
}

$ensureAddressList list="mgmt-allow" address="203.0.113.10" comment="managed: admin";
```

Avoid passing parameters with the same names as globals. If one function calls another, declare the called global inside the caller.

## Error Handling

Use `:onerror` around commands that may fail and should not abort the whole script:

```routeros
:onerror err in={
    :put [:resolve "example.com"];
} do={
    :log warning ("DNS check failed: " . $err);
}
```

For configuration scripts, fail early when a required object is missing:

```routeros
:local wan [/interface/find where name="wan"];
:if ([:len $wan] = 0) do={
    :error "missing required interface: wan";
}
```

## Script Repository

Scripts live under `/system script`.

```routeros
/system/script/add name="managed-health-check" policy=read,test source={
    :log info "health check started";
    /ping 1.1.1.1 count=3;
}

/system/script/run managed-health-check
/system/script/print detail where name="managed-health-check"
/system/script/job/print
```

Permissions matter:

- Running from CLI usually uses the caller's permissions.
- `use-script-permissions` runs with the script's policy when allowed.
- Scheduler, Netwatch, and other event hooks may run with different permissions.
- Device-mode can disable features needed by scripts on newer RouterOS versions.

## Scheduler Pattern

```routeros
/system/scheduler/add name="managed-nightly-export" interval=1d start-time=03:00:00 on-event={
    /export terse file=("nightly-" . [/system/identity/get name]);
} policy=read,write,test
```

Give scheduled jobs stable names and comments. Include a removal command in rollback instructions:

```routeros
/system/scheduler/remove [find name="managed-nightly-export"]
```

## Import Files

A `.rsc` file can contain console commands and scripts. Keep imports deterministic:

- Use absolute paths.
- Avoid interactive prompts.
- Add required objects before referring to them.
- Put disruptive changes after management allow rules and verification-friendly steps.
- Use startup delays when importing after reset and the script depends on physical interfaces.

Test syntax with import dry-run where supported:

```routeros
import file-name=config.rsc verbose=yes dry-run
```
