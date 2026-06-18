# Headless / CI / scripting

OrbStack runs without the GUI, which makes it usable in CI and scripts. The CLI
returns meaningful exit codes so you can gate on state.

## Install

```bash
brew install orbstack
```

## Start / stop the service

```bash
orb start                    # start OrbStack (no machine name = the service itself)
orb stop                     # stop ALL of OrbStack (engine + every machine)
```

## Health & state (exit codes)

```bash
orb status                   # prints Running/Starting/Stopped
# exit codes: 0 = Running, 1 = Stopped, 2 = Starting
```

```bash
# wait until ready in a script
until orb status >/dev/null 2>&1; do sleep 1; done
```

```bash
orb update -c                # check for updates without installing
# exit codes: 0 = up to date, 3 = outdated
```

## Non-interactive setup

```bash
orb config set setup.use_admin false   # don't prompt for admin/sudo permissions
orb config set docker.set_context false # don't hijack the active docker context
```

## Provision a machine unattended

```bash
orb create -c cloud-init.yml ubuntu ci-runner   # cloud-init does first-boot setup
orb create --memory 4G --cpus 2 ubuntu ci-runner
orb -m ci-runner -u root ./bootstrap.sh         # then run setup steps
```

Pass env vars into a run with `ORBENV`:

```bash
ORBENV=AWS_PROFILE:CI orb -m ci-runner ./deploy.sh
```

## Machine-readable output

```bash
orb list -f json
orb info ubuntu -f json
orb usb list -f json
```

## Updates without the GUI

Auto-update needs the GUI app, which is fine for CI. To update manually:

```bash
brew upgrade --greedy orbstack
```

(`--greedy` is needed because Homebrew skips self-updating apps by default.)

## Docker in CI

The `docker` CLI works as-is once OrbStack is running:

```bash
orb start
until orb status >/dev/null 2>&1; do sleep 1; done
docker run -p 80:80 docker/getting-started
```
