# Design Principles Reference

Official source: WWDC26 Session 250 — "Principles of great design"
https://developer.apple.com/videos/play/wwdc2026/250/
Apple HIG: https://developer.apple.com/design/human-interface-guidelines/design-principles

Load this reference when grounding a finding in Lens 1 (Design Principles).

## What Design Is

Design is making something with intention — focusing on what's most important to people, so you build something they will truly value. Every feature asks for a person's time, attention, and trust. Choosing what to build is often a matter of deciding what not to include.

There is no formula or right way to combine these principles. Leaning into one may feel like compromising another. Use knowledge and intuition to find the best path forward.

## Purpose

Purpose means designing experiences that genuinely serve people: ones that respect and adapt to their lives, are clear and considered, and at their best, a true joy to use.

Before writing a line of code, ask whether what you're making has real purpose and delivers something people will truly value.

**Review application**: Flag screens where secondary content, decorative treatment, or extra controls compete with the main reason the app exists.

## Agency

Agency means putting people in control. Let them explore at their own pace, avoid forcing them down predetermined paths, and build in forgiveness: easy undo and confirmation for destructive actions, so they feel confident and free to try things.

Offering choices is the best way to bring agency into your experience. An interface should never stand in the way of what someone is trying to do.

People will make mistakes. When that happens, offer forgiveness:
- Make it easy to undo actions
- Double-check before destructive actions
- Use interruptions carefully, only when someone is about to make a big mistake

**Review application**: Flag forced paths, unclear system state, destructive dead ends, and missing undo/recovery.

## Responsibility

Acting responsibly means respecting privacy as a human right, asking only for what's necessary, and anticipating how features could cause harm.

Responsible interfaces wait for the right moment to ask for personal data. They only ask for what's necessary, and are transparent about what the data is for.

Anticipate misuse:
- How could this feature be misused?
- Who would be harmed by this?
- How do I prevent it?
- With AI: anticipate that a model might generate something unexpected or inaccurate. Add safeguards: previews, confirmations, disclaimers.
- Remove features entirely if the risks to people's safety outweigh the value.

**Review application**: Flag permission prompts on first launch before showing value, missing safeguards on AI features, and data collection without context.

## Familiarity

Familiarity lets people apply existing knowledge to your design. Use metaphors that aren't too literal or abstract, follow established conventions for common actions, and keep behavior consistent: things that look the same should work the same.

The trick to metaphors is making sure they aren't too literal or abstract. A good metaphor draws on something people know and helps them predict what it will do.

Consistency helps people predict what will happen next:
- Things that look the same should behave the same
- Consistent placement speeds people up (they don't have to think about it)
- Don't reinvent the wheel for common actions — use the metaphors people already know

**Review application**: Flag custom icons or gestures that do something unexpected, inconsistent behavior between similar-looking controls, and metaphors that don't match real-world expectations.

## Flexibility

A flexible design adapts to the many different contexts, devices, and abilities of its users. Design for each platform's strengths, consider the full range of your audience, and let people personalize their experience when no single solution fits everyone.

People use your design in ways as unique as they are. Support all the different contexts:
- Different devices (iPhone touch, Mac pointer, Apple Watch glance)
- Different abilities (accessibility features, languages, ages, skill levels)
- Different situations (at home, on a run, driving)

When no single design solution fits everyone, let people personalize: rearrange controls, hide unused elements.

**Review application**: Flag layouts that break at large Dynamic Type sizes, missing VoiceOver support, and designs that don't adapt to different devices or orientations.

## Simplicity

Simplicity isn't minimalism: it's removing friction. Concise language, strong visual hierarchy, and clear affordances help people find what they need without effort. Every element should earn its place, and sometimes adding context makes an interface simpler.

Simplicity means:
- Concise interfaces use plain language, strip jargon, avoid redundancy
- Clear interfaces use hierarchy (order, spacing, contrast) to guide attention
- Every element earns its place
- Sometimes simpler means adding context (a play/pause control with time remaining is simpler than one without)

**Review application**: Flag screens where the primary action is hard to find, jargon-heavy copy, and elements that don't serve the user's purpose.

## Craft

Craft is the uncompromising attention to detail that builds trust. Beautiful typography, responsive animations, solid performance, and a commitment to iteration show people you care. Great design has longevity: keep evolving it as platforms and people's needs change.

Ingredients of well-crafted design:
- Beautiful fonts that look great across devices
- Thoughtful colors that adapt across light and dark
- Clear graphics and iconography
- Responsive animations that feel fluid and provide immediate feedback
- Reliable and secure foundation

Craft comes from iteration. Great design has longevity — keep evolving it when new features or hardware are introduced.

**Review application**: Flag misaligned elements, janky scrolling, inconsistent spacing, fonts that don't adapt, and animations that feel rushed or delayed.

## Delight

Delight isn't confetti: it's the natural result of getting everything else right. Identify the emotion you want people to feel, then reinforce it through your design. When you combine all these principles with genuine care, you create something people truly love.

The way to make a design delightful isn't by adding confetti or tacking on extra flourishes. Identify the emotion you want your audience to feel — relaxed, confident, excited — and find opportunities to reinforce that through your design.

Delight is the sum of the consideration you put into your product. It's the natural result of getting all the design principles right.

**Review application**: Flag decoration that gets in the way of task completion, delight that becomes noise, and missing emotional connection to the task.