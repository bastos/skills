# Design Principles Reference

Official source: https://developer.apple.com/design/human-interface-guidelines/design-principles

Use this file as the first lens for any substantial iOS UI review. The page was reintroduced by Apple on June 8, 2026, and frames the rest of the HIG as product judgment rather than a mechanical checklist.

## Review Lens

- **Purpose**: The interface should make the app's core value and primary jobs obvious. Flag screens where secondary content, decorative treatment, or extra controls compete with the main reason the app exists.
- **Agency**: People should be able to act, explore, recover, skip unnecessary guided flows, and leave modes without losing work. Flag forced paths, unclear system state, destructive dead ends, and missing undo/recovery.
- **Responsibility**: Privacy, permissions, safety, data use, product claims, health/child/location/payment behavior, and automation should be transparent and in the user's best interest.
- **Familiarity**: The UI should build on concepts people know, use established platform patterns, stay internally consistent, and provide clear feedback for changes in control availability, content, and state.
- **Flexibility**: The experience should adapt to different devices, configurations, input methods, accessibility needs, languages, orientations, and iPad window sizes without becoming unfamiliar.
- **Simplicity**: The interface should be organized, direct, and concise. Simplicity means keeping necessary capability understandable, not stripping away needed function.
- **Craft**: Details matter: wording, alignment, motion, performance feel, current platform patterns, and realistic testing across device contexts.
- **Delight**: Character should support the task and emotional goal. Flag delight that becomes decoration, slows progress, weakens clarity, or harms accessibility.

## How to Use in Findings

- Use Design Principles for broad product-level findings that cross multiple components.
- Pair each principle finding with a concrete UI surface: screen, screenshot region, file/line, or runtime behavior.
- Avoid using a principle as a vague taste argument. Explain the user impact and the specific design adjustment.
