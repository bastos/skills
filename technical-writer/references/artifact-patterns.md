# Artifact patterns

Read only the section for the requested artifact. Use headings that help the reader; do not force the writing into a template.

## Contents

- [Documentation systems](#documentation-systems)
  - [Manual](#manual)
  - [Wiki page](#wiki-page)
  - [README or overview](#readme-or-overview)
  - [Diataxis documentation](#diataxis-documentation)
  - [Troubleshooting guide](#troubleshooting-guide)
- [Engineering records](#engineering-records)
  - [Commit message](#commit-message)
  - [Code comment or documentation comment](#code-comment-or-documentation-comment)
  - [Feature request or issue](#feature-request-or-issue)
  - [RFC or technical specification](#rfc-or-technical-specification)
  - [Pull request title and description](#pull-request-title-and-description)
  - [Release note](#release-note)
  - [Runbook](#runbook)
  - [Decision record](#decision-record)
  - [Review comment](#review-comment)
- [Workplace communication](#workplace-communication)
  - [Slack or workplace thread reply](#slack-or-workplace-thread-reply)
  - [Email](#email)
  - [Status update or handoff](#status-update-or-handoff)
- [Rewrite or edit](#rewrite-or-edit)

## Documentation systems

### Manual

Design a manual as a maintained system, not one long article.

1. Define the product, supported versions, audience, scope, and assumptions.
2. Give readers a map of the product and the manual.
3. Separate setup, common tasks, reference, troubleshooting, maintenance, and support information.
4. Put safety warnings, permissions, destructive effects, and prerequisites before the relevant action.
5. Use consistent chapter and procedure structures.
6. Provide observable results and recovery paths for procedures.
7. Add a glossary, index, or cross-links when terminology or scale requires them.
8. Identify version-specific behavior and remove stale instructions.

Prefer one canonical explanation for each concept. Link to the canonical explanation instead of maintaining conflicting copies.

### Wiki page

Make each page answer a recognizable question or document one bounded subject.

- Use likely search terms in the title and opening paragraph.
- State the page's scope and intended reader immediately.
- Lead with the current answer, decision, or procedure. Do not lead with meeting history.
- Link to canonical sources with descriptive link text.
- Avoid duplicating volatile facts across pages.
- Record an owner, status, or last-verified date when the wiki supports maintenance metadata.
- Mark historical pages and superseded decisions clearly.
- Connect the page to parent topics and related workflows without creating link lists that lack context.

### README or overview

Help a new reader determine what the project is, whether it is relevant, and how to begin.

Include, as applicable:

1. purpose and current status;
2. primary capabilities and boundaries;
3. prerequisites and the shortest working setup;
4. a minimal usage example with an expected result;
5. links to detailed documentation, contribution guidance, support, and licensing.

Keep volatile details in their canonical source. Do not turn the README into a complete manual.

### Diataxis documentation

Choose one primary reader need per page:

- **Tutorial:** teach a beginner through a successful learning experience.
- **How-to guide:** help a competent reader complete a specific task.
- **Reference:** describe a system accurately and consistently.
- **Explanation:** build understanding of concepts, reasons, or tradeoffs.

Split mixed material into distinct pages or clearly labeled sections.

#### Tutorial

Create a safe, repeatable learning path that reaches a visible result. List minimal prerequisites, guide the reader through complete tested steps, explain only what is necessary to continue, and confirm the result. Do not turn the tutorial into an exhaustive option reference.

#### How-to guide

Name the outcome, state prerequisites and limits, give the shortest reliable procedure, and include verification and recovery where failure is plausible. Assume the reader has the relevant background.

#### Reference

Organize material by the structure of the system. Use consistent entries for parameters, types, defaults, return values, errors, permissions, limits, and examples. Keep instruction and opinion secondary.

#### Explanation

Establish context, connect causes and effects, compare alternatives fairly, and state boundaries. Link to how-to guides for actions and reference pages for exact details.

### Troubleshooting guide

Organize around symptoms that readers can observe.

For each symptom, provide:

1. the exact symptom or error;
2. likely causes in diagnostic order;
3. safe checks that distinguish the causes;
4. the corrective action for each confirmed cause;
5. the expected result;
6. escalation criteria and evidence to collect.

Separate diagnosis from repair. Do not tell readers to mutate or delete state before confirming the cause and recovery path.

## Engineering records

### Commit message

Derive the message from the staged change. Follow the repository's commit convention.

- Summarize one logical change and its outcome.
- Use an imperative summary when the project does not specify another style.
- Add a scope only when the scope helps readers classify the change.
- Use the body for motivation, user-visible behavior, constraints, or consequences that the summary cannot carry.
- Use issue links, breaking-change notices, co-author lines, and other trailers according to project convention.
- Do not list every changed file or claim verification that the commit does not establish.

If the project uses Conventional Commits, use `type(scope): description`. Choose the type from the actual change, not from the ticket label.

### Code comment or documentation comment

Write a code comment only when the code cannot communicate the necessary reason, constraint, invariant, risk, or non-obvious behavior.

- Explain *why* the code exists or why the obvious alternative is unsafe.
- Do not translate the next line of code into prose.
- Keep names, behavior, and examples synchronized with the implementation.
- Document public APIs in the language's standard form. Cover contracts, parameters, returns, errors, side effects, concurrency, and availability when relevant.
- Tie a TODO or FIXME to a specific condition, issue, or removal criterion.
- Do not put secrets, personal data, speculation, or transient debugging notes in comments.

### Feature request or issue

Use this order when applicable:

1. **Title:** name the user-visible outcome or defect.
2. **Problem:** identify the affected user, current behavior, and impact.
3. **Evidence:** include reproduction, examples, metrics, or source references.
4. **Desired outcome:** describe the needed capability without prescribing unnecessary implementation.
5. **Requirements or acceptance criteria:** make each item observable and testable.
6. **Constraints and non-goals:** define the boundary.
7. **Open questions:** list only unresolved decisions.

Separate facts from hypotheses. For bugs, include expected behavior, actual behavior, reproduction conditions, and environment details. Do not claim severity or priority without evidence or project policy.

### RFC or technical specification

Include, as applicable:

1. status, authors, reviewers, and decision deadline;
2. summary and motivation;
3. goals and non-goals;
4. terminology;
5. current state and constraints;
6. proposed design and user-visible behavior;
7. alternatives and tradeoffs;
8. compatibility, migration, rollout, and rollback;
9. security, privacy, accessibility, localization, and operations;
10. testable requirements and acceptance criteria;
11. unresolved questions and decision record.

Use BCP 14 keywords only when the artifact defines normative obligations. Give each requirement a stable identifier when reviewers or tests need to reference it.

### Pull request title and description

Derive the message from the actual diff and verification evidence.

- **Title:** summarize the outcome in the project's preferred convention.
- **Why:** state the problem or goal.
- **What changed:** group meaningful behavior changes; do not narrate every file.
- **Verification:** list only checks that ran, with exact results where useful.
- **Risk and rollout:** state compatibility, migration, flags, monitoring, or rollback needs.
- **Links:** connect the issue, design, evidence, or follow-up work with descriptive text.

Call out skipped checks, known limitations, screenshots, breaking changes, and reviewer-sensitive areas. Do not write `all tests pass` when only a focused test ran.

### Release note

Address the affected user. Lead with the benefit or behavior change. State any required action, compatibility boundary, migration, deprecation, or known issue. Omit internal implementation detail unless the detail affects use. Do not announce an unapproved future feature.

### Runbook

Optimize for safe execution under pressure:

1. scope and trigger;
2. owner and required access;
3. preconditions and safety checks;
4. numbered actions with exact commands;
5. expected output after consequential steps;
6. stop conditions, rollback, and escalation;
7. verification and evidence capture.

Separate commands that mutate state from read-only diagnostics. Never use a placeholder that could be mistaken for a literal production identifier.

### Decision record

Record the context, decision, status, date, decision makers, considered alternatives, consequences, and follow-up triggers. Describe the decision, not the meeting chronology. Mark a superseded decision and link to the replacement.

### Review comment

State the observable concern first. Explain the consequence. Point to the exact location or behavior. Suggest the smallest viable correction when known. Distinguish blockers, recommendations, questions, and optional polish. Keep the comment about the artifact, not the author.

## Workplace communication

### Slack or workplace thread reply

Answer the question in the first sentence. Add only the context needed to trust or act on the answer. Use short paragraphs or bullets. Include exact owners, actions, dates, and links when relevant. Mark uncertainty and proposals explicitly.

For a decision, finish with the decision and next owner. For a request, finish with the requested action and deadline. For a status update, state outcome, evidence, blocker, and next step. Link to the durable source of truth instead of reproducing a full specification.

### Email

Use a subject line that states the topic and requested action. Put the purpose and request in the opening paragraph. Separate background from action items. Name owners and deadlines. Preserve enough context for recipients who did not participate in earlier conversations. End with the next step, not a generic invitation when a specific response is needed.

### Status update or handoff

State:

1. the outcome or current state;
2. completed work and evidence;
3. remaining work;
4. blockers or risks;
5. the next action, owner, and required context.

Distinguish a local result from a published or deployed result. Link to durable artifacts. Do not make the next person reconstruct identifiers, commands, or decisions from conversation history.

## Rewrite or edit

Preserve the original meaning and valid domain terminology. Correct ambiguity, structure, tone, and formatting. Do not silently add requirements or factual claims. If the original admits two materially different meanings, surface the ambiguity or choose only when the evidence resolves it.
