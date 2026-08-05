---
name: unhobble-agent-context
description: Audits and designs lean, coherent context across system prompts, persistent instructions, repository guidance, skills, tool descriptions, memory, and references. Use for context engineering; creating, reviewing, simplifying, or reorganizing agent context; resolving conflicting, duplicated, bloated, stale, or misplaced guidance; designing progressive disclosure; or deciding where shared information should live.
---

# Unhobble Agent Context

Shape persistent context so each task begins with the smallest coherent guidance it needs and can discover deeper material when relevant. Preserve local knowledge and hard boundaries; remove friction that does not change outcomes.

## Workflow

1. Define the outcome the context must improve.

   - Identify the tasks, decisions, or recurring failures in scope.
   - For an audit, inspect the sources that are actually assembled together and their precedence.
   - For new context, start from representative requests and the information they truly require.

2. Inventory each instruction by purpose and owner.

   Record what it changes, when it applies, where it currently lives, whether another source already owns it, and whether the current task authorizes changing it. Do not broaden the audit to unrelated documentation.

3. Put information in the narrowest durable home that reliably supplies it.

   | Information | Preferred home |
   | --- | --- |
   | Immediate outcome, inputs, and task constraints | Current request |
   | Product role and universal invariants | Highest-scope instructions |
   | Repository-wide conventions and non-obvious gotchas | Root project guidance |
   | Directory- or component-specific rules | Nearest scoped guidance |
   | Reusable workflow needed only for certain tasks | Skill |
   | Operation semantics, parameters, states, and errors | Tool interface or description |
   | Stable preferences or facts reused across sessions | Memory, subject to retention policy |
   | Detailed specifications, tests, code, mockups, or rubrics | Reference loaded when relevant |

4. Simplify before adding.

   - Remove facts discoverable cheaply from the workspace, generic advice, stale history, repeated instructions, and rules without a concrete failure or invariant behind them.
   - Preserve local gotchas, team taste, safety boundaries, irreversible-action gates, and resource-discovery hints.
   - Prefer one canonical home for each instruction. Repeat it only when independent enforcement or unavoidable loading boundaries justify the duplication, and keep copies synchronized.
   - Resolve contradictions according to precedence, ownership, and edit authority. Report conflicts that cannot be resolved in scope; do not let a lower-scope preference override a higher-scope rule.
   - Separate semantics-preserving cleanup from policy changes. When a proposal weakens, strengthens, or removes an explicit requirement, label it as an owner decision and preserve current behavior until it is approved.

5. Rewrite for judgment.

   - State the desired outcome and decision criterion, then allow the approach to adapt to the task.
   - Use soft defaults such as “prefer” or “usually” for contextual choices. Reserve absolute language for invariants, safety, legality, or explicit user requirements.
   - Replace exhaustive branches with the distinction that should govern the choice.
   - Use one term per concept and match the surrounding project's language.
   - Add examples only when an interface or decision rule cannot remove the ambiguity. Keep them varied and explicitly illustrative.

6. Improve interfaces before writing tutorials.

   - Make names, types, parameters, allowed states, defaults, and error results communicate correct use.
   - Keep operation-specific behavior beside the operation rather than repeating it in global guidance.
   - Prefer interfaces that make invalid states difficult to express and results easy to verify.

7. Design progressive disclosure.

   - Keep the entry file as a short router plus the essential workflow.
   - Move specialized detail out only when it is substantial and often irrelevant; do not fragment short, tightly related guidance.
   - Link every optional resource directly from the entry file and state when to load it.
   - Prefer high-fidelity references such as executable tests, source code, structured specifications, mockups, and rubrics over prose that restates them.

8. Validate the assembled context.

   - Read all applicable layers together and check precedence, conflicts, gaps, and repetition.
   - Apply the deletion test: if removing a sentence is unlikely to change behavior or prevent a real failure, remove it.
   - Apply the retrieval test: confirm that a fresh agent can discover deeper guidance at the moment it becomes relevant.
   - Confirm that simplification preserved every necessary boundary and did not widen permissions.
   - For consequential or complex changes, run representative tasks using only the context a fresh agent would receive. Do not disclose the intended answer during validation.

## Deliverable

Return the smallest artifact that makes the improvement reviewable:

- For an audit, provide prioritized findings with exact locations, a keep/move/delete/replace decision, and unresolved conflicts.
- For an authorized edit, provide the revised context or patch plus the checks performed.
- For new context, deliver the context itself and a brief placement rationale; avoid a separate design essay unless requested.

## Typical Requests

- “Audit our repository instructions for conflicts and unnecessary rules.”
- “Decide what belongs in shared instructions, a skill, a tool description, memory, or a reference.”
- “Simplify this skill while keeping its safety guarantees and specialist knowledge discoverable.”

## Quality Bar

Before finishing, confirm that every retained line changes behavior, prevents a known failure, preserves a boundary, or helps locate relevant detail; uncommon information stays discoverable without being loaded by default; and the final context is coherent without requiring its author to explain it.

## Reference

Consult the [source article](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) only when deeper rationale or provenance is needed.
