i---
name: topydo
description: Manage todo.txt tasks using topydo CLI. Add, list, complete, prioritize, tag, and organize tasks with dependencies, due dates, recurrence, and projects. Use for any task management, todo lists, or when the user mentions tasks, todos, or todo.txt.
license: MIT
compatibility: Requires Python 3 and pip. Works on macOS, Linux, and Windows.
metadata: {"clawdbot":{"requires":{"bins":["topydo"]},"install":[{"id":"brew","kind":"brew","formula":"topydo","bins":["topydo"],"label":"Install topydo (brew)"},{"id":"pip","kind":"pip","package":"topydo","bins":["topydo"],"label":"Install topydo (pip)"}]}}
---

# topydo - Todo.txt Task Manager

topydo is a powerful CLI for managing tasks in the todo.txt format. It supports dependencies, due dates, start dates, recurrence, priorities, projects, and contexts.

## Installation

### pip (recommended, all platforms)
```bash
pip3 install topydo

# With column UI support (TUI)
pip3 install 'topydo[columns]'

# With prompt mode support
pip3 install 'topydo[prompt]'

# Full installation
pip3 install 'topydo[columns,prompt,ical]'
```

### Homebrew (macOS)
```bash
brew install topydo
```

### apt (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3-pip
pip3 install topydo
```

## Configuration

topydo looks for config files in this order:
- `/etc/topydo.conf`
- `~/.config/topydo/config`
- `~/.topydo`
- `.topydo` (current directory)
- `topydo.conf` (current directory)

Example config (`~/.topydo`):
```ini
[topydo]
filename = ~/todo.txt
archive_filename = ~/done.txt
colors = 1
identifiers = text

[add]
auto_creation_date = 1

[sort]
sort_string = desc:importance,due,desc:priority
keep_sorted = 0
ignore_weekends = 1
```

## Core Commands

### Adding Tasks
```bash
# Basic task
topydo add "Buy groceries"

# With priority (A-Z, A is highest)
topydo add "(A) Urgent task"

# With project and context
topydo add "Write report +ProjectX @office"

# With due date (absolute or relative)
topydo add "Submit proposal due:2025-01-15"
topydo add "Call mom due:tomorrow"
topydo add "Weekly review due:fri"

# With start/threshold date
topydo add "Future task t:2025-02-01"
topydo add "Start next week t:monday"

# With recurrence
topydo add "Water plants due:sat rec:1w"
topydo add "Pay rent due:2025-02-01 rec:+1m"  # Strict recurrence

# With dependencies
topydo add "Deploy app"
topydo add "Write tests before:1"  # Must complete before task 1
topydo add "Review code partof:1"   # Part of task 1
```

### Listing Tasks
```bash
# List all relevant tasks
topydo ls

# List all tasks including hidden/blocked
topydo ls -x

# Filter by project
topydo ls +ProjectX

# Filter by context
topydo ls @office

# Filter by priority
topydo ls "(A)"
topydo ls "(>C)"  # Greater than C

# Filter by due date
topydo ls due:today
topydo ls due:tomorrow
topydo ls "due:<today"      # Overdue
topydo ls "due:<=fri"       # Due by Friday

# Combine filters
topydo ls +ProjectX @office due:today

# Exclude items
topydo ls -- -@waiting

# Sort results
topydo ls -s priority
topydo ls -s desc:due,priority

# Group results
topydo ls -g project
topydo ls -g context,priority

# Limit output
topydo ls -n 5

# Custom format
topydo ls -F "%I %p %s %{due:}d"
```

### Completing Tasks
```bash
# Complete by ID
topydo do 1
topydo do 1 2 3  # Multiple tasks

# Complete by expression
topydo do -e due:today
topydo do -e +ProjectX

# With custom completion date
topydo do -d yesterday 1
```

### Priority Management
```bash
# Set priority
topydo pri 1 A
topydo pri 1 2 3 B  # Multiple tasks

