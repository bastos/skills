---
name: send-to-minion
description: Use this skill only when the user explicitly invokes $send-to-minion, /send-to-minion, or explicitly asks to delegate a prompt to one minion, helper, worker, child agent, spawned agent, subagent, Claude Code agent, or other single delegated agent. It sends the user's prompt to exactly one subagent using the current runtime's delegation tools, coordinates follow-up with the runtime's messaging/resume tools, verifies the result, and returns the parent agent's final answer.
---

# Send to Minion

Delegate the user's prompt to exactly one helper agent, called the minion, then supervise it until completion.

Treat explicit invocation of `$send-to-minion` or `/send-to-minion` as explicit user permission to spawn one subagent. Do not use this skill implicitly for ordinary requests that merely need research, depth, or careful execution.

## Contract

- Spawn exactly one subagent for the user's task.
- Do not spawn multiple agents, use CSV fan-out, or ask the minion to spawn nested agents.
- Keep the parent agent responsible for orchestration, verification, cleanup, and the final user response.
- Let the minion do the substantive delegated work.
- Preserve the user's original goal, constraints, language, and requested output format.
- Close the minion after completion, failure, or cancellation unless the runtime has already closed it.
- Do not silently downgrade to parent-only execution. If no subagent mechanism is available, say so.

## Runtime Selection

Use the native subagent mechanism for the current runtime. Do not mix runtimes in one invocation.

Prefer this order:

1. Codex multi-agent tools when `spawn_agent` is available.
2. Claude Code subagents when the `Agent` tool is available.
3. A legacy/adapted subagent runner such as `Task` only when neither of the above names is exposed but the runtime clearly documents it as the subagent tool.

If no subagent mechanism exists, follow Failure Handling.

## Codex Tool Setup

Use Codex multi-agent tools when available:

- `spawn_agent`
- `send_input`
- `resume_agent`
- `wait_agent`
- `close_agent`

If these tools are not visible and `tool_search` is available, search for multi-agent tools before concluding delegation is unavailable.

Use Codex built-in agent types this way:

- `worker`: implementation, edits, tests, fixes, or other concrete execution.
- `explorer`: read-heavy investigation, repository mapping, diagnosis, or research.
- `default`: mixed tasks or when no specialized type fits.

Do not set a model override unless the user asks for one or there is a clear task-specific reason. Prefer inheriting the parent model, sandbox, approvals, and runtime overrides.

## Claude Code Tool Setup

Use Claude Code's `Agent` tool when available. It runs a subagent in an isolated context and returns the subagent's result to the main conversation.

Use Claude built-in subagents this way:

- `general-purpose`: implementation, edits, tests, fixes, or mixed multi-step tasks.
- `Explore`: read-only codebase exploration, file discovery, search, and diagnosis.
- `Plan`: planning-mode research when the runtime is already in plan mode.

If a project or plugin exposes a better custom Claude subagent, use it only when the user names it or the task clearly matches its description.

Claude Code may support resuming or steering a previous subagent through `SendMessage`. Use that only for the single minion spawned for this task. Do not spawn a replacement unless the first minion cannot be resumed and a fresh run is the only way to satisfy the user's explicit delegation request.

Prevent nested delegation in Claude by instructing the minion not to use the `Agent` tool or spawn other subagents. When using a custom Claude subagent configuration under your control, prefer omitting `Agent` from its tools or adding it to `disallowedTools`.

## Workflow

1. Extract the task.

   Keep the user's original prompt intact. Add only relevant surrounding context, constraints, file paths, and output requirements needed for the minion to succeed.

2. Spawn one minion.

   In Codex, call `spawn_agent` once. Omit `fork_context` by default and pass a complete task packet in `message` or `items`. Use `fork_context: true` only when conversation history is essential and safe to share.

   In Claude Code, call `Agent` once with the closest built-in or custom subagent. Use `general-purpose` for work that may edit files, `Explore` for read-only investigation, and a named custom subagent only when appropriate.

3. Give the minion a complete task packet.

   Include:

   - the original user request
   - constraints and allowed write scope
   - expected output format
   - whether tests or validation should be run
   - an instruction not to spawn more agents
   - a request to report files changed, commands run, validation results, and remaining risks

   Suggested packet:

   ```text
   You are the minion for this task. Do the substantive work and report back.

   Original user request:
   <paste request>

   Constraints:
   - Do not spawn additional agents or use any subagent delegation tool.
   - Preserve the user's requested language and output format.
   - Make the smallest defensible change when editing.
   - Avoid unrelated changes and do not revert changes made by others.
   - Report files changed, commands run, validation performed, and remaining risks.

   Return a concise final result for the parent agent to verify and deliver.
   ```

4. Wait for the result.

   In Codex, use `wait_agent` because this skill's final answer depends on the minion result. Prefer a longer timeout over repeated short polling.

   In Claude Code, wait for the `Agent` result in the main conversation. If the subagent runs in the background, monitor it through the runtime's agent view or equivalent until it returns.

5. Steer only when useful.

   In Codex, use `send_input` when the minion is blocked, needs a correction, needs another constraint, or produced incomplete work. Use `interrupt: true` only to stop an actively wrong direction.

   Use `resume_agent` only when the agent was closed and must be reopened before sending input or waiting again.

   In Claude Code, use `SendMessage` or the runtime's resume mechanism to continue the same minion when it needs a correction or follow-up. Do not start a second subagent for a corrective pass while the original one can still be reached.

6. Handle clarification.

   If the minion asks a question and the answer can be inferred from the prompt or project context, answer it with `send_input`, `SendMessage`, or the runtime's equivalent. If the answer truly requires the user, stop and ask the user directly.

7. Verify and close.

   Inspect the minion's final response against the user's request. Check relevant files, diffs, commands, or validation results when the task changed local state. In Codex, call `close_agent` after collecting the result or deciding the attempt failed. In Claude Code, close, stop, or let the subagent finish cleanly according to the available runtime controls; do not leave a resumable minion active when the task is done.

8. Respond as the parent.

   Return a clean final answer. Summarize what was done, validation, and any residual risk. Do not paste raw minion logs unless the user asked for logs.

## Failure Handling

If no subagent tool exists, say:

```text
I could not use send-to-minion because this runtime does not expose a subagent tool. I can still do the task directly, but that would not satisfy the one-minion delegation contract.
```

Then continue locally only if the user clearly wants progress over strict delegation.

If the minion fails, times out, or returns incomplete work, use `send_input`, `SendMessage`, or the runtime's equivalent once with a precise correction:

```text
Your result is incomplete. Finish the missing part, keep the original constraints, and return only the final deliverable plus validation notes.
```

If it still fails, close the minion and report what was completed, what failed, what remains, and the safest next step.

## Optional Codex Configuration Notes

Do not edit configuration unless the user asks. If the user wants to configure this pattern, keep subagent nesting disabled with `agents.max_depth = 1` and avoid raising it for this skill. Use `agents.max_threads = 1` only when the user wants to enforce a single open subagent thread across the session.

## Optional Claude Code Configuration Notes

Do not edit configuration unless the user asks. If the user wants a Claude-native variant, this skill can remain a normal skill invoked as `/send-to-minion`. For a forked-skill variant, Claude Code supports `context: fork` and `agent: <name>` frontmatter, but that makes the whole skill body become the subagent task. Use that only if the user wants `/send-to-minion <arguments>` to always run inside a Claude subagent without parent-side orchestration.
