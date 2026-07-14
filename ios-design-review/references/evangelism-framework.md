# Design Evangelism Framework Reference

Official source: WWDC25 Session 359 — "Design foundations from idea to interface"
https://developer.apple.com/videos/play/wwdc2025/359/

Load this reference when grounding a finding in Lens 2 (Evangelism Framework).

This framework walks through four layers of an app in order. Each layer builds on the previous one: structure shapes navigation, navigation reveals content, content is presented through visual design.

## Structure — Is the app's purpose clear?

Every app is built on a foundation that shapes everything else: how people navigate, what stands out, and how the experience comes across.

When looking at an app, find clarity by answering three questions:
1. **Where am I?** The app should make that clear right away — not leave the user wondering where they are or how they got there.
2. **What can I do?** Actions should be clear and easy to understand — no guessing.
3. **Where can I go from here?** A clear sense of next steps keeps the flow going.

When those questions are easy to answer, the app feels inviting and fluid.

**Information architecture** is the process of organizing and prioritizing information so people can easily find what they need, when they need it — without friction:
1. Write down everything the app does — features, workflows, nice-to-haves
2. Imagine how someone else might use the app: when, where, how it fits their routine
3. Clean up: remove non-essential features, rename unclear things, group what belongs together

If you don't have clarity on what's essential, you can't communicate it in the app. Simplifying sharpens the app's purpose.

**Review application**: Flag screens where the user has to work to understand where they are, what they can do, and where to go next. Flag mixing of menu/branding where a screen title should be.

## Navigation — Can people move with confidence?

Navigation should make people feel oriented and confident.

### Tab Bar
- Each extra tab means one more decision for people to make and may present the app as more complex than it really is
- Ask: What's truly essential? What deserves a tab? What doesn't?
- Merge non-essential elements (e.g., a "Crates" screen to group Records can merge into the main Records tab)
- **Tabs are for navigation, not for taking action** — a primary "Add" action belongs in the context where it's used, not in the tab bar
- Use direct labels and familiar SF Symbols icons so people get a sense of what each tab is for without interacting
- 3-4 well-named tabs with recognizable icons make the app's scope and purpose evident

### Toolbar
- Great way to orient people: includes a title with the name of the screen and screen-specific actions
- Sets expectations about content and helps people stay oriented as they navigate and scroll
- Offers a place for screen-specific actions people are most likely to want
- Space is limited — include only what's essential, using SF Symbols for recognition

**Review application**: Flag tab bars with too many tabs, action buttons in the tab bar, vague labels, custom icons instead of SF Symbols, and screens missing a clear title.

## Content — Is information organized to guide action?

Content should be organized to guide people to what matters most and what they expect to find first.

### Separation
- When two types of content are mixed together, it feels messy — split them into separate sections with clear titles

### Progressive Disclosure
- Show only what's necessary upfront — just enough to help people get started
- Reveal more as people interact (disclosure controls)
- When the expanded screen opens, arrange content the same way — it should feel connected to the previous screen, like it's expanding
- Don't forget the toolbar on expanded screens — it provides orientation and a back button

### Layout Choice
- **List**: flexible, highly usable, familiar for structured information, facilitates quick scanning, takes less vertical space than images so more items fit on screen
- **Grid/Collection**: ideal for groups of visual items (photos, products) that can be scrolled on and off screen — consistent spacing, minimal text on items
- Match the container to the content type

### Grouping (for large amounts of content)
- **By time**: Recent files, continue watching — helps people find things by when they're relevant
- **By progress**: Drafts, ongoing classes — helps people pick up where they left off
- **By patterns**: Related products, similar genres — surfaces relationships people didn't know to look for
- Grouping reduces choice overload and makes the app feel one step ahead

**Review application**: Flag mixed content types, missing progressive disclosure, grid layouts for structured text data, and ungrouped long lists that cause decision fatigue.

## Visual Design — Does the styling serve the content?

Visual design communicates the personality of the app and shapes how people feel. It's the thoughtful use of hierarchy, typography, images, and color, all while supporting function.

### Visual Hierarchy
- Guide the eye through the screen so it notices elements in order of importance
- Make what's most important larger or higher in contrast so it naturally draws attention first
- Provide a visual anchor for the most important content

### System Text Styles
- Make it easy to create clear hierarchy and strong legibility under different screen conditions
- Offer a consistent way to style titles, body, captions — without eyeballing text sizes or creating custom styles
- Support Dynamic Type, allowing people to choose a comfortable text size
- When text overlays an image, add a subtle background (gradient or blur) for readability

### Color
- **Semantic colors** are named after their purpose, not their appearance (label, secondarySystemBackground)
- They're dynamic — automatically change according to contrast settings, screen environments, and light/dark modes
- Use an accent color sparingly: on buttons, controls, to show what's selected
- Be careful it doesn't get in the way of dynamic changes, overall legibility, or comfort
- For anything dynamic, lean on system colors as the palette — they adapt without extra work

### Imagery
- Add images to represent groups and make lists easier to scan
- Establish a cohesive visual style: choose a color palette and set simple rules
- Choose a few retro shapes and mix and match for consistency
- Use bolder, expanded fonts for group titles so they look different from list text

### The System vs Personality
- Know when to lean on the system (semantic colors, text styles) and where to add personality (custom palette, unique imagery)
- The real impact comes when all elements work together, contributing to the overall meaning of the interface

**Review application**: Flag missing visual hierarchy, custom text sizes instead of system styles, hard-coded colors instead of semantic ones, inconsistent imagery styles, and text that's illegible over images.