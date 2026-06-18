# Container & machine domains (.orb.local)

OrbStack gives everything a DNS name under `.orb.local`, with zero-config HTTPS,
so you reach services by name instead of juggling `localhost:PORT`.

**Requirement:** "Allow access to container domains & IPs" must be enabled in
Settings → Network (on by default).

## Automatic names

| Thing | Domain |
|-------|--------|
| Container | `<container-name>.orb.local` |
| Compose service | `<service>.<project>.orb.local` (project = folder of the compose file) |
| Linux machine | `<machine-name>.orb.local` |
| Index of everything running | visit `https://orb.local` |

```bash
docker run --name web -p 80:80 nginx
curl http://web.orb.local            # no port needed for detected web ports
```

Non-web services keep their port: `database.stack.orb.local:5432`.

## Custom domains

Add the `dev.orbstack.domains` label (comma-separated, `.local` TLD only):

```bash
docker run --rm -l dev.orbstack.domains=foo.local,bar.local nginx
```

```yaml
# compose
services:
  nginx:
    image: nginx
    labels:
      - dev.orbstack.domains=foo.local,bar.local
```

Wildcards work: `*.foo.local`. Default names are wildcards too -
`*.web.orb.local` resolves to `web.orb.local`.

## Port / protocol detection

OrbStack auto-detects the listening web port on first connection (it probes with
an `OrbStack-Server-Detection` user agent to decide HTTP vs HTTPS). Override it:

```bash
docker run -l dev.orbstack.http-port=8080 myapp
```

## HTTPS

Every `.orb.local` domain gets a dynamic, trusted certificate automatically -
`https://web.orb.local` just works, no setup.

## Kubernetes domains

- Services: `<service>.<namespace>.svc.cluster.local`
- LoadBalancer / Ingress: `*.k8s.orb.local`

See `references/kubernetes.md`.
