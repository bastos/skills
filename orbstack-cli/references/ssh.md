# SSH access

OrbStack runs one multiplexed SSH server for every machine - no per-machine
setup. `orb ssh` just prints these details.

## Connect

```bash
ssh orb                  # default machine, default user
ssh dev@orb              # machine "dev"
ssh root@orb             # default machine as root
ssh root@dev@orb         # user@machine@orb
```

Port forwarding (`-L`/`-R`) and SSH **agent forwarding** (automatic) both work.

## Manual connection details

For apps that don't use OpenSSH (e.g. IntelliJ IDEA):

| Field | Value |
|-------|-------|
| Host | `localhost` |
| Port | `32222` |
| User | `default` (or a specific user) |
| Private key | `~/.orbstack/ssh/id_ed25519` |

```bash
ssh -p 32222 -i ~/.orbstack/ssh/id_ed25519 default@localhost
```

## IDE integration

- **VS Code:** install "Remote - SSH", connect to host `orb` (or `dev@orb`).
  `orb` shows up in the Remote Explorer sidebar.
- **JetBrains Fleet:** connect to the `orb` host directly.
- **JetBrains IntelliJ/others:** use the manual host/port/user/key above.

## Security & keys

- Password auth is disabled - public/private key only.
- Access is restricted to `localhost` (set `ssh.expose_port` to allow remote).
- Add extra public keys in `~/.orbstack/ssh/authorized_keys` (ECDSA and RSA
  supported). You can replace the generated keypair with your own.

## Ansible

```ini
[servers]
ubuntu@orb  ansible_user=ubuntu
# root: root@ubuntu@orb  ansible_user=root@ubuntu
```
