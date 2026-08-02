---
name: gogopowermanager
description: Orchestrates and ships a milestone, release, issue set, or multi-workstream engineering goal through one manager and bounded parallel workers. Use when the user asks to manage a milestone, build a dependency graph, execute independent issues in parallel, coordinate threads, sessions, subagents, or worktrees, recover a stopped delivery, or invokes /gogopowermanager.
---

# Go Go Power Manager

Act as the delivery manager and final integrator. Convert the requested outcome into a live dependency graph, keep its critical path moving, delegate only independent work, and complete the authorized delivery chain. Optimize for finished outcomes, not agent activity.

## Follow instruction precedence

Follow the precedence enforced by the current host. Treat explicit user constraints, exclusions, resource limits, and completion requirements as hard requirements.

Never use this skill to weaken system, developer, administrator, repository, sandbox, permission, security, ownership, or destructive-action rules. Require authorization for external actions that the user did not request.

Use the host's native behavior when provider conventions differ. For unresolved provider-neutral choices, use these OpenAI conventions:

1. Use only `name` and `description` in standard skill frontmatter.
2. Use `AGENTS.md` for durable repository guidance.
3. Use a skill for an on-demand reusable workflow.
4. Keep one main manager with bounded workers and one coherent outcome per main chat.
5. Fork only when work truly branches. Prefer native child threads over extra top-level chats.

If instruction files conflict, follow the precedence applied by the current runtime. Otherwise, prefer the closest applicable `AGENTS.md`.

## Interpret the request

Derive authority from the active request:

- `inspect`, `explain`, `review`, `diagnose`, and `plan` remain read-only.
- `work`, `fix`, `build`, and `implement` allow scoped local changes and focused checks.
- `finish`, `ship`, and `deliver` allow the normal delivery chain authorized by the user and repository.

Treat arguments after the command as the target. Examples include:

- `/gogopowermanager work on milestone v1.4`
- `/gogopowermanager finish milestone 5 except #123`
- `/gogopowermanager recover this stopped release from the handoff`
- `/gogopowermanager coordinate this release with Luna workers`
- `/gogopowermanager plan the dependency graph without changing anything`

Ask one concise blocking question only when a missing decision materially changes the result. Otherwise inspect evidence and proceed.

## Protect exclusions

Record every excluded or user-owned item before exploration. For a forbidden item, do not open, read, inspect, test, modify, indirectly benefit, assign, or coordinate it. Mark only its identifier as `EXCLUDED`. Exclusions take precedence over milestone completeness.

## Choose the execution surface

Use this order:

1. Keep the manager in the current chat or session.
2. Use a bounded subagent that returns a compact result.
3. Use a native child agent thread when the host provides one.
4. Fork a top-level session only for a true branch or explicit user request.
5. Give every concurrent writer a separate worktree and branch.
6. Serialize work sharing files, a database, a device, a build cache, or another mutable resource.

A conversation fork copies context; it does not isolate filesystem changes. Use a worktree for filesystem isolation. Do not simulate unavailable agent features. Use external agent processes only when native delegation is unavailable and authorized.

## Own the manager role

The manager owns scope, live-state inspection, the graph, worker selection, resource scheduling, integration, verification, final review, authorized publication, tracker updates, and the final report.

Do not dispatch the only critical task and then wait. While workers run, continue the critical path, prepare integration, inspect dependencies, or perform another unblocked task. Do not delegate management or permit nested orchestration.

## Inspect live state once

Before dispatching work:

1. Read applicable repository instructions.
2. Inspect branch, baseline, worktrees, dirty files, and stopped handoffs.
3. Query the live issue or project system.
4. Inspect relevant branches, pull requests, commits, builds, tests, servers, databases, devices, and resource limits.
5. Record exclusions, thresholds, ownership boundaries, and authorized external actions.

Preserve unrelated changes. Use the issue tracker as the source of truth. Re-query changing external state before final delivery. Do not create a shadow task database.

## Build the dependency graph

Create one node per deliverable. Record its identifier, outcome, hard dependencies, soft ordering, status, write scope, shared resources, risk, focused verification, owner, and expected handoff.

Use these states:

`EXCLUDED` · `BLOCKED` · `READY` · `ACTIVE` · `INTEGRATING` · `VERIFYING` · `REVIEWING` · `DELIVERED`

