# Agent Skills

A collection of reusable skills for AI agents.

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for all commit messages.

Format: `<type>: <description>`

Types:
- `feat`: New feature or skill
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `chore`: Maintenance tasks

## Creating a Skill

A skill is a directory containing a `SKILL.md` file with YAML frontmatter and Markdown instructions.

### Structure

```
skill-name/
├── SKILL.md              # Required - frontmatter + instructions
├── scripts/              # Optional - executable code
├── references/           # Optional - additional docs loaded on demand
└── assets/               # Optional - templates, images, data files
```

### SKILL.md Format

```yaml
---
name: skill-name
description: What the skill does and when to use it. Be specific and include trigger keywords.
---

# Skill Title

Step-by-step instructions, examples, and edge cases go here.
```

**Required fields:**
- `name` — lowercase letters, numbers, hyphens only (max 64 chars). Must match the directory name.
- `description` — what the skill does *and* when to use it (max 1024 chars). Write in third person.

**Optional fields:** `license`, `compatibility`, `metadata` (key-value map), `allowed-tools`.

### Key Guidelines

- **Be concise** — Claude is already smart. Only add context it doesn't have. Keep `SKILL.md` under 500 lines.
- **Progressive disclosure** — put detailed reference material in separate files; link from `SKILL.md`. Keep references one level deep.
- **Match specificity to fragility** — use exact scripts for critical operations, general guidance for flexible tasks.
- **Use consistent terminology** — pick one term per concept and stick with it.
- **Include examples** — concrete input/output pairs improve output quality.

### References

- [Agent Skills Specification](https://agentskills.io/specification.md)
- [Cursor Skills Documentation](https://cursor.com/docs/context/skills.md)
- [Claude Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)
