---
name: review-ios-ui-apple-hig
description: Review iOS app UI against Apple Human Interface Guidelines and iOS platform conventions. Use when asked for an Apple HIG-based iOS UI, UX, SwiftUI, UIKit, screenshot, simulator, accessibility, Dynamic Type, navigation, layout, controls, color, typography, or platform-conventions review, especially when the user wants critique or prioritized findings grounded in Apple's interface guidance instead of project-specific design docs.
---

# Review iOS UI Against Apple HIG

## Purpose

Use this skill to review an iOS interface against Apple Human Interface Guidelines, iOS conventions, and observable product behavior.

Default to review-only. Do not edit files unless the user explicitly asks for fixes.

## Workflow

1. Define the review surface: identify the app screens, screenshots, SwiftUI/UIKit files, simulator state, and target devices or size classes involved.
2. Gather evidence from the actual artifact. Prefer screenshots, simulator runs, UI previews, or concrete SwiftUI/UIKit code over generic assumptions.
3. Read `references/apple-hig-review.md` before making guideline claims, then read the page-specific reference files it routes to. If the user asks for the current or exact Apple rule, verify the linked Apple page live.
4. Review by category: platform fit, layout, navigation, controls and input, typography, color and materials, accessibility, feedback states, destructive actions, and iPad/adaptive behavior when relevant.
5. Rank findings by user impact and confidence. Prioritize issues that affect comprehension, task completion, accessibility, safety, or platform expectation.
6. Report findings with evidence and a concrete recommendation. Avoid broad redesign advice unless it follows directly from an observed issue.

## Evidence Rules

- Do not rely on project-specific design documents unless the user explicitly asks for that comparison.
- When reviewing code, cite file paths and line numbers for the UI surface that creates the issue.
- When reviewing screenshots or simulator output, describe the visible region precisely enough that the user can locate it.
- When behavior depends on runtime state, Dynamic Type, appearance mode, localization, or device size, say whether it was verified.
- Use the Browser plugin or another rendered browser only when Apple HIG imagery/examples or web-rendered reference pages need visual inspection.

## Output Shape

Start with findings, ordered by severity:

```text
High: <issue title>
Evidence: <file:line, screenshot area, or runtime observation>
Apple guideline basis: <short paraphrase plus HIG page name/link when useful>
Recommendation: <specific UI change or validation step>
```

Then include:

- `Open questions` only when missing context changes the recommendation.
- `Verification gaps` when the review did not include device, simulator, Dynamic Type, dark mode, VoiceOver, or localization checks that matter.
- `No guideline-level issues found` when the inspected surface appears aligned and only subjective style preferences remain.

Keep the response concise. Do not include a generic HIG checklist in the final answer unless the user asks for one.
