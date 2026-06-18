# Docker under OrbStack

You don't need a Linux machine to use Docker - OrbStack ships a Docker engine you
drive with the normal `docker` CLI from macOS. Compose and buildx are included
and kept up to date.

```bash
docker run -p 80:80 docker/getting-started   # then visit http://localhost
docker compose up
docker buildx build .
```

For networking and `.orb.local` domains see `references/networking.md` and
`references/domains.md`.

## Docker context

OrbStack registers a context named **`orbstack`** and selects it automatically.

```bash
docker context use orbstack          # if `docker` can't reach the daemon
orb config set docker.set_context false   # stop OrbStack auto-switching contexts
```

A socket symlink at `/var/run/docker.sock` keeps third-party tools and Dev
Containers working.

## Platform / architecture (Apple Silicon)

x86/amd64 images run via Rosetta. Supported platforms: `linux/amd64`,
`linux/arm64`, `linux/arm`, `linux/386`.

```bash
docker run -it --rm --platform linux/amd64 alpine
docker build --platform linux/arm64 .
export DOCKER_DEFAULT_PLATFORM=linux/amd64        # default for the session
```

If an x86 binary fails inside a **machine** with a libc error:
`sudo dpkg --add-architecture amd64 && sudo apt install libc6:amd64`.

## Volumes

Prefer **named volumes** over bind mounts - data stays in Linux with no
cross-filesystem overhead. Inspect them on macOS at `~/OrbStack/docker/volumes/`.

OrbStack adds extension commands for volumes:

```bash
orb docker volume clone  SRC DEST              # copy a volume (or -n NAME; default <src>2)
orb docker volume export VOL out.tar.zst       # back up a volume
orb docker volume import in.tar.zst            # restore (-n NAME to rename; default: original name)
```

## Migrate from Docker Desktop

```bash
orb docker migrate          # move containers, volumes, and images over
```

(`orb migrate docker` is the deprecated spelling.)

## Debug shell (Pro)

Attach a shell with real tools to *any* container - even minimal, distroless, or
read-only ones:

```bash
orb debug mysql1                       # aliases: wormhole
orb debug -w /app mysql1               # set workdir
orb debug -f mysql1                    # fall back to `docker exec` if no Pro license
orb debug -c remote-context mysql1     # debug a container on another Docker context
```

Inside the debug shell, `dctl` installs/removes packages. Requires an OrbStack
Pro license (use `-f` otherwise).

## SSH-agent forwarding into containers

```bash
docker run -it --rm \
  -v /run/host-services/ssh-auth.sock:/agent.sock \
  -e SSH_AUTH_SOCK=/agent.sock \
  alpine
```

## Checkpoints (CRIU)

Docker experimental mode is on by default:

```bash
docker checkpoint create my-container chk1
docker start --checkpoint chk1 my-container
```

## Credential store

OrbStack uses the `osxkeychain` credential store (Docker Desktop used `desktop`).
Log in to private registries normally:

```bash
docker login ghcr.io
```

## Engine config & control

```bash
orb config docker            # open ~/.orbstack/config/docker.json in $EDITOR (restarts engine on save)
orb logs docker              # Docker engine logs
orb restart docker           # restart just the Docker engine
```

Self-signed registry certs go under `~/.docker/certs.d/<registry>/` (ca.crt,
client.cert, client.key) - see `references/networking.md`.

## Kubernetes

Brief: `orb start k8s` then `kubectl get pods -A`. Full detail in
`references/kubernetes.md`.
