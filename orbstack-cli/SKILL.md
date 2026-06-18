---
name: orbstack-cli
description: >-
  Command reference and recipes for driving OrbStack from the terminal on macOS:
  the orb/orbctl CLI for Linux VMs (create, start/stop, exec, file transfer,
  clone, export/import, per-VM CPU/memory limits), Docker under OrbStack
  (contexts, platform/Rosetta, volume extension commands, migrate from Docker
  Desktop, debug shell), container domains (.orb.local) and networking
  (port-forwarding, host.docker.internal, proxies, IP ranges), SSH access,
  Kubernetes, every config key, and headless/CI automation. Use whenever the
  user runs or asks about an `orb`, `orbctl`, or OrbStack-flavored `docker`
  command, manages OrbStack Linux machines, runs containers locally on a Mac,
  sets up .orb.local domains or port-forwarding, scripts OrbStack in CI, or hits
  an OrbStack networking/daemon problem - even phrased loosely as "spin up an
  ubuntu VM", "my container isn't reachable on localhost", "use Docker on my
  Mac", or "OrbStack keeps resetting the connection".
---

# OrbStack CLI

OrbStack is a fast Docker + Linux VM runtime for macOS (a Docker Desktop
replacement). You drive it from the terminal with four commands. This skill is
the **command index and recipe book**; read the matching `references/` file when
you need full flags or detail.

## Which command do I use?

| Command | Use it for |
|---------|-----------|
| `orb` (no args) | Open a shell in the **default** Linux machine |
| `orb <cmd> [args]` | Run `<cmd>` **inside** the default Linux machine (e.g. `orb uname -a`) |
| `orb <subcommand>` / `orbctl <subcommand>` | **Manage** OrbStack and its machines (create, start, config, logs...) |
| `docker` / `docker compose` / `kubectl` | Build/run containers and Kubernetes - run these straight from macOS, no VM needed |
| `mac <cmd>` | Run a **macOS** command from *inside* a Linux machine (e.g. `mac open`, `mac notify`) |

`orb` and `orbctl` are the same binary: `orb foo` runs `foo` in Linux, but
`orb create`/`orb start`/etc. (any known subcommand) manage OrbStack. When a name
could collide, prefer `orbctl <subcommand>` to be explicit.

## Cheat sheet (most common)

```bash
# Machines
orb create ubuntu                       # newest Ubuntu, VM named "ubuntu"
orb create ubuntu:24.04 dev             # specific version + name
orb list                                # list machines + status
orb                                     # shell into default machine
orb -m dev -u root apt update           # run a command in "dev" as root
orb push ~/file.txt code/               # copy Mac -> Linux (~/code/)
orb pull code/out.log .                 # copy Linux -> Mac
orb stop dev / orb start dev / orb delete dev

# Docker (just use docker; OrbStack is the "orbstack" context)
docker run -p 80:80 nginx               # then visit http://localhost
docker run -l dev.orbstack.domains=app.local nginx   # custom domain

# Kubernetes
orb start k8s && kubectl get pods -A

# Service control / health
orb status                              # Running=0, Stopped=1, Starting=2
orb doctor --fix                        # verify + repair Docker integration
orb restart docker                      # restart just the Docker engine

# Config (see `orb config show` for all keys)
orb config set memory_mib 8192
orb config set cpu 4
```

## Key facts you can rely on

- **Auto port-forwarding:** a server listening inside a container or VM is
  reachable on the same port on macOS `localhost` - no `-p` needed for VMs, and
  containers are *also* reachable by domain without any mapping.
- **Domains:** every container is at `<name>.orb.local`; compose services at
  `<svc>.<project>.orb.local`; VMs at `<machine>.orb.local`. All get zero-config
  HTTPS. Visit `https://orb.local` for an index of running containers. → `references/domains.md`
- **Docker context** is named `orbstack` and is selected automatically. If
  `docker` says "cannot connect to the daemon": `docker context use orbstack`
  or `orb doctor --fix`. → `references/docker.md`
- **File paths:** Linux files from macOS at `~/OrbStack/<machine>/`; macOS files
  from Linux at `/mnt/mac/...`; Docker volumes at `~/OrbStack/docker/volumes/`.
