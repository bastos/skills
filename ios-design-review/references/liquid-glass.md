# Liquid Glass & New Design System Reference

Official sources:
- WWDC25 Session 219 — "Meet Liquid Glass" — https://developer.apple.com/videos/play/wwdc2025/219/
- WWDC25 Session 356 — "Get to know the new design system" — https://developer.apple.com/videos/play/wwdc2025/356/
- WWDC25 Session 323 — "Build a SwiftUI app with the new design" — https://developer.apple.com/videos/play/wwdc2025/323/
- Apple Newsroom — https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/

Load this reference when grounding a finding in Lens 3 (Liquid Glass & New Design System).

## Overview

Liquid Glass marks the most extensive software design update Apple has made, reshaping the relationship between interface and content through a brand new set of heuristics. The result is a harmonized design language that's more cohesive, adaptive, and expressive.

The new design extends across iOS 26, iPadOS 26, macOS Tahoe 26, watchOS 26, and tvOS 26 — for the first time, a universal design across platforms.

## What Is Liquid Glass?

Liquid Glass is a new digital meta-material that dynamically bends and shapes light. It behaves and moves organically like a lightweight liquid, responding to both the fluidity of touch and the dynamism of modern apps.

Key properties:
- **Lensing**: dynamically bends, shapes, and concentrates light in real time, providing definition against background content while letting content shine through
- **Adaptive**: color is informed by surrounding content and intelligently adapts between light and dark environments
- **Materializes**: objects materialize in and out by gradually modulating the light bending and lensing (graceful transitions)
- **Responsive**: reacts to interaction by instantly flexing and energizing with light
- **Concentric**: rounded, floating forms that nest neatly in the rounded curves of modern devices

### Two Variants
- **Regular**: the most versatile. All visual and adaptive effects. Provides legibility regardless of context. Works in any size, over any content. Anything can be placed on top.
- **Clear**: permanently more transparent, allows richness of content underneath to come through. Does not have adaptive behaviors. Needs a dimming layer for legibility. Use only when: element is on top of media-rich content; content layer won't be negatively impacted by a dimming layer; content above is bold and bright.
- **Never mix the two variants** — they have different characteristics and use cases.

### Layering Rules
- Liquid Glass is best reserved for the **navigation layer** — controls, toolbars, tab bars, sidebars
- **Avoid putting glass in the content layer**
- **Avoid putting glass within or on top of other glass elements** — use GlassEffectContainer for grouping so glass can sample consistently

## Design Language

### Color
- System color family adjusted across Light, Dark, and Increased Contrast appearances to work in harmony with Liquid Glass
- Improved hue differentiation without losing the optimistic spirit

### Typography
- Refined to strengthen clarity and structure
- Bolder and left-aligned to improve readability in key moments like alerts and onboarding
- Use system text styles — they support Dynamic Type and adapt across conditions

## Concentricity

There's a quiet geometry to how shapes fit together, driven by concentricity. By aligning radii and margins around a shared center, shapes can comfortably nest within each other.

Three shape types:
1. **Fixed shapes**: constant corner radius
2. **Capsules**: radius is half the height of the container — naturally supports concentricity, seen throughout the system in sliders, switches, bars, buttons, grouped table view corners
3. **Concentric shapes**: calculate radius by subtracting padding from the parent's radius

### Platform-specific shape guidance
- **iPhone**: capsules bring focus and clarity to touch-friendly layouts. Use capsule with extra margin near screen edges.
- **iPad/Mac**: use concentric shape that aligns with the window edge for better balance. On macOS, Mini/Small/Medium controls use rounded rectangles for compact density (inspector panels). Large controls use capsule shapes. X-Large size takes advantage of Liquid Glass for emphasis in spacious areas.

### Common issues
- Corners that feel too pinched or flared create tension and break balance
- Nested containers (artwork in a card) often need concentric shapes so the system calculates inner radii automatically
- Components that work both inside a container and on their own: use concentric shape with a fallback radius

## Structure

### Functional Layer
Liquid Glass defines a new functional layer in the UI, floating above content to bring structure and clarity without ever stealing focus.

