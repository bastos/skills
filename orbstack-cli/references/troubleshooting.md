# Troubleshooting

## First stops

```bash
orb doctor              # verify Docker integration is healthy and OrbStack is in control
orb doctor --fix        # auto-fix what it can
orb status              # is OrbStack even running? (0/1/2)
orb top                 # live CPU/mem/disk/net for machines, containers, compose, k8s
orb logs <machine>      # machine boot/unified logs (-a = verbose)
orb logs docker         # Docker engine logs
orb report              # gather a diagnostic bundle (~/.orbstack/diag) for a bug report
```

`orb doctor` only checks the CLI/PATH/context wiring - it reports "all checks
passed" even when the VM's networking is broken. Don't trust a green doctor to
mean the network is fine.

## "Cannot connect to the Docker daemon"

```bash
orb status                       # make sure OrbStack is running; `orb start` if not
docker context use orbstack      # select OrbStack's context
orb doctor --fix                 # or let doctor repair it
```

## Restart just the engine

```bash
orb restart docker      # restart the Docker engine without touching machines
```

Note: a bare `orb stop` (no machine) stops *everything*. Containers without a
restart policy won't come back on their own - `docker start` them after.

## x86 / Rosetta errors in a machine

```bash
sudo dpkg --add-architecture amd64 && sudo apt install libc6:amd64
```

Or run the image with `--platform linux/amd64`. See `references/docker.md`.

## Cloud-init didn't run / machine setup failed

```bash
orb -m <machine> cloud-init status --long
orb -m <machine> cat /var/log/cloud-init-output.log
```

## Published-port "wedge" (connect OK, resets on first data)

A published host port can wedge: TCP connect succeeds but the connection resets
on first data ("Connection reset by peer", or MySQL "Lost connection ... reading
initial communication packet"). The service is healthy *inside* the container
(`docker exec <c> curl localhost:<port>` / a ping works).

- The wedge is **sticky per host-port-number**. It survives `docker restart`,
  `docker compose up --force-recreate`, `orb restart docker`, and even a full
  `orbctl stop && orbctl start`.
- **Fix:** republish the service on a *fresh, never-used* host port (e.g. map
  `3307:3306` instead of `3306:3306`) and point the client at the new port.
  Only that or `orb reset` (factory wipe - avoid) clears it.
- Some images bind loopback-only inside the container (e.g. older Elasticsearch);
  the proxy can't reach those even when not wedged - bind to `0.0.0.0` instead.

## Total route loss to containers (worse than a wedge)

Symptom: *every* path to containers fails, not just published ports. DNS still
resolves (`<svc>.<project>.orb.local` answers) but you get **"No route to host"**
to the container IP, while the service is fine inside the container. Tell-tale:
`orbctl start` prints `start VM: timed out waiting for VM to start` while
`orbctl status` says `Running` and `docker` works - the VM's network interface
never came up.

- `orb doctor`, `bin/cli services` cycles, and `orbctl stop && start` do **not**
  fix this.
- **Fix:** Quit the OrbStack GUI app and reopen it (re-creates the macOS network
  interface/routes), or reboot. Also check for a VPN/firewall (corporate VPN,
  Cloudflare WARP, Little Snitch) eating the `192.168.x.x` route.
- Reach containers by `<service>.<project>.orb.local`, not the bare container
  name (`mycontainer` is NXDOMAIN from the host).

## Factory reset (last resort)

```bash
orb reset               # delete ALL machines + Docker data (config is kept)
orb reset -y            # skip the confirmation prompt
```