- **Exit codes** make `orb` scriptable: `orb status` (0/1/2), `orb update -c`
  (0 = current, 3 = outdated). → `references/headless.md`

## Full command index

Every `orbctl`/`orb` subcommand. Read the linked reference for flags + examples.

| Subcommand | What it does | Reference |
|-----------|--------------|-----------|
| `create` | Create a Linux machine (distro\[:version] \[name]) | machines.md |
| `list` / `info` | List machines / show one machine's details (`-f json`) | machines.md |
| `default` | Get or set the default machine | machines.md |
| `start` / `stop` / `restart` | Start/stop/restart machine(s); bare `orb stop` stops **all** of OrbStack | machines.md |
| `delete` | Permanently delete machine(s) (`-a` all, `-f` force) | machines.md |
| `clone` / `rename` | Copy / rename a machine | machines.md |
| `export` / `import` | Save a machine to / restore from a `.tar.zst` | machines.md |
| `run` (alias `exec`/`shell`) | Run a command in a machine (`-m`, `-u`, `-w`, `ORBENV`) | machines.md |
| `push` / `pull` | Copy files Mac↔Linux | machines.md |
| `logs` | Unified machine logs (`-a` for all/debug) | machines.md, troubleshooting.md |
| `ssh` | Print SSH connection details | ssh.md |
| `usb` / `serial` | USB passthrough (attach/detach/list/info) / serial devices | machines.md |
| `docker` | Docker **extension** cmds: `volume` (clone/export/import), `migrate` | docker.md |
| `debug` (Pro) | Open a debug shell with tools in any container | docker.md |
| `k8s` | Show Kubernetes usage (`orb start k8s`) | kubernetes.md |
| `config` | get/set/add/remove/show/reset settings; `config docker` edits engine JSON | config.md |
| `status` | Is OrbStack running? (exit 0/1/2) | headless.md |
| `update` | Update OrbStack (`-c` check only, exit 3 if outdated) | headless.md |
| `top` | Live activity monitor (CPU/mem/disk/net) | troubleshooting.md |
| `doctor` | Verify Docker integration (`--fix` to repair) | troubleshooting.md |
| `report` / `reset` | Diagnostic bug report / factory reset (destroys data) | troubleshooting.md |
| `login` / `logout` | Manage OrbStack account + Pro license | config.md |
| `version` | Show version | - |
| `completion` | Generate shell completions (bash/zsh/fish/powershell) | config.md |

## Reference files

Read on demand:

- **`references/machines.md`** - full machine lifecycle, `run`/exec, file
  transfer, per-VM CPU/memory/disk limits, isolation, cloud-init, USB/serial,
  and running macOS commands from Linux (`mac`, `ORBENV`).
- **`references/docker.md`** - using `docker` under OrbStack: context, platform/
  Rosetta, volume extension commands, migrating from Docker Desktop, debug
  shell, SSH-agent forwarding, checkpoints, credential store, engine config.
- **`references/domains.md`** - `.orb.local` naming, custom domains label,
  HTTP-port override, wildcards, HTTPS, compose + k8s domains.
- **`references/networking.md`** - port-forwarding, reaching the Mac host
  (`host.docker.internal`), direct container IPs, IP ranges, proxies, IPv6, LAN
  exposure, VPN, self-signed registry certs.
- **`references/ssh.md`** - `ssh orb` patterns, port 32222, key path, IDE setup
  (VS Code / JetBrains / Fleet), Ansible, authorized_keys.
- **`references/kubernetes.md`** - start/stop the cluster, kubectl context,
  kubeconfig, service domains, exposing services.
- **`references/config.md`** - `orb config` subcommands and a full reference of
  every config key with its meaning.
- **`references/headless.md`** - CLI/CI automation: install, service start/stop,
  status + exit codes, non-interactive provisioning, disabling admin prompts and
  context switching, JSON output.
- **`references/troubleshooting.md`** - `doctor`/`report`/`reset`, restarting the
  engine, fixing the Docker context, Rosetta arch errors, cloud-init debugging,
  and the published-port "wedge" / route-loss gotchas.
