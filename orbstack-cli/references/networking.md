# Networking

OrbStack runs a custom virtual network stack: IPv6, ping, traceroute, VPN- and
DNS-aware, up to ~45 Gbps between macOS and containers. For DNS names see
`references/domains.md`; this file covers ports, host access, IP ranges, and
proxies.

## Port forwarding

Containers and VMs expose listening ports on macOS `localhost` automatically.
With Docker you can still publish explicitly:

```bash
docker run --rm -p 80:80 nginx                 # localhost:80
docker run --rm -p 192.168.1.50:80:80 nginx    # bind a specific address
docker run --rm --net=host nginx               # host networking
```

LAN access to published ports is controlled by `docker.expose_ports_to_lan`
(enabled by default). For machines: `machines.expose_ports_to_lan` /
`machines.forward_ports`.

## Reaching the macOS host from a container / VM

```bash
docker run --rm mysql mysql -h host.docker.internal -u root   # from a container
# from a Linux machine: host.orb.internal
```

`localhost` and `host.docker.internal` work bidirectionally with `--net=host`.

## Direct container IPs

Each container has a routable IP (copy it from the OrbStack app, or
`docker inspect`). Connect directly without any mapping:

```bash
curl 192.168.215.2
```

## IP ranges

Default container range is `192.168.x.x` (machine subnet shown by
`orb config get network.subnet4`, e.g. `192.168.138.0/23`). Change container
pools in the Docker engine config (`orb config docker`):

```json
{
  "bip": "198.19.192.1/23",
  "default-address-pools": [
    {"base": "198.19.192.0/19", "size": 23},
    {"base": "198.19.224.0/20", "size": 23}
  ]
}
```

## Proxies

OrbStack follows the macOS system proxy automatically. Override it:

```bash
orb config set network_proxy http://example.com
orb config set network_proxy https://user:password@example.com:8443
orb config set network_proxy socks5://user:password@example.com:1081
orb config set network_proxy socks5h://example.com:1081     # remote DNS
orb config set network_proxy auto                           # follow macOS (default)
orb config set network_proxy none                           # disable

orb config set network.proxy.exclude "example.com,.internal,10.0.0.0/8"
```

## IPv6

Disabled by default. Enable in app settings, or set `"ipv6": true` in the Docker
engine config (`orb config docker`).

## VPN

The stack is compatible with VPNs and advanced DNS resolver settings - no special
config. (If routes to container IPs vanish entirely, see the route-loss note in
`references/troubleshooting.md`.)

## Self-signed registry certificates

OrbStack trusts the macOS keychain. For a private registry, place certs at:

```
~/.docker/certs.d/<registry-host>/ca.crt
~/.docker/certs.d/<registry-host>/client.cert
~/.docker/certs.d/<registry-host>/client.key
```