# Remove priority
topydo depri 1
```

### Tagging Tasks
```bash
# Add/set tag
topydo tag 1 due tomorrow
topydo tag 1 star 1

# Remove tag (omit value)
topydo tag 1 due

# Force relative date conversion
topydo tag -r 1 customtag 2w
```

### Modifying Tasks
```bash
# Append text
topydo append 1 "additional notes"
topydo append 1 due:friday

# Edit in text editor
topydo edit 1
topydo edit -e +ProjectX  # Edit filtered tasks
```

### Deleting Tasks
```bash
topydo del 1
topydo del 1 2 3
topydo del -e completed:today  # Delete by expression
```

### Dependencies
```bash
# Add dependency (task 2 depends on task 1)
topydo dep add 2 to 1
topydo dep add 2 partof 1
topydo dep add 2 before 1
topydo dep add 2 after 1

# List dependencies
topydo dep ls 1 to        # What depends on 1
topydo dep ls to 1        # What 1 depends on

# Remove dependency
topydo dep rm 2 to 1

# Visualize (requires graphviz)
topydo dep dot 1 | dot -Tpng -o deps.png
```

### Postponing Tasks
```bash
# Postpone due date
topydo postpone 1 1w      # 1 week
topydo postpone 1 3d      # 3 days
topydo postpone 1 2m      # 2 months

# Also postpone start date
topydo postpone -s 1 1w
```

### Other Commands
```bash
# Sort the todo.txt file
topydo sort

# Revert last command
topydo revert
topydo revert ls  # Show revert history

# List projects
topydo lsprj

# List contexts
topydo lscon

# Archive completed tasks
topydo archive
```

## Relative Dates

Supported formats for due/start dates:
- `today`, `tomorrow`, `yesterday`
- Weekdays: `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`
- Periods: `1d` (days), `2w` (weeks), `3m` (months), `1y` (years)
- Business days: `5b` (excludes weekends)

## Task Format Reference

```
(A) 2025-01-11 Task text +Project @Context due:2025-01-15 t:2025-01-10 rec:1w star:1
│   │          │         │        │        │             │            │      │
│   │          │         │        │        │             │            │      └─ Star marker
│   │          │         │        │        │             │            └─ Recurrence
│   │          │         │        │        │             └─ Start/threshold date
│   │          │         │        │        └─ Due date
│   │          │         │        └─ Context
│   │          │         └─ Project
│   │          └─ Task description
│   └─ Creation date
└─ Priority (A-Z)
```

## Sort/Group Expressions

Available fields:
- `priority` - Task priority
- `due` - Due date
- `importance` - Calculated importance
- `importance-avg` - Average importance including dependencies
- `creation` - Creation date
- `project` - Project name
- `context` - Context name
- `text` - Task text
- `length` - Task length (start to due)

Prefix with `desc:` for descending order.

Example: `desc:importance,due,desc:priority`

## Tips

1. **Quick alias**: Add to shell config:
   ```bash
   alias t="topydo"
   alias ta="topydo add"
   alias tl="topydo ls"
   alias td="topydo do"
   ```

2. **Text identifiers**: Enable stable IDs in config:
   ```ini
   [topydo]
   identifiers = text
   ```

3. **Hide internal tags**: Default hidden: `id`, `p`, `ical`

4. **Importance calculation**: Based on priority, due date, and star status

5. **Starred tasks**: Add `star:1` tag for extra importance

## Common Workflows

### Morning Review
```bash
topydo ls due:today -s desc:importance
topydo ls "due:<=today" -n 10
```

### Weekly Planning
```bash
topydo ls "due:<=fri" -g project
topydo ls t:today  # Tasks starting today
```

### Project Focus
```bash
topydo ls +ProjectX -x -s due
topydo dep dot +ProjectX | dot -Tsvg -o project.svg
```

### Cleanup
```bash
topydo archive
topydo ls "completed:<-7d" -x  # Completed over a week ago
```