### Action Sheets
- Now spring from the action itself (the source), rather than appearing at the bottom of the screen
- Clearly defined roles help the system understand the relationship, anchoring the interaction as it extends directly from the tapped element
- Apply the material directly to the control, not its inner views

### Focus and Modality
- Liquid Glass reflects navigation focus through subtle material variation
- When a task interrupts the main flow: pair Liquid Glass with a dimming layer to center attention
- When a task happens in parallel: Liquid Glass creates natural separation without breaking flow
- When focus shifts (dragging a sheet upward): Liquid Glass subtly recedes, becomes more opaque, grows in size to signal deeper engagement

### Bars (Toolbars and Tab Bars)
- **Remove background colors from custom toolbars and tab bars** — customizations like extra backgrounds or borders are unnecessary now
- Rely on layout and grouping to express hierarchy rather than decoration
- Organize bar items logically by function and frequency of use
- Buttons that perform related actions should generally go together
- Don't group symbols with text (could be perceived as a single button) — allow text buttons to sit in their own containers
- A primary action (like Done) stays separate and appears tinted — blue checkmark on iOS/iPadOS, prominent text button on macOS
- Badges can be added with a single line of code
- Monochrome icons reduce noise
- Automatic scroll edge effect blurs content under toolbars for legibility

### Tab Bar
- One of the most persistent parts of the app — organizing it well gives people a clear sense of layout
- **iOS now includes a dedicated Search tab** at the bottom for quick access
- Tab bars can support persistent features using accessory views (media playback controls that stay visible)
- Avoid placing screen-specific actions here — a checkout button belongs with the content it supports
- Tab bars shrink when scrolling to bring focus to content; expand when scrolling back up

### Scroll Edge Effects
- Replace hard dividers with subtle blur to reduce clutter and keep UI legible
- Reinforce the boundary between floating UI and content
- Not decorative — don't block or darken like overlays; clarify where UI and content meet
- Don't use where there aren't any floating UI elements
- **Two styles**:
  - **Soft** (default, most cases on iOS/iPadOS): subtle transition, works well for interactive elements using Liquid Glass
  - **Hard** (mostly macOS): stronger, more opaque boundary — ideal for interactive text, controls without backgrounds, pinned table headers
- Apply one scroll edge effect per view. In Split View, each pane can have its own — keep consistent in height.

## Sidebars & Immersion

- Sidebars are now **inset** and built with Liquid Glass, allowing content to flow behind them for a more immersive feel
- **Background extension effects** let content expand behind the sidebar, filling the full width while keeping visuals centered
- Use for hero images, tinted backgrounds, or any surface meant to feel expansive
- Ensure text and controls are layered above to avoid unwanted visual distortion
- Scroll views extend beneath sidebars by default — carousels and other content glide through naturally
- On iPad and Mac, sidebars and tab bars form a cohesive, consistent language for core navigation — a single navigational element that fluidly scales as the canvas grows

## Continuity

When someone moves between devices or resizes a window, they're not starting over — they're continuing the same task.

### Design Once, Scale Per Platform
- Design the **anatomy** of the app once — it scales appropriately for each platform:
  - **iPhone**: narrow, vertical layout
  - **iPad**: scalable middle ground
  - **Mac**: wide, expansive canvas
- Structure components to scale with shared anatomy and core interactions that remain the same regardless of form factor

### Shared Content and Symbols
- Use the same symbols across devices to preserve meaning and build familiarity through repetition
- When there's no clear shorthand, a text label is always the better choice over ambiguous icons
- Bars now rely more on symbols than text — this shift is happening platform-wide including menus
- Populate menus with symbols where it helps recognition
- When actions are closely related (multiple ways to copy), use the symbol once to introduce the group, let text do the rest

### Component Anatomy
- Define shared anatomy: pieces of a component layout should persist and be reused in familiar placements
- A popup menu on macOS and a context menu on iOS might not look the same, but both include: selection indicator, icon, label, accessory item
- Components should support the same set of core interactions — tab bars, segmented controls, and sidebars all signal selection, navigation, and state in consistent ways