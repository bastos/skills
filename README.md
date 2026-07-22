# Agent Skills

A collection of skills for AI agents.

## Overview

This repository contains reusable skills that enhance AI agent capabilities. Skills are modular, composable units that provide specialized knowledge and workflows for agents.

## Skills

| Skill | Description |
|-------|-------------|
| [apple-cktool](apple-cktool/) | Automate CloudKit schema and test-data workflows with Apple's Xcode-bundled `cktool` CLI on macOS, including safe authentication, validation, reset, query, and deletion procedures. |
| [apple-cktool-js](apple-cktool-js/) | Build typed CloudKit automation for Node.js, browsers, and CI with Apple's CKTool JS packages, Promise APIs, secure token injection, and guarded schema and record operations. |
| [audit-training-experiment](audit-training-experiment/) | Audit ML experiments for reproducibility, evidence integrity, leakage, checkpoint identity, evaluation validity, and overclaimed conclusions. |
| [awk](awk/) | Expert GNU awk (gawk) one-liner generation and transformation for text field processing, column extraction, aggregation, CSV/TSV reformatting, and log analysis. |
| [close-out-ml-experiment](close-out-ml-experiment/) | Preserve experiment evidence, reconcile report discrepancies, record the canonical decision and limitations, and prepare a concise handoff. |
| [compare-models-blindly](compare-models-blindly/) | Create seeded blinded model-comparison packets and evaluate candidate outputs with reversed order to control identity and presentation bias. |
| [conventional-commits](conventional-commits/) | Format commit messages using the Conventional Commits specification for automated tooling, changelog generation, and semantic versioning. |
| [design-resumable-model-evaluation](design-resumable-model-evaluation/) | Design strict model benchmarks that persist per-case evidence, resume without repeating work, and use mathematically valid early stopping. |
| [ios-design-review](ios-design-review/) | Review iOS app UI/UX design quality using Apple's design principles and the Liquid Glass-era design language from WWDC25/26. |
| [mikrotik-routeros](mikrotik-routeros/) | Configure and automate MikroTik RouterOS routers through the terminal, CLI, .rsc imports, scripts, Scheduler, Netwatch, firewall, NAT, DHCP, bridge, VLAN, routing, and backups. |
| [obsidian-daily](obsidian-daily/) | Manage Obsidian Daily Notes via the official Obsidian CLI. Create, open, and append entries to daily notes, read past notes by date, and search vault content. |
| [orbstack-cli](orbstack-cli/) | Drive OrbStack from the terminal on macOS: the orb/orbctl CLI for Linux VMs, Docker engine usage, .orb.local domains and networking, SSH, Kubernetes, config keys, and headless/CI automation. |
| [package-private-ml-artifacts](package-private-ml-artifacts/) | Inventory, hash, scan, and verify ML artifacts before an explicitly approved private upload. |
| [prepare-training-corpus](prepare-training-corpus/) | Build deterministic train, validation, and test corpora with provenance, group-safe splits, manifests, hashes, and leakage checks. |
| [proxmox-admin](proxmox-admin/) | Administer Proxmox VE hosts, create and manage KVM virtual machines with qm, manage LXC containers with pct, and configure storage, networking, and clusters via the CLI. |
| [review-ios-ui-apple-hig](review-ios-ui-apple-hig/) | Review iOS app UI against Apple Human Interface Guidelines and iOS platform conventions using page-specific Apple reference notes. |
| [review-training-data-quality](review-training-data-quality/) | Audit training corpora for distribution collapse, ambiguity, context sufficiency, hard negatives, abstention behavior, leakage, and label defensibility. |
| [run-hugging-face-training-smoke](run-hugging-face-training-smoke/) | Run a bounded private Hugging Face training smoke with immutable inputs, preflight checks, stop gates, checkpoint verification, and reproducible evidence. |
| [sed](sed/) | Expert GNU sed one-liner generation for stream editing, in-place file editing, bulk find/replace, log filtering, and text transformation pipelines. |
| [select-and-verify-best-checkpoint](select-and-verify-best-checkpoint/) | Verify evaluation cadence, best-checkpoint selection, and held-out inference checkpoint identity before trusting test metrics. |
| [send-to-minion](send-to-minion/) | Delegate a prompt to exactly one helper agent, supervise it to completion, verify its result, and return the parent agent's final answer. |
| [swift-review](swift-review/) | Review Swift/Xcode codebases, pull requests, local changes, or individual files against Swift best practices for style, API design, memory management, performance, and testing. |
| [tmuxinator](tmuxinator/) | Create, edit, and debug tmuxinator project configurations for complex tmux session layouts and automated development environment startup. |
| [topydo](topydo/) | Manage todo.txt tasks using topydo CLI. Add, list, complete, prioritize, tag, and organize tasks with dependencies, due dates, and recurrence. |
| [validate-structured-model-output](validate-structured-model-output/) | Validate JSON or tool-call model outputs without repair across parsing, schema, identifiers, semantics, replay, and safety gates. |
| [write-a-prompt](write-a-prompt/) | Create a copy-ready prompt from a rough request, source material, or the current conversation without performing the underlying task. |

## Learn More

Visit [agentskills.io](https://agentskills.io/) for documentation and examples.

## License

MIT