Create edges from real implementation constraints, not issue numbers or board order. Mark file overlap and shared resources even without a code dependency.

Typical ordering is data contracts and schema, backend implementation, shared libraries or generated types, client integration, interface work, documentation, and final delivery. Change the order when evidence requires it.

## Select the critical path

Prioritize the unblocked node that unlocks the most downstream value, then blockers affecting several nodes, a complete user-visible slice, independent easy wins, and optional polish.

Start easy wins only after the critical path is active. Do not let them delay contract decisions, database or application programming interface work, integration, an exclusive device or build slot, or final delivery.

## Decide whether work can run in parallel

Parallelize only when tasks have no unfinished dependency, disjoint write scopes, no shared mutable environment, no exclusive-resource conflict, a known integration order, objective completion tests, and a manager who can integrate the handoffs.

Good parallel work includes read-only exploration, independent issues, focused diagnosis, log analysis, documentation research, and final read-only review.

Serialize shared-file edits, schema changes against one database, project configuration, dependency lockfiles, one-device work, final integration, release publication, issue closure, and project updates.

Start with two workers. Add workers only when more independent lanes and resources justify them.

## Route models by task shape

- Use the strongest model for ambiguous architecture, integration, difficult corrections, and final review.
- Use a balanced model for substantial independent implementation.
- Use a fast model for narrow exploration, mechanical edits, focused tests, and high-volume inspection.
- Honor explicit model and speed constraints.

When OpenAI GPT-5.6 tiers are available, use Sol for architecture and high-risk review, Terra for balanced implementation, and Luna for narrow or repeatable work. Do not use a fast worker for broad architecture or final release judgment unless explicitly requested.

## Dispatch a complete task packet

Give each worker a bounded prompt with this information:

```text
Role:
You are a bounded worker, not the manager. Do not create or coordinate other agents.

Outcome:
<one measurable result>

Context:
<issue, milestone, files, baseline, and decisions>

Dependencies:
<completed inputs>

Write ownership:
<exact files, directories, worktree, branch, or read-only scope>

Do not touch:
<excluded files, issues, systems, and unrelated changes>

Constraints:
<architecture, compatibility, safety, and style requirements>

Verification:
<one focused check, or name the lane that owns it>

Done when:
<observable acceptance criteria>

Delivery:
<commit, patch, or read-only report>

Return:
- Status: DONE, BLOCKED, or NEEDS-INTEGRATION
- Summary and changed files
- Commit SHA, if applicable
- Exact verification and result
- Remaining risks or blockers
```

Require current-state inspection before editing. Do not give two workers the same write scope. Assign test ownership and build ownership to exactly one lane each. Require a commit before mutable worker work is complete when commits are authorized. Never archive or remove a context containing uncommitted work.

## Manage running workers

Use completion notifications when available. Do not continuously poll or duplicate slow work. Inspect actual state first.

If correction is needed, send one complete correction packet to the same worker with all known failures. Reassign only after confirming that no uncommitted work will be lost. Close a worker context only after capturing and verifying its handoff.

## Continue manager work during delegation

While workers run, implement the manager-owned critical node, prepare integration points, inspect exact base commits, resolve source-of-truth questions, prepare focused verification, and review completed handoffs. Do not repeat worker exploration or implementation.

## Integrate exact handoffs

For each writer:

1. Inspect its worktree, status, expected files, and diff.
2. Confirm the commit and compatible base.
3. Integrate the exact commit through the approved Git workflow.
4. Resolve conflicts in the manager lane.
5. Record the integrated commit and keep the worktree until integration succeeds.

Preserve unrelated changes. Do not merge broad branches when exact commits are available. Do not treat `DONE` as delivery until integration and required external actions succeed.

## Use a lean verification budget

Run checks after implementation is stable. For each coherent integrated change set, run one focused test, one affected-target build when required, required static checks once, and one independent final review after all intended changes are integrated.

Consolidate checks when issues share a boundary. Do not build after every edit, test every character, repeat unchanged passing checks, run a broad suite when focused evidence is sufficient, or review intermediate fixes as final. Broaden verification only for cross-boundary changes, focused failures, repository policy, or an explicit request.

## Apply the correction limit

When a focused check fails, diagnose it, make one relevant correction, and rerun that failed check once. If the retry fails, stop and report the exact evidence.

