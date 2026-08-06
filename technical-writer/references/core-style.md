# Core style rules

Use this reference when drafting or editing any artifact. Apply each rule with judgment; preserve standard syntax, quoted text, legal language, and established product terminology.

## Contents

- [Design the content](#design-the-content)
- [Precision and controlled language](#precision-and-controlled-language)
- [Normative language](#normative-language)
- [Voice and readability](#voice-and-readability)
- [Accessibility and global use](#accessibility-and-global-use)
- [Technical formatting](#technical-formatting)
- [Truth and time](#truth-and-time)
- [Edit in passes](#edit-in-passes)

## Design the content

Start from the reader's question, task, or decision. State the answer or outcome before background unless the background is necessary to interpret the answer safely.

Use progressive disclosure:

1. Give the minimum complete answer or path.
2. Add conditions, consequences, exceptions, and verification near the relevant statement.
3. Link to deeper explanation or reference material instead of interrupting the main path.

Use headings that describe content, not generic labels such as *Overview* or *More information*, when a specific heading is possible. Make each section useful to readers who arrive through search or a direct link.

Put related information together. Keep a rule next to its exception, a command next to its expected result, and a claim next to its evidence. Do not require readers to combine distant fragments to understand one instruction.

Use examples to clarify a pattern or boundary. Keep examples realistic, minimal, internally consistent, and valid for the documented version. State whether placeholder values must be replaced.

## Precision and controlled language

### Keep terms stable

Choose one preferred term for each concept. Do not alternate terms for variety. Match names in the product, code, API, UI, and existing project glossary.

Define an unfamiliar term at first use. Expand an abbreviation at first use unless the audience certainly knows it. Do not use the same term for two different concepts.

### Make actions atomic

Write one action per sentence in procedures. Aim for no more than 20 words in a procedural sentence. Split a sentence when its clauses can succeed, fail, or require permission independently.

Recommended:

1. Create the branch.
2. Run the focused test.
3. Push the branch after the test passes.

Avoid: Create the branch, run the test, and push it if everything looks good.

### Name the actor and object

Use active voice. Use the imperative for reader actions. Name the actor when another system or person acts.

- Reader action: `Select Save.`
- System action: `CI uploads the signed artifact.`
- Team action: `The release manager approves the deployment.`

In instructions, replace cross-sentence pronouns such as *it*, *this*, *that*, and *the above* with the exact noun. Repeat a term when repetition prevents a mistaken reference.

### Remove vague language

Replace subjective or relative terms with observable limits.

| Vague | Precise |
| --- | --- |
| a large file | a file larger than 10 MB |
| retry soon | retry after 30 seconds |
| use a recent version | use version 4.2 or later |
| verify it works | confirm that `GET /health` returns HTTP `200` |

Do not invent a threshold. Identify the missing decision when the source does not provide one.

### Eliminate grammatical ambiguity

- Do not coordinate a negation. Write `Do not commit. Do not push.`
- Repeat distributed modifiers. Write `expired access tokens and expired refresh tokens` when *expired* applies to both.
- Put each condition before the instruction that depends on it.
- Keep an exception next to the rule it changes.
- Use parallel grammar for parallel items.
- Avoid slash constructions such as `and/or`, `input/output`, or `he/she` when a complete phrase is clearer.

### State the full operational contract

For a consequential step, state:

1. Preconditions: what must already be true.
2. Action: who does what, with exact identifiers.
3. Postcondition: the observable success state.
4. Failure path: what to do when the postcondition is false.

Do not hide permissions, destructive effects, irreversible consequences, or required verification in notes after the procedure.

### Prefer positive direction

Lead with the correct action. Add a separate prohibition only when the wrong action is plausible and consequential.

Recommended: `Use git switch -c <branch>. Do not modify main.`

Avoid: `Don't use the wrong Git command.`

## Normative language

Use the BCP 14 keywords only in requirements, specifications, policies, or acceptance contracts:

- `MUST` or `MUST NOT`: an absolute requirement or prohibition.
- `SHOULD` or `SHOULD NOT`: a strong recommendation with valid exceptions whose consequences must be understood.
- `MAY`: a genuinely optional choice.

When these words are normative, include this notice near the start:

> The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", and "MAY" in this document are to be interpreted as described in BCP 14, RFC 2119 and RFC 8174, when, and only when, they appear in all capitals.

Use normative keywords sparingly. Make every requirement singular, testable, and assigned to an actor. Do not combine different obligation levels in one sentence. In ordinary documentation and conversation, prefer direct natural language.

## Voice and readability

- Sound like a knowledgeable, respectful colleague.
- Lead with useful information. Remove throat-clearing, cheerleading, jokes, clichés, and rhetorical questions.
- Use common, concrete words. Prefer `use` to `utilize` and `start` to `initiate`.
- Avoid idioms, culturally specific references, and most phrasal verbs.
- Use jargon only when it is more precise for the audience. Define necessary jargon.
- Use contractions when they sound natural and cannot cause ambiguity.
- Use standard American English unless the project or user specifies another variety.
- Avoid claims such as *easy*, *simple*, *obvious*, or *just*. Describe the action instead.
- Avoid blaming the reader. Describe the state and recovery action.

## Accessibility and global use

- Organize content with a logical heading hierarchy.
- Make link text meaningful outside its sentence. Avoid `click here`, `this page`, and bare URLs.
- Give informative images concise alt text. Mark decorative images as decorative when the format supports it.
- Do not convey meaning through color alone.
- Avoid directional references such as *above*, *below*, *left*, and *right*. Name the section, control, or item.
- Introduce tables only when relationships are easier to scan in rows and columns. Keep headers explicit.
- Use captions or surrounding text to explain diagrams and screenshots.
- Use locale-independent examples and inclusive names.
- Write dates with an unambiguous format. Include the time zone when timing matters.
- State units. Do not assume a currency, measurement system, keyboard layout, legal regime, or network quality.
- Keep sentences structurally direct for readers and translators.

## Technical formatting

- Use code font for commands, flags, filenames, paths, environment variables, API elements, classes, methods, literals, status codes, and user-entered text.
- Use fenced code blocks for multi-line code or terminal output. Identify the language when known.
- Keep punctuation outside linked text unless the punctuation belongs to the target title.
- Reserve underlining for links.
- Use italics sparingly for introduced terms or semantic emphasis.
- Do not use ampersands as a substitute for *and* unless an official name or UI label contains one.
- Preserve the exact capitalization of APIs, products, commands, and UI labels.

## Truth and time

Distinguish these states explicitly:

- **Available:** verified current behavior.
- **Proposed:** requested or designed behavior that is not implemented.
- **Planned:** approved work with a reliable source and status.
- **Unknown:** information that available evidence does not establish.

Do not turn a proposal into a promise. Do not use `will` for uncertain behavior. In durable product documentation, describe current behavior in the present tense. Include version boundaries when behavior varies by release.

## Edit in passes

Use separate passes so sentence polish does not hide structural or factual defects:

1. **Truth pass:** verify claims, names, numbers, examples, links, status, and scope against the source of truth.
2. **Purpose pass:** remove content that does not serve the audience or intended outcome.
3. **Structure pass:** reorder content, split mixed purposes, improve headings, and expose prerequisites and decisions.
4. **Clarity pass:** remove ambiguity, stabilize terms, name actors, quantify limits, and simplify sentence structure.
5. **Presentation pass:** check lists, code formatting, links, alt text, tables, punctuation, and visual consistency.
6. **Use pass:** follow the procedure, answer the question, or make the decision as the intended reader would.

For a short message, perform the same checks mentally and proportionally. Do not expand a small artifact merely to display the checklist.
