# Apple HIG Review Router

Use this file first after the `review-ios-ui-apple-hig` skill triggers. It routes to page-specific references and keeps the core review shape compact. For exact or current wording, open the linked Apple page.

## Source Map

- `design-principles.md`: Use for the top-level product lens: purpose, agency, responsibility, familiarity, flexibility, simplicity, craft, and delight. Start here for every substantive review.
- `designing-for-ios.md`: Use for iPhone-specific expectations: handheld use, Multi-Touch, short sessions, system features, Dark Mode, Dynamic Type, orientation, one-handed reach, and permissioned platform capability use.
- `layout.md`: Use for safe areas, margins, hierarchy, adaptive layouts, Dynamic Type, localization, Display Zoom, iPad resizing, and iOS-specific layout concerns.
- `menus-and-actions.md`: Use when reviewing command surfaces: buttons, toolbars, context menus, edit menus, pull-down/pop-up menus, share sheets, row actions, and Home Screen quick actions.
- `design-resources.md`: Use when reviewing app icons, symbols, screenshots, UI kits, fonts, Icon Composer output, product bezels, badges, logos, or App Store imagery.
- `app-store-review-guidelines.md`: Use only as an App Store compliance cross-check when UI or copy touches safety, privacy, payments, metadata, minimum functionality, misleading behavior, children, health, legal, or submission readiness.

## Official Apple Entry Points

- Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
- Design principles: https://developer.apple.com/design/human-interface-guidelines/design-principles
- Apple Design Resources: https://developer.apple.com/design/resources/
- App Store Review Guidelines: https://developer.apple.com/app-store/review/guidelines/

## Core Review Categories

- **Platform fit**: Native iOS patterns, familiar gestures, system controls, predictable navigation, and clear permissioned use of platform capabilities.
- **Layout and hierarchy**: Safe areas, readable margins, visual grouping, scan order, control/content separation, stable wrapping, and layouts that survive small/large devices and large text.
- **Navigation and modality**: Clear place, clear path back, appropriate tabs/stacks/sheets/alerts, no unnecessary traps, and preserved context across adaptation.
- **Controls and input**: Correct control choice, reachable primary actions, clear labels, keyboard/input type, validation, loading/disabled/error states, and separated destructive actions.
- **Typography and language**: System text styles, Dynamic Type, legibility, direct wording, meaningful labels, and truncation/multiline behavior.
- **Color, materials, and appearance**: Semantic colors, contrast, non-color-only status, light/dark/increased-contrast behavior, and material/blur that supports readability.
- **Accessibility**: VoiceOver labels and traits, reading order, target size, contrast, Dynamic Type, Reduce Motion, Differentiate Without Color, localization, and recovery from mistakes.
- **Feedback and safety**: Empty/loading/success/failure/offline states, clear acknowledgement, undo or confirmation for destructive work, and flags for misleading or unsafe flows.
- **Adaptivity**: Size classes, orientation, iPad windows, split view, pointer/keyboard support, sidebar/tab adaptation, and smallest/largest supported layouts.

## Review Discipline

- Make guideline claims as paraphrases tied to the relevant Apple page or local reference file.
- Separate HIG/platform issues from subjective style preferences.
- State confidence when evidence is partial.
- Recommend the smallest UI change that resolves the observed mismatch.
- Do not cite App Store Review Guidelines as if they were HIG; label them as compliance cross-checks.
