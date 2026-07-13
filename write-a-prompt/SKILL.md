---
name: write-a-prompt
description: Creates a copy-ready prompt from a rough request, notes, source material, or the current conversation using OpenAI's prompting guidance. Use when the user invokes $write-a-prompt or /write-a-prompt, types a common misspelling such as /write-a-promopt or /wite-a-prompt, asks to "write a prompt for me," asks to turn the conversation into a prompt, or wants a prompt tailored for Chat, ChatGPT Work, or Codex. It writes the prompt without performing the underlying task.
---

# Write a Prompt

Turn the user's intent and available context into one prompt they can paste into a new task. Do not execute the task described by that prompt.

Treat OpenAI's [Prompting guide](https://learn.chatgpt.com/docs/prompting) as the source of truth. Read the current page when web access is available and current guidance matters. Do not block prompt writing when the page is unavailable; follow the principles below.

## Workflow

1. Determine the target surface.

   - Use Chat for questions, ideas, short drafts, and everyday decisions.
   - Use Work for multi-source, tool-using, multi-step, or larger deliverables.
   - Use Codex for codebases, code changes, debugging, tests, and developer tools.
   - Follow an explicitly named target. Otherwise infer it from the request without asking unless the choice materially changes the prompt.

2. Extract only context that can change the result.

   - Carry forward relevant requirements, decisions, examples, reproduction steps, file paths, constraints, and unresolved facts from the conversation.
   - Make the prompt self-contained when the target will not have access to this conversation.
   - Name useful files, images, connected sources, or tools and say what to take from each.
   - Omit irrelevant dialogue, obsolete directions, raw secrets, and unsupported assumptions.

3. Write from the result the user needs. Add only the useful parts:

   - Goal: state the outcome first.
   - Context: include information or sources that affect the result.
   - Output: specify the audience, format, length, or detail level when useful.
   - Boundaries: preserve the one or two constraints that prevent real problems.
   - Verification: request a final check proportional to the task's importance.

   Do not force these parts into headings or a rigid template. A short prompt is preferable when it is sufficient. Describe process only when the process itself matters.

4. Tailor the prompt to the task.

   - For current information, request web search and source links.
   - For Work, name the reviewable deliverable, relevant sources, audience, and approval boundary before sending, publishing, or changing shared information.
   - For Codex, include the desired behavior, relevant code or reproduction, important compatibility constraints, and how to verify the change. Ask for a plan first only when the approach needs review.
   - For important outputs, ask the target to flag missing or conflicting information instead of guessing.

5. Resolve gaps conservatively.

   Ask at most one concise clarification only when the missing answer would materially change the prompt and cannot be inferred. Otherwise make a reasonable assumption or use a clearly labeled placeholder.

6. Return the deliverable.

   Output only the finished prompt in one fenced code block unless the user asks for rationale, variants, or another format. Match the user's language. Do not preface the block with analysis.

## Quality Check

Before responding, confirm that the prompt:

- is self-contained for its intended target
- leads with the requested result
- includes relevant context without replaying the whole conversation
- preserves material boundaries without micromanaging every step
- asks for an appropriate output and final verification
- contains no invented facts, hidden assumptions, or exposed secrets
- clearly asks the next agent to do the task rather than to write another prompt

## Examples

### Hand Off a Bug Fix

Input:

```text
/write-a-prompt based on this conversation to fix the bug
```

Expected behavior: synthesize the bug symptoms, reproduction evidence, relevant paths, prior findings, change boundaries, and validation expectations from the conversation into a standalone Codex prompt. Return the prompt only; do not fix the bug.

### Research a Reversible Workplace Experiment

Input:

```text
/write-a-prompt help me decide whether our 18-person remote design studio should test a four-day workweek
```

Output:

```text
Research whether an 18-person remote design studio should run a four-day-workweek experiment. Use current, credible sources and distinguish measured evidence from opinion or inference.

Deliver a concise decision memo that summarizes likely benefits, risks, operational constraints, and the kinds of teams for which published results may not generalize. Recommend whether to proceed. If the evidence supports a test, propose a reversible eight-week pilot with scope, workload safeguards, employee and client communication drafts, success metrics, baseline data, weekly check-ins, and explicit stop conditions.

Flag assumptions and missing company-specific information instead of guessing. Do not announce a policy, contact employees or clients, or change calendars; prepare the memo and pilot plan for leadership review only. Link every material factual claim to its source and finish by checking that the recommendation follows from the evidence.
```

### Turn Session Context into an Experiment

Input:

```text
/write-a-prompt use the context of this session to create a tailored prompt to run the experiment we discussed
```

Expected behavior: extract the specific hypothesis, current baseline, relevant files or implementation seam, benchmark commands, constraints, and success or rejection criteria established during the session. Turn them into a self-contained prompt for a reversible experiment that measures before and after, reports comparable evidence, keeps only a demonstrated improvement, and removes rejected experiment code. Do not tell the next agent to "use this session," because it may not have access to the original conversation.
