# Proxmox CLI Cheat Sheet

Quick reference for the most common Proxmox VE commands.

## qm — VM Management

```bash
qm list                              # List all VMs
qm create <vmid> [options]           # Create a new VM
qm destroy <vmid> [--purge]          # Delete a VM
qm start <vmid>                      # Start
qm shutdown <vmid>                   # ACPI shutdown
qm stop <vmid>                       # Force stop
qm reboot <vmid>                     # Reboot
qm reset <vmid>                      # Hard reset
qm suspend <vmid>                    # Suspend to RAM
qm resume <vmid>                     # Resume
qm status <vmid>                     # Show status
qm config <vmid>                     # Show configuration
qm set <vmid> [options]              # Modify configuration
qm clone <vmid> <newid> [options]    # Clone a VM
qm template <vmid>                   # Convert to template
qm migrate <vmid> <node> [--online]  # Migrate to another node
qm snapshot <vmid> <name>            # Create snapshot
qm rollback <vmid> <name>            # Rollback to snapshot
qm delsnapshot <vmid> <name>         # Delete snapshot
qm listsnapshot <vmid>               # List snapshots
qm disk resize <vmid> <disk> <size>  # Resize a disk
qm importdisk <vmid> <img> <storage> # Import disk image
qm monitor <vmid>                    # QEMU monitor console
qm agent <vmid> <command>            # Guest agent commands
qm unlock <vmid>                     # Remove lock
qm pending <vmid>                    # Show pending config changes
```

## pct — Container Management

```bash
pct list                             # List all containers
pct create <ctid> <template> [opts]  # Create container
pct destroy <ctid>                   # Delete container
pct start <ctid>                     # Start
pct shutdown <ctid>                  # Graceful shutdown
pct stop <ctid>                      # Force stop
pct reboot <ctid>                    # Reboot
pct status <ctid>                    # Show status
pct config <ctid>                    # Show configuration
pct set <ctid> [options]             # Modify configuration
pct enter <ctid>                     # Open shell inside container
pct exec <ctid> -- <command>         # Run command in container
pct console <ctid>                   # Attach console
pct clone <ctid> <newid> [options]   # Clone container
pct snapshot <ctid> <name>           # Create snapshot
pct rollback <ctid> <name>           # Rollback to snapshot
pct migrate <ctid> <node>            # Migrate container
pct unlock <ctid>                    # Remove lock
pct push <ctid> <src> <dst>          # Copy file into container
pct pull <ctid> <src> <dst>          # Copy file from container
```

## pveam — Appliance/Template Management

```bash
pveam update                         # Update template list
pveam available                      # List available templates
pveam available --section system     # List system templates
pveam available --section turnkey    # List Turnkey templates
pveam download <storage> <template>  # Download a template
pveam list <storage>                 # List downloaded templates
pveam remove <storage>:<template>    # Remove a template
```

## pvesm — Storage Management

```bash
pvesm status                         # List all storage with usage
pvesm list <storage>                 # List content on storage
pvesm add <type> <name> [options]    # Add storage pool
pvesm remove <name>                  # Remove storage pool
pvesm set <name> [options]           # Modify storage
pvesm alloc <storage> <vmid> <name> <size>  # Allocate volume
pvesm free <volume>                  # Free/delete a volume
pvesm scan nfs <server>              # Scan NFS exports
pvesm scan lvm                       # Scan LVM volume groups
pvesm scan zfs                       # Scan ZFS pools
```

## pvecm — Cluster Management

```bash
pvecm create <name>                  # Create cluster
pvecm add <ip>                       # Join cluster
pvecm status                         # Show cluster status
pvecm nodes                          # List nodes
pvecm delnode <name>                 # Remove node
pvecm expected <num>                 # Set expected votes (recovery)
```

## vzdump — Backup

```bash
vzdump <vmid/ctid>                   # Backup guest
vzdump <vmid> --mode snapshot        # Snapshot-based backup
vzdump <vmid> --mode stop            # Stop-mode backup
vzdump <vmid> --compress zstd        # With compression
vzdump --all --storage <name>        # Backup all guests
vzdump <vmid> --mailto user@host     # Email notification
```

## Restore

```bash
qmrestore <archive> <vmid>          # Restore VM
pct restore <ctid> <archive>        # Restore container
qmrestore <archive> <vmid> --storage <name>  # Restore to specific storage
```

## pvesh — API Shell

```bash
pvesh get /nodes                     # List nodes via API
pvesh get /nodes/<node>/qemu         # List VMs on a node
pvesh get /nodes/<node>/lxc          # List containers on a node
pvesh get /cluster/resources         # List all cluster resources
pvesh create /nodes/<node>/qemu      # Create VM via API
```

## Firewall

```bash
pve-firewall start                   # Enable firewall
pve-firewall stop                    # Disable firewall
pve-firewall status                  # Show status
```

## System / Host

```bash
pveversion                           # Show Proxmox version
pveperf                              # Run performance benchmark
pvesubscription get                  # Show subscription status
systemctl restart pvedaemon          # Restart PVE daemon
systemctl restart pveproxy           # Restart PVE web proxy
journalctl -u pvedaemon              # View PVE daemon logs
```

## Source References

- [qm manual](https://pve.proxmox.com/pve-docs-6/qm.1.html)
- [Proxmox CLI Guide (dev.to)](https://dev.to/sebos/how-to-build-and-manage-virtual-machines-using-proxmox-cli-a-step-by-step-guide-5926)
- [Top 10 Proxmox CLI Commands](https://www.nakivo.com/blog/top-10-proxmox-cli-commands/)
- [Proxmox Cheat Sheet (Stordis)](https://stordis.com/proxmox-cheat-sheet/)
