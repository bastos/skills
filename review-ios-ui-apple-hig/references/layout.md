# Layout Reference

Official source: https://developer.apple.com/design/human-interface-guidelines/layout

Use this file for spatial organization, safe areas, visual hierarchy, and adaptive behavior.

## Core Layout Checks

- Group related items so people can find information quickly. Use spacing, separators, background shapes, color, or material only when they clarify relationships.
- Give essential information enough space. Do not crowd the primary content with secondary metadata or controls.
- Extend backgrounds, artwork, and scrollable content to fill the screen or window where appropriate, while accounting for bars and control layers.
- Keep controls visually distinct from content, especially when using material, blur, scroll-edge effects, or full-bleed imagery.
- Place important items near the top and leading side in the current reading direction; account for right-to-left languages.
- Align components to support scanning and hierarchy.
- Use progressive disclosure when content is hidden, and make the availability of more content discoverable.
- Provide enough spacing around controls and group controls into logical sections.

## Adaptability Checks

- Design for context changes while preserving a recognizable structure: screen size, resolution, color space, orientation, Dynamic Island, camera controls, external display, Display Zoom, iPad resizing, Dynamic Type, and localization.
- Use SwiftUI layout or Auto Layout patterns that respond dynamically. If custom layout is used, inspect the fallback behavior carefully.
- Preview or request verification at the smallest and largest supported layouts, portrait/landscape where supported, multiple localizations, and large text sizes.
- Scale artwork without changing its aspect ratio; keep important visual content visible if letterboxing or cropping would occur.

## Safe Areas and iOS-Specific Checks

- Respect safe areas so content and controls do not collide with bars, Dynamic Island, sensor housing, home indicator, or other system/interactive regions.
- Aim to support both portrait and landscape unless the app has a strong reason not to.
- For games or immersive media, full-bleed can be appropriate, but it still needs to account for hardware curvature, sensor housing, and Dynamic Island.
- Question edge-to-edge full-width buttons on iOS. Buttons generally feel more native when inset from system-defined margins unless the full-width treatment is intentional and safe-area aware.
- Hide the status bar only when it clearly improves an immersive experience.
- On iPad, review resizable window behavior and prefer stable transitions over abrupt compact-mode changes.
