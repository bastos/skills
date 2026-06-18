# Linux machines

Managing OrbStack Linux VMs with `orb`/`orbctl`. A "machine" is a lightweight
Linux VM that boots in ~2s and shares files/network with macOS.

## Create

```bash
orb create DISTRO[:VERSION] [NAME]
```

```bash
orb create ubuntu                       # newest Ubuntu, named "ubuntu"
orb create ubuntu:24.04 dev             # specific version + custom name
orb create -a amd64 fedora foo          # x86 emulation via Rosetta
orb create --memory 4G --cpus 2 --disk 64G ubuntu dev
orb create -u alice -p ubuntu           # custom user + prompt for password
orb create -c cloud-init.yml ubuntu ci  # provision with cloud-init
```

Aliases: `add`, `new`. Version is optional (latest stable is used).

| Flag | Meaning |
|------|---------|
| `-a, --arch arm64\|amd64` | Override CPU architecture (amd64 = Rosetta on Apple Silicon) |
| `--cpus N` | CPU core limit for this machine |
| `--memory 4G` | Memory limit (MiB, or units like `4G`) |
| `--disk 64G` | Disk usage limit |
| `-u, --user NAME` | Username for the default user (defaults to your macOS user) |
| `-p, --set-password` | Set a password for the default user **and** root |
| `-c, --user-data PATH` | Cloud-init user-data file for automatic setup |
| `--isolated` | Isolated machine: no file sharing / host integration |
| `--isolate-network` | Block an isolated machine from other machines + host IPs |
| `--mount SRC[:DEST]` | Add a selective host mount to an isolated machine (repeatable) |
| `--forward-ssh-agent` | Enable SSH agent forwarding for an isolated machine |

**Supported distros** (default version in parens): alma, alpine, arch, centos,
debian (bookworm/12), devuan, fedora, gentoo, kali, nixos, openeuler, opensuse,
oracle, rocky, ubuntu (resolute/26.04), void. Run `orb create --help` for the
full version matrix on your installed version.

## List & inspect

```bash
orb list                     # table of machines + status
orb list -q                  # names only
orb list -r                  # running only
orb list -f json             # JSON (scriptable)
orb info ubuntu              # details for one machine
orb info ubuntu -f json
```

## Lifecycle

```bash
orb start dev                # start a machine
orb start -a                 # start all
orb start                    # (with no machine name) start OrbStack itself

orb stop dev                 # stop a machine
orb stop -a                  # stop all machines
orb stop                     # WARNING: no args stops ALL of OrbStack (Docker + every machine)
orb stop -f                  # force-stop the VM immediately (may lose data)

orb restart dev              # restart a machine (or `orb restart -a`)
orb delete dev               # PERMANENTLY delete (data lost, no warning)
orb delete -a -f             # delete everything, no confirmation
```

`orb start` with no machine starts machines that were running when last stopped.

## Default machine

```bash
orb default                  # show the default
orb default dev              # set "dev" as default (used by bare `orb`, `orb <cmd>`)
```

## Clone / rename / move

```bash
orb clone ubuntu ubuntu-test # copy-on-write snapshot; new machine starts stopped
orb rename ubuntu old-ubuntu
```

Cloning pauses the source briefly and does **not** double disk usage (snapshotted,
copied on demand).

## Export / import (backup, transfer)

```bash
orb export ubuntu ubuntu.tar.zst       # pauses machine while exporting
orb import ubuntu.tar.zst -n ubuntu2   # restore under a new name
```

## Run commands inside a machine

```bash
orb uname -a                 # run in default machine (= orbctl run uname -a)
orb -m dev uname -a          # specific machine
orb -m dev -u root apt update   # specific machine + user
orb run ls                   # explicit form (aliases: exec, shell)
```

| Flag (for `run`) | Meaning |
|------|---------|
| `-m, --machine NAME` | Target a specific machine |
| `-u, --user NAME` | Run as a specific user |
| `-w, --workdir DIR` | Set working directory |
| `-s, --shell` | Use the login shell instead of running the command directly |
| `-p, --path` | Translate absolute macOS paths to Linux paths |

**Forward env vars** into the command with `ORBENV` (colon-separated):

```bash
ORBENV=EDITOR:AWS_PROFILE orb git commit
```

Paths are auto-translated when safe; to be explicit prefix Linux paths with
`/mnt/linux` and macOS paths with `/mnt/mac`.

## File transfer

```bash
orb push ~/file.txt                    # -> default machine's home
orb push ~/file.txt code/              # -> ~/code/ in default machine
orb push -m dev ~/file.txt /tmp/       # -> /tmp/ in machine "dev"
orb pull code/out.log .                # Linux ~/code/out.log -> current dir
orb pull -m dev /var/log/syslog .
```

These are conveniences over shared folders. The equivalent plain copy:
`cp ~/file.txt ~/OrbStack/<machine>/home/$USER/code/`.

## Logs

```bash
orb logs ubuntu              # unified machine/boot logs (aliases: log, console)
orb logs ubuntu -a           # all logs (verbose, for debugging)
orb logs docker              # Docker engine logs
```

## USB & serial passthrough

```bash
orb usb list                 # list USB devices (-f json)
orb usb info ID              # device details
orb usb attach ID            # attach to default machine
orb usb attach ID -m dev     # move USB network interfaces to "dev"
orb usb detach ID

orb serial list              # list serial devices
```

## Running macOS commands from inside Linux

Inside a machine, the `mac` command runs things back on macOS:

```bash
mac open https://example.com   # open a URL in the Mac's browser
mac notify "Build done"        # macOS notification
mac uname -a                   # run a Mac command
mac run osascript ...          # explicit form (orbctl-style)
mac link pbcopy                # expose a Mac binary in Linux (open/osascript/code linked by default)
mac unlink pbcopy
mac push / mac pull            # file transfer in the other direction
```

## Key paths

| From | Location |
|------|----------|
| Linux files, on macOS | `~/OrbStack/<machine>/` |
| Docker volumes, on macOS | `~/OrbStack/docker/volumes/` |
| macOS files, from Linux | `/mnt/mac/...` (also at the same absolute path) |
| Other machines, from Linux | `/mnt/machines/<name>/` |