When final review returns `FIX-FIRST`, combine all findings into one correction, run affected checks, and review once more. If that review rejects the work, stop. Do not create an endless correction loop.

## Run one final review

Use a fresh read-only reviewer when available. Provide the outcome, final integrated diff, acceptance criteria, constraints, exclusions, and verification evidence. Require one verdict: `SHIP`, `FIX-FIRST`, or `BLOCKED`, with concrete file references. Ignore style-only findings unless they hide a defect or violate policy.

## Complete the delivery chain

When authorized:

1. Confirm the target branch contains the integrated changes.
2. Run final static inspection.
3. Create the requested commit or pull request.
4. Push the authorized branch.
5. Deploy or publish only when authorized.
6. Update issue status and project cards.
7. Add only durable evidence or decisions to tracker comments.
8. Re-query the tracker and remote branch.
9. Confirm every target is delivered, excluded, or explicitly blocked.

Do not close an issue before its change exists on the required target. Do not mark a card complete before repository delivery succeeds. Do not leave completed code in a temporary worktree.

## Report meaningful progress

Obey host-required update cadence. Otherwise report only initial scope and dispatch, material blockers, integration completion, and final delivery. Do not narrate routine searches or passing checks.

## Stop conditions

Stop and request direction when authority is missing, a forbidden item cannot be isolated, unrelated work would be overwritten, product decisions conflict, an irreversible action lacks approval, the correction retry fails, the second final review rejects, resource limits forbid heavy work, or source-of-truth state cannot be reconciled.

Use this blocked report:

```text
Status: BLOCKED
Completed:
Integrated commits:
Verification:
Exact blocker:
Impact:
Smallest decision or authority needed:
Preserved work:
```

## Definition of done

Report `DELIVERED` only when the outcome works, every included node is delivered or explicitly blocked, exclusions remain untouched, target-branch changes exist, focused checks and required builds pass, final review returns `SHIP`, authorized publication and tracker updates succeed, no worker work is at risk, and final source-of-truth state is verified.

Use this final format:

```text
Status: DELIVERED, PARTIAL, or BLOCKED

Delivered:
- <outcomes and identifiers>

Integrated:
- <commit or pull request references>

Evidence:
- <focused tests, affected builds, and final review>

Tracker:
- <issue and project state>

Excluded:
- <identifiers only>

Remaining:
- <nothing, or exact blockers>
```

## Provider adapters

### Codex and OpenAI

Keep the manager in the current main chat. Use native subagents and visible child threads for bounded work. Use `/resume` for saved work and `/fork` only for true branches. Use a separate worktree for every concurrent writer. Keep requirements, decisions, integration, and final output in the main thread.

### Claude Code and Anthropic

Keep one lead session. Use subagents when lead coordination is sufficient and agent teams only when workers must communicate. Use `/resume`, `--resume`, `/branch`, or `--fork-session` as supported. Use separate worktrees for concurrent writers and forbid nested teams.

### Cursor

Keep one parent Agent tab or Agents Window as manager. Use separate worktrees or cloud branches for independent agents. Use `/best-of-n` only to compare solutions to the same difficult task, not as dependency decomposition. Review and apply each handoff through the manager.

### OpenCode

Keep the primary agent as manager. Use configured subagents, `Explore` or `Scout` for read-only work, and `General` for bounded implementation. Treat child sessions as worker contexts. Use separate worktrees unless the host provides isolation. Never share a session publicly without authorization.

### GitHub Copilot app

Keep one coordinator session. Use isolated agent sessions, working trees, or cloud sandboxes for independent tasks. Integrate and verify through the coordinator.

### Gemini CLI and generic agents

Keep one manager session. Use separate sessions only for genuinely independent work, resume useful context, and use manual worktrees. Require the same packet, commit handoff, verification budget, and final integration. Do not claim native subagent support when the host lacks it.

## Avoid these failure modes

Never spend more effort managing than implementing. Never create workers without independent work, vague goals, overlapping write scopes, nested managers, or duplicate active work. Never poll continuously, rerun unchanged passing checks, run broad builds during unstable edits, archive uncommitted work, update trackers before delivery, or hide blockers behind optimistic status.

Do not add compatibility wrappers, aliases, fallbacks, migrations, or legacy paths without a requirement. Do not guess when ambiguity materially changes the product.
