# Kubernetes

OrbStack includes a single-node Kubernetes cluster and `kubectl`.

```bash
orb start k8s            # start the cluster
orb stop k8s             # stop it
orb k8s                  # print usage instructions
kubectl get pods -A
```

Enable it persistently with `orb config set k8s.enable true`.

## kubectl context & kubeconfig

The cluster is registered as the **`orbstack`** kubectl context and selected
automatically. Kubeconfig lives at `~/.orbstack/k8s/config.yml`.

```bash
orb config set docker.set_context false   # stop OrbStack auto-switching contexts
```

## Service access & domains

All service types are reachable from macOS without `kubectl port-forward`:

- In-cluster DNS works directly: `<service>.<namespace>.svc.cluster.local`
- LoadBalancer / Ingress services: `*.k8s.orb.local`

Related config keys:

| Key | Meaning |
|-----|---------|
| `k8s.enable` | Start Kubernetes with OrbStack |
| `k8s.expose_services` | Expose service ports to the host/LAN |
| `k8s.kubeconfig_use_domain` | Use a domain instead of an IP in the kubeconfig |
| `k8s.tls_san` | Extra TLS subject-alternative-names for the API server |

See `references/domains.md` for `.orb.local` naming and `references/config.md`
for all keys.
