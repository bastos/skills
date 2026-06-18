# Configuration

`orb config` reads and writes OrbStack settings. Some changes only take effect
after restarting OrbStack.

## Subcommands

```bash
orb config show              # list every key + current value
orb config get KEY           # read one value
orb config set KEY VALUE     # set a value   (e.g. orb config set memory_mib 8192)
orb config add KEY VALUE     # append to a list-type option
orb config remove KEY VALUE  # remove from a list-type option
orb config reset             # reset all config to defaults
orb config docker            # open the Docker engine JSON (~/.orbstack/config/docker.json) in $EDITOR
```

`orb config show` is the source of truth for available keys on your installed
version. The `docker.json` file holds Docker **engine** settings (bip,
default-address-pools, ipv6, ...) - see `references/networking.md`.

## Key reference

### Resources (global, apply to OrbStack as a whole)

| Key | Meaning |
|-----|---------|
| `cpu` | Global CPU core limit |
| `memory_mib` | Global memory limit, in MiB (e.g. `8192`) |
| `rosetta` | Use Rosetta for x86 emulation on Apple Silicon |

### Per-machine (`machine.<name>.*`, also `machine.docker.*` for the Docker VM)

| Key | Meaning |
|-----|---------|
| `machine.<name>.cpu` | CPU limit for that machine (0 = unlimited) |
| `machine.<name>.memory_mib` | Memory limit for that machine |
| `machine.<name>.disk_bytes` | Disk limit |
| `machine.<name>.username` | Default Linux user |
| `machine.<name>.isolated` | Isolated machine (no host integration) |
| `machine.<name>.mounts` | Selective host mounts for an isolated machine |
| `machine.<name>.http_port` / `.https_port` | Fixed host ports for the machine's web server |

### Docker engine

| Key | Meaning |
|-----|---------|
| `docker.set_context` | Auto-switch the active Docker context to `orbstack` (set false to stop it) |
| `docker.expose_ports_to_lan` | Make published container ports reachable on the LAN (default true) |
| `docker.node_name` | Docker node name (`orbstack`) |

### Kubernetes

| Key | Meaning |
|-----|---------|
| `k8s.enable` | Start Kubernetes with OrbStack |
| `k8s.expose_services` | Expose service ports to host/LAN |
| `k8s.kubeconfig_use_domain` | Use a domain (not IP) in kubeconfig |
| `k8s.tls_san` | Extra TLS SANs for the API server |

### Networking

| Key | Meaning |
|-----|---------|
| `network_proxy` | Proxy URL, or `auto` (follow macOS) / `none` |
| `network.proxy.exclude` | Comma-separated proxy bypass list (hosts/CIDRs) |
| `network.https` | Enable zero-config HTTPS for `.orb.local` |
| `network.subnet4` | IPv4 subnet for machines (e.g. `192.168.138.0/23`) |
| `network_bridge` | Bridged networking |
| `machines.expose_ports_to_lan` | Expose machine ports to the LAN |
| `machines.forward_ports` | Forward machine ports to the host |
| `ssh.expose_port` | Expose the SSH port (32222) beyond localhost |

### App / behavior

| Key | Meaning |
|-----|---------|
| `setup.use_admin` | Allow admin/sudo prompts during setup (set false for headless/CI) |
| `app.start_at_login` | Launch OrbStack at login |
| `app.wait_for_container_stop` | Wait for containers to stop cleanly on quit |
| `power.pause_in_sleep` | Pause the VM when the Mac sleeps |
| `data_allow_backup` | Allow Time Machine to back up OrbStack data |
| `mount_hide_shared` | Hide shared mounts |

## Account / license

```bash
orb login                    # log in + activate a license
orb login --domain acme.com  # SSO
orb login --force            # re-login even if already logged in
orb logout
```

## Shell completion

```bash
orb completion zsh > "${fpath[1]}/_orb"          # zsh
orb completion bash > $(brew --prefix)/etc/bash_completion.d/orb
orb completion fish > ~/.config/fish/completions/orb.fish
```

Tab completion is auto-configured for bash/zsh/fish on a normal install.
