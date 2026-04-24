---
name: obsidian-daily
description: Manages Obsidian Daily Notes via the official Obsidian CLI. Creates and opens daily notes, appends entries (journals, logs, tasks, links), reads daily notes and vault files, searches vault content, and handles relative dates like "yesterday", "last Friday", and "3 days ago". Requires Obsidian 1.12+ with Command line interface enabled.
metadata:
  author: github.com/bastos
  version: "2.0"
---

# Obsidian Daily Notes

Interact with Obsidian Daily Notes through the official `obsidian` command: create
or open today's note, append entries, read notes, and search vault content.

## Setup

Check that the official CLI is available:

```bash
obsidian version
```

If the command is unavailable, ask the user to enable Obsidian's CLI:
1. Install or update to Obsidian 1.12 or newer.
2. Open **Settings > General**.
3. Enable **Command line interface** and follow the registration prompt.

Target a vault explicitly when needed by placing `vault=<name-or-id>` before the
command:

```bash
obsidian vault="Work" daily
```

**Obsidian Daily Notes plugin defaults:**
- Date format: `YYYY-MM-DD`
- New file location: Vault root
- Template file location: (none)

## Date Handling

Get current date:

```bash
date +%Y-%m-%d
```

Cross-platform relative dates (GNU first, BSD fallback):

| Reference | Command |
|-----------|---------|
| Today | `date +%Y-%m-%d` |
| Yesterday | `date -d yesterday +%Y-%m-%d 2>/dev/null \|\| date -v-1d +%Y-%m-%d` |
| Last Friday | `date -d "last friday" +%Y-%m-%d 2>/dev/null \|\| date -v-1w -v+fri +%Y-%m-%d` |
| 3 days ago | `date -d "3 days ago" +%Y-%m-%d 2>/dev/null \|\| date -v-3d +%Y-%m-%d` |
| Next Monday | `date -d "next monday" +%Y-%m-%d 2>/dev/null \|\| date -v+monday +%Y-%m-%d` |

## Commands

### Open/Create Today's Note

```bash
obsidian daily
```

Opens today's daily note in Obsidian, creating it from template if it doesn't exist.

### Append Entry

```bash
obsidian daily:append content="ENTRY_TEXT"
```

Append without adding a newline:

```bash
obsidian daily:append content="ENTRY_TEXT" inline
```

### Read Note

Today:

```bash
obsidian daily:read
```

Specific date, using the vault's configured daily-note folder and date format:

```bash
obsidian read path="Daily Notes/2025-01-10.md"
```

Relative date (yesterday):

```bash
obsidian read path="Daily Notes/$(date -d yesterday +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d).md"
```

### Search Content

```bash
obsidian search query="TERM"
```

### Search Notes

Machine-readable search:

```bash
obsidian search query="TERM" format=json
```

### Specific Vault

Put `vault="NAME"` before the command:

```bash
obsidian vault="Work" read path="Daily Notes/2025-01-10.md"
```

## Example Output

```markdown
- Went to the doctor
- [ ] Buy groceries
- https://github.com/anthropics/skills
- 15:45 This is a log line
```

## Use Cases

**Journal entry:**
```bash
obsidian daily:append content="- Went to the doctor"
```

**Task:**
```bash
obsidian daily:append content="- [ ] Buy groceries"
```

**Link:**
```bash
obsidian daily:append content="- https://github.com/anthropics/skills"
```

**Timestamped log:**
```bash
obsidian daily:append content="- $(date +%H:%M) This is a log line"
```

**Read last Friday:**
```bash
obsidian read path="Daily Notes/$(date -d 'last friday' +%Y-%m-%d 2>/dev/null || date -v-1w -v+fri +%Y-%m-%d).md"
```

**Search for "meeting":**
```bash
obsidian search query="meeting"
```
