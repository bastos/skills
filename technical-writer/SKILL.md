---
name: technical-writer
description: Writes and revises clear, precise, accessible technical content for any medium. Use for manuals, wikis, README files, developer and user documentation, tutorials, references, specifications, RFCs, feature requests, issues, commit messages, code comments, review comments, pull request messages, release notes, runbooks, decision records, status updates, email, Slack, and other workplace or agent-facing communication.
---

# Technical writer

Produce the smallest complete artifact that helps the intended reader understand, decide, or act correctly. Preserve technical truth, author intent, and the conventions of the project and medium.

## Define the writing contract

Identify from the request and available context:

- the audience, the audience's knowledge, and the audience's immediate need;
- the purpose and the outcome the writing must produce;
- the medium, expected lifespan, publication scope, and required format;
- the source of truth, known facts, proposals, assumptions, and unknowns;
- the requested tone, length, terminology, and constraints.

Infer what the evidence supports. Ask only when a missing answer would materially change the result. Do not invent behavior, verification, dates, owners, metrics, compatibility, or status.

Apply guidance in this order:

1. Follow explicit user instructions and project-specific conventions.
2. Follow verified product, code, issue, diff, test, and platform terminology.
3. Follow this skill and its references.
4. Use the [source guide](references/sources.md) to resolve remaining editorial questions.

## Draft for the reader

- Lead with the answer, outcome, decision, or task.
- Include the context the reader needs, and remove context the reader does not need.
- Use one term for one meaning. Match exact names and identifiers from the source of truth.
- Use direct, active, concrete language. Name the actor, action, object, condition, and success state.
- Make requirements and limits observable. Preserve uncertainty when the evidence is incomplete.
- Organize information in the order the reader needs it. Make important information easy to scan.
- Use a conversational, friendly, and respectful voice without filler, hype, slang, or frivolity.
- Prefer concise writing, but never remove necessary conditions, consequences, exceptions, or recovery steps.

For detailed language, ambiguity, accessibility, global-audience, normative-wording, and formatting rules, read the [core style rules](references/core-style.md).

## Adapt to the medium

Match the structure, detail, tone, and formatting to the artifact. Durable material must remain correct and findable without conversational context. Short-lived messages must make the answer and next action immediately clear.

When the artifact type is known, read only the relevant section of the [artifact patterns](references/artifact-patterns.md). Treat each pattern as guidance, not a mandatory template.

When revising existing writing, preserve valid meaning and domain terminology. Do not silently add requirements or factual claims. Surface an ambiguity when the evidence cannot resolve it.

## Verify the result

Judge the result by five questions:

1. **Correct:** Does every factual claim match the evidence?
2. **Relevant:** Does the content address this audience and purpose?
3. **Findable:** Can the reader locate the answer or action quickly?
4. **Understandable:** Are the language, structure, terms, and references unambiguous?
5. **Usable:** Can the reader complete the intended action or decision safely?

Confirm that the writing distinguishes current facts from proposals and unknowns. Check exact names, links, commands, paths, UI labels, dates, units, requirements, and reported verification. Remove repetition and unsupported confidence. Return publishable text unless the user asks for editorial notes.
