# RouterOS Recipes

These are patterns, not universal configs. Adapt interface names, addresses, rule order, and comments to the device.

## Health Snapshot

```routeros
/system/resource/print
/system/routerboard/print
/system/package/update/print
/interface/print terse
/ip/address/print terse
/ip/route/print terse
/ip/dns/cache/print count-only
/log/print where topics~"error|critical|warning"
```

## Idempotent Address-List Entry

```routeros
:local listName "mgmt-allow";
:local entryAddress "203.0.113.10";
:if ([:len [/ip/firewall/address-list/find list=$listName address=$entryAddress]] = 0) do={
    /ip/firewall/address-list/add list=$listName address=$entryAddress comment="managed: admin workstation";
}
```

## Management Allow Before Input Drop

Inspect first:

```routeros
/ip/firewall/filter/print where chain=input
```

Add allow rules before a broad input drop:

```routeros
/ip/firewall/address-list/add list="mgmt-allow" address="203.0.113.10" comment="managed: admin workstation"
/ip/firewall/filter/add chain=input action=accept src-address-list="mgmt-allow" protocol=tcp dst-port=22,8291 comment="managed: allow SSH and WinBox"
```

If there is a known drop rule, place the allow rule before it:

```routeros
/ip/firewall/filter/move [find comment="managed: allow SSH and WinBox"] [find chain=input action=drop]
```

If `[find chain=input action=drop]` returns more than one rule, print the rules and choose the correct anchor.

## Add NAT Masquerade for a WAN Interface

```routeros
:local wan "ether1";
:if ([:len [/ip/firewall/nat/find chain=srcnat action=masquerade out-interface=$wan]] = 0) do={
    /ip/firewall/nat/add chain=srcnat action=masquerade out-interface=$wan comment="managed: WAN masquerade";
}
```

Verify:

```routeros
/ip/firewall/nat/print where comment="managed: WAN masquerade"
```

## Create a Basic Bridge

```routeros
:if ([:len [/interface/bridge/find name="bridge-lan"]] = 0) do={
    /interface/bridge/add name="bridge-lan" protocol-mode=rstp comment="managed: LAN bridge";
}

:foreach iface in={"ether2";"ether3";"ether4"} do={
    :if ([:len [/interface/bridge/port/find bridge="bridge-lan" interface=$iface]] = 0) do={
        /interface/bridge/port/add bridge="bridge-lan" interface=$iface comment="managed: LAN bridge port";
    }
}
```

## Add a VLAN Interface on a Bridge

```routeros
:local vlanId 20;
:local vlanName "vlan20-users";
:local bridgeName "bridge-lan";

:if ([:len [/interface/vlan/find name=$vlanName]] = 0) do={
    /interface/vlan/add name=$vlanName interface=$bridgeName vlan-id=$vlanId comment="managed: users VLAN";
}
```

Bridge VLAN filtering designs are device-specific. Before enabling `vlan-filtering=yes`, inspect:

```routeros
/interface/bridge/print detail
/interface/bridge/port/print detail
/interface/bridge/vlan/print detail
```

## Add a DHCP Client on WAN

```routeros
:local wan "ether1";
:if ([:len [/ip/dhcp-client/find interface=$wan]] = 0) do={
    /ip/dhcp-client/add interface=$wan add-default-route=yes use-peer-dns=no comment="managed: WAN DHCP client";
}
```

## Set DNS Servers

```routeros
/ip/dns/set servers=1.1.1.1,9.9.9.9 allow-remote-requests=yes
/ip/dns/print
```

Only set `allow-remote-requests=yes` when firewall rules prevent open resolver exposure from untrusted networks.

## Create and Run a Script

```routeros
/system/script/add name="managed-log-health" policy=read,test source={
    :log info ("health: " . [/system/resource/get uptime]);
}
/system/script/run managed-log-health
/log/print where message~"health:"
```

Update an existing managed script:

```routeros
/system/script/set [find name="managed-log-health"] source={
    :log info ("health updated: " . [/system/resource/get uptime]);
}
```

## Schedule a Script

```routeros
:if ([:len [/system/scheduler/find name="managed-log-health-hourly"]] = 0) do={
    /system/scheduler/add name="managed-log-health-hourly" interval=1h on-event="/system/script/run managed-log-health" policy=read,test comment="managed: hourly health log";
}
```

Verify:

```routeros
/system/scheduler/print detail where name="managed-log-health-hourly"
/system/script/job/print
/log/print where topics~"script"
```
