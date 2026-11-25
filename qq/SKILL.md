---
name: qq
description: Answers a quick question directly and briefly, using any read-only tool to find the answer (files, code search, read-only commands, web, connected services) without changing files, sending messages, or asking clarifying questions. Use when the user invokes qq or $qq, prefixes a message with "qq", or says "quick question" and wants an answer rather than work done.
---

# QQ (Quick Question)

The user wants an answer, not a change. Find it with whatever tools help, reply briefly, and stop.

## Rules

- **Read anything, change nothing.** Use any tool that only reads: files, code search, directory listings, read-only commands (`git log`, `git diff`, `ls`, `--version`), web search and fetch, and connected services such as GitHub, Linear, Slack, Sentry, or docs. Read-only subagents are fine for a broad search.
- **No side effects.** Don't create, edit, move, or delete files. Don't run commands that write or change state, such as installs, builds, migrations, commits, pushes, or tests that write files or touch shared services. Don't send, post, comment, react, create, update, or delete anything in any service: no messages, emails, issues, PR comments, or calendar events. If the only way to answer is a tool with side effects, say so and answer as well as you can without it.
- **Check, don't guess.** If a lookup can settle the question, do it. "This" and "here" usually mean the current project or whatever is under discussion.
- **Stop when you have it.** Do as many lookups as the answer needs and no more. You're answering a question, not auditing the codebase.
- **Don't ask questions.** If the question is ambiguous, pick the most likely reading and answer it. If another reading is plausible, cover it in one short clause ("If you meant X, then Y.").
- **Lead with the answer.** The first sentence is the answer: a yes/no, a number, a name, a command. Add context only when the answer would be wrong or misleading without it. Cite where you found it when it helps (`src/api.ts:42`, a PR link).
- **Match length to the question.** A yes/no question ("is it…?", "can we…?", "does it…?") gets "Yes." or "No." plus at most one short sentence with the key reason. Don't add what would need to change, steps, plans, trade-offs, or caveats unless the user asks for them. Other questions get one to three sentences. Use a list, table, or code snippet only when the user asks for one or when it is the answer itself.
- **Be honest about uncertainty.** If the lookups don't settle it, say so in a few words and give your best answer, marked as a guess.
- **No preamble or follow-ups.** Skip "Great question", restating the question, summaries of what you searched, and "Want me to...?" offers.

## Examples

**Input:** qq what's the difference between `git fetch` and `git pull`?
**Output:** `git fetch` downloads remote commits without changing your branch; `git pull` fetches and then merges (or rebases) them into your current branch.

**Input:** qq is this using pagination?
*(Searches the code for the API call and `next_page`/`has_more`.)*
**Output:** No. `fetchCards()` in `src/scryfall.js:18` requests `/cards/search` once and never follows `next_page`, so it gets at most the first 175 results.

**Input:** qq can we support pagination with the library this uses?
*(Reads how requests are made.)*
**Output:** Yes. Requests already go through curl, and Scryfall pages are the same URL with `&page=N`.

**Input:** qq did anyone review my PR yet?
*(Reads the PR's reviews with `gh pr view`.)*
**Output:** Yes. Two people approved it this morning, and one left a comment on `src/auth.ts` asking for a test.

**Input:** qq reply to Sam on Slack that I'm running late
**Output:** That sends a message, which qq doesn't do. Ask without qq and it can be sent.
