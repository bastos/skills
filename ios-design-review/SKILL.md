---
name: ios-design-review
description: >
  Review iOS app UI/UX design quality using Apple's design principles and the
  Liquid Glass-era design language from WWDC25/26. Use when asked for a design
  review, UX critique, visual design assessment, or evaluation of an app's
  interface quality, design intent, alignment with the new Apple design system,
  or usability. Triggers: "design review", "UX review", "visual design
  critique", "review the UI", "does this design work", "evaluate this
  interface", "design feedback", "Liquid Glass review".
license: MIT
metadata:
  author: github.com/bastos
  version: "1.0"
---

# iOS Design Review

Evaluate an iOS app's design quality by examining the **intent, structure, and craft** of its interface — not just whether it follows a rulebook.

It assesses the **quality of the design itself** using three lenses from WWDC25/26:

1. **8 Design Principles** (WWDC26 #250) — Purpose, Agency, Responsibility, Familiarity, Flexibility, Simplicity, Craft, Delight
2. **Design Evangelism Framework** (WWDC25 #359) — Structure → Navigation → Content → Visual Design
3. **Liquid Glass & New Design System** (WWDC25 #356, #219) — Concentricity, Liquid Glass adoption, continuity, platform harmony

## Review Surface

Establish the review scope before starting:

| User says | What to review |
|---|---|
| "Review this app" | Identify screens; prefer screenshots, simulator, or video |
| "Review this screenshot" | Single screen — analyze layout, hierarchy, controls |
| "Review this flow" | Sequence — examine navigation, transitions, task completion |
| "Review this prototype" | Evaluate against purpose — does the prototype serve its goal? |
| "Compare to Apple's new design" | Evaluate Liquid Glass adoption, concentricity, platform fit |

Prefer visual evidence (screenshots, simulator, video) over code. Code tells you how it's built, not how it feels to use. When you only have code, extrapolate the visible result before judging.

## Lens 1: 8 Design Principles

For full principle definitions and review application guidance, read `references/design-principles.md`.

Evaluate the design against each principle that applies to the review scope. Not every principle applies to every screen — use judgment.

### Purpose
- Does the screen make the app's core value obvious within seconds?
- Is there a clear primary action or takeaway?
- Do secondary elements compete with the main reason the screen exists?
- **Red flag**: A screen where you can't immediately answer "what is this for?"

### Agency
- Can people explore at their own pace, or are they forced down paths?
- Is undo available for destructive actions?
- Are there confirmation prompts for irreversible changes?
- **Red flag**: No way to undo or go back from a key action.

### Responsibility
- Are privacy requests contextual and necessary?
- Does the app anticipate how features could be misused?
- Are AI-generated outcomes safeguarded (previews, confirmations, disclaimers)?
- **Red flag**: Permission prompt on first launch before showing value.

### Familiarity
- Do metaphors match real-world expectations (trash = delete)?
- Are standard gestures and conventions respected (back swipe, tap to select)?
- Do things that look the same behave the same?
- **Red flag**: A custom icon or gesture that does something unexpected.

### Flexibility
- Does the design adapt to different devices, orientations, and text sizes?
- Does it support accessibility features (Dynamic Type, VoiceOver, Reduced Motion)?
- Are there personalization options for different workflows?
- **Red flag**: Layout breaks or becomes unusable at large Dynamic Type sizes.

### Simplicity
- Is the interface concise and direct, or full of jargon?
- Does strong visual hierarchy guide attention to what matters?
- Does every element earn its place?
- **Red flag**: A screen where you have to hunt for the primary action.

### Craft
- Are fonts, colors, and spacing consistent and intentional?
- Do animations feel fluid and provide natural feedback?
- Does the design hold up across light/dark mode and different content states?
- **Red flag**: Misaligned elements, janky scrolling, inconsistent spacing.

### Delight
- What emotion should the design evoke? Does it succeed?
- Is delight earned through thoughtful interaction, not confetti?
- Do micro-interactions feel considered (haptics, transitions, spring animations)?
- **Red flag**: Decoration that gets in the way of task completion.

## Lens 2: Design Evangelism Framework

For full framework detail with the vinyl collection app walkthrough, read `references/evangelism-framework.md`.

Walk through these four layers in order. Each layer builds on the previous one.

### Structure — Is the app's purpose clear?
- **Orientation**: Can the user immediately answer "where am I?"
- **Actions**: Can they see "what can I do here?" without hunting?
- **Next steps**: Is it clear "where can I go from here?"
- **Information architecture**: Is content organized and prioritized, or is everything fighting for attention?
- **Essential vs optional**: Are non-essential features trimmed or demoted?

### Navigation — Can people move with confidence?
- **Tab bar**: Is it minimal (3-4 tabs max)? Are labels direct and icons from SF Symbols?
- **Toolbar**: Does each screen have a title and screen-specific actions?
- **Primary action placement**: Is the main action in the right place (not in the tab bar)?
- **Back/exit**: Is navigation predictable? Can people always go back?
- **Progressive disclosure**: Are options revealed when needed, not all at once?

### Content — Is information organized to guide action?
- **Separation**: Are different content types clearly separated (not mixed together)?
- **Progressive disclosure**: Is essential info shown first, detail revealed on interaction?
- **Layout choice**: Is the right container used (list for structured data, grid/collection for visual items)?
- **Grouping**: Is content grouped meaningfully (by time, progress, patterns)?
- **Scanning**: Can people find what they need without reading everything?

### Visual Design — Does the styling serve the content?
- **Visual hierarchy**: Does the most important content draw attention first?
- **Typography**: Are system text styles used? Does it handle Dynamic Type?
- **Color**: Are semantic colors used for dynamic adaptation? Is accent color used sparingly?
- **Imagery**: Do images have a cohesive visual style? Do they enhance scannability?
- **Legibility**: Is text readable over images (gradient/blur overlay)?
- **Consistency**: Do visual treatments hold up across all screens?

## Lens 3: Liquid Glass & New Design System

For full detail on Liquid Glass properties, variants, concentricity, structure, and continuity, read `references/liquid-glass.md`.

Evaluate alignment with Apple's current design language introduced at WWDC25.

### Concentricity
- Do controls nest concentrically within their containers?
- Are corner radii aligned with hardware curves (not rectangular on round screens)?
- Do bar elements use capsule geometry that supports the new concentric layout system?
- **Check**: Are corner radii too pinched or flared? Use concentric shapes with fallback radii for nested components.

### Liquid Glass Adoption
- Are toolbars, tab bars, and navigation elements using Liquid Glass material instead of solid backgrounds?
- Have custom bar backgrounds been removed — is hierarchy expressed through layout and grouping instead?
- Do action sheets and popovers spring from their source control rather than appearing at the screen bottom?
- Are scroll edge effects present where floating UI overlaps content? Soft (default) for iOS/iPadOS, hard for macOS.
- **Check**: Solid bar backgrounds = legacy pattern. Should be Liquid Glass or transparent.

### Sidebars & Immersion
- Are sidebars inset, using Liquid Glass, with content flowing behind them?
- Are background extension effects used for hero images and tinted backgrounds?
- Is text layered above to avoid distortion from the background extension?
- Do scroll views extend beneath sidebars so carousels glide through naturally?
- **Check**: A sidebar with a solid background is missing the new design language.

### Typography & Color
- Is typography bolder and left-aligned where appropriate (alerts, onboarding)?
- Are system text styles used instead of custom sizes?
- Are semantic colors used (label, secondarySystemBackground) instead of hard-coded values?
- Does the app handle light/dark mode natively without breaking?
- **Check**: Hard-coded text sizes and colors that don't adapt = legacy pattern.

### Continuity
- Does the app's anatomy scale across iPhone (narrow vertical), iPad (scalable middle), and Mac (wide canvas)?
- Are the same SF Symbols and labels used across platforms for the same actions?
- Do core interactions remain the same regardless of form factor?
- **Check**: Different icons for the same action across platforms = inconsistency.

## Review Workflow

1. **Scope**: Define the review surface and source of truth (screenshot, simulator, code).
2. **First pass — Design Principles (Lens 1)**: Scan for the biggest wins and issues. What feels off immediately?
3. **Second pass — Evangelism Framework (Lens 2)**: Walk Structure → Navigation → Content → Visual Design in order.
4. **Third pass — Design System (Lens 3)**: Check Liquid Glass adoption, concentricity, continuity.
5. **Rank**: Order findings by user impact. Prioritize issues that affect comprehension, task completion, safety, or trust.
6. **Report**: Structure findings with evidence, the design principle violated, and a concrete recommendation.

## Output Format

```
## Summary
<1-2 sentence overall assessment of design quality>

## Findings

### Critical
<issues that prevent task completion, cause confusion, or betray trust>

### Important
<issues that reduce clarity, slow users down, or miss design system alignment>

### Minor
<craft details, polish opportunities, subjective improvements>

## What's Working Well
<2-3 things the design does right — always include this>
```

For each finding, include:
- **Screen/location**: Which screen or component
- **Lens**: Which principle or framework category applies
- **Issue**: What's wrong and why it matters
- **Recommendation**: Concrete change or design direction

## Evidence Rules

- Prefer visual evidence (screenshot annotations, simulator video) over code.
- When reviewing from code, extrapolate the visible result before judging.
- Distinguish between design quality issues and personal taste.
- State confidence when evidence is partial or context is missing.
- Recommend the smallest change that resolves the observed issue.
- Ground findings in the reference files — each lens has a companion `references/*.md` with the WWDC source material, full principle definitions, and review application notes. Cite the WWDC session number when grounding a finding.
- Official Apple links are at the top of each reference file for live verification.
