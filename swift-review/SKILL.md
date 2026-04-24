---
name: swift-review
description: >
  Reviews Swift/Xcode codebases, pull requests, local changes, or individual files against
  Swift best practices including Google's Swift Style Guide, Apple's API Design Guidelines,
  build performance, memory management, and testing standards. Use this skill whenever the
  user asks to review Swift code, audit a Swift PR, check Swift style, review an Xcode
  project, or mentions swift code review, swift lint, swift best practices review, or
  swift code quality. Also trigger when reviewing .swift files, Package.swift, or Xcode
  project changes — even if the user just says "review this" or "check this code" and
  the context involves Swift.
license: MIT
metadata:
  author: github.com/bastos
  version: "1.0"
---

# Swift Code Review

Review Swift code against industry best practices drawn from Google's Swift Style Guide,
Apple's API Design Guidelines, Apple's performance and memory documentation, and
real-world patterns from Apple's open-source projects.

## Determine Review Scope

Figure out what to review based on the user's request:

| Request | How to get the code |
|---|---|
| "Review this PR" / PR URL | `gh pr diff <number>` or read the diff |
| "Review my changes" | `git diff` (unstaged) and `git diff --cached` (staged) |
| "Review this file" / path | Read the file(s) directly |
| "Review the codebase" | Glob for `**/*.swift` files, prioritize by size/complexity |
| Xcode project review | Also check `*.xcodeproj`, `Package.swift`, build settings |

When reviewing diffs, always read surrounding context (the full file or function) to
understand intent — don't review isolated hunks.

## Review Checklist

Work through these categories in order. For each finding, cite the file, line, and
the specific guideline being violated. Skip categories that don't apply to the scope.

### 1. Naming & API Design

Read `references/api-design.md` for the complete rules.

Key checks:
- Types use `UpperCamelCase`, everything else uses `lowerCamelCase`
- Methods read as grammatical English at the call site: `x.insert(y, at: z)`
- Names describe roles, not types: `greeting` not `string`
- Mutating/nonmutating pairs follow the `-ed`/`-ing` convention
- Boolean properties read as assertions: `isEmpty`, `isValid`
- Factory methods start with `make`
- Protocol names use nouns for "what it is", `-able`/`-ible` for capabilities
- Argument labels form grammatical phrases with the method name
- No abbreviations unless universally understood (`min`, `max`, `URL`)

### 2. Code Style & Formatting

Read `references/code-style.md` for the complete rules.

Key checks:
- 100-character line limit
- K&R brace style (opening brace on same line)
- No semicolons
- One statement per line
- `//` comments only, never `/* */`
- One variable per `let`/`var` declaration
- Trailing commas in multiline array/dictionary literals
- Imports grouped: standard modules, then individual declarations, then `@testable`
- `// MARK:` comments to organize type members
- Shorthand syntax for arrays `[Element]`, dictionaries `[Key: Value]`, optionals `T?`

### 3. Swift Patterns & Idioms

Read `references/swift-patterns.md` for the complete rules.

Key checks:
- `guard` for early exits instead of nested `if` blocks
- `for-where` instead of `for` + single `if` body
- `Optional` over sentinel values (`-1`, empty string)
- Errors thrown, not merged with return types
- No force-unwrap (`!`) without a comment explaining the invariant
- No implicitly unwrapped optionals except `@IBOutlet` and test fixtures
- Explicit access control where it differs from `internal`
- Nested types for scoping (error types, flag enums inside their parent)
- Prefer `let` over `var` when value doesn't change
- Prefer value types (`struct`, `enum`) over `class` when no identity needed
- Protocol extensions for default implementations, not base classes
- Computed properties omit `get` when read-only

### 4. Build Performance

Read `references/performance.md` for the complete rules.

Key checks:
- No complex expressions that slow type-checker (break into smaller statements)
- Explicit types on complex closures and collection literals
- Minimize use of `AnyObject`, `Any` — prefer concrete or generic types
- No unnecessary `@objc` or `dynamic` unless needed for Objective-C interop
- Module boundaries are clean — no circular dependencies
- Prefer `final` on classes not designed for inheritance (enables compiler optimizations)
- Large expressions broken into smaller sub-expressions with explicit types
- No excessive protocol conformance in extensions across files (merge where logical)

### 5. Memory Management

Read `references/memory-management.md` for the complete rules.

Key checks:
- No retain cycles in closures — use `[weak self]` or `[unowned self]` appropriately
- `weak` preferred over `unowned` unless lifetime is guaranteed
- Delegates declared as `weak var`
- Large resources freed in `deinit` or on memory warnings
- Discardable resource caches use `NSCache` with count/cost limits; deterministic
  maps or non-discardable data may use bounded dictionaries
- Autoreleasepool used in tight loops creating many temporary objects
- No strong reference chains between parent and child objects
- Image and data caches have size limits
- Observation tokens stored and invalidated properly

### 6. Testing

Read `references/testing.md` for the complete rules.

Key checks:
- Test methods named descriptively: `test_<condition>_<expectedResult>`
- One assertion concept per test (test may have setup + multiple related asserts)
- No test interdependencies — each test stands alone
- `setUp()` / `tearDown()` used for shared fixtures, not duplicated in every test
- Async code tested with expectations or Swift concurrency
- UI tests separated from unit tests
- Edge cases covered: nil, empty, boundary values, error paths
- No network calls in unit tests — use protocols and mocks
- Force-unwrap permitted in tests (fails the test if nil, which is desired)

### 7. Documentation

Key checks:
- Public API has `///` doc comments with summary, parameters, returns, throws
- Doc comments use verb phrases for methods, noun phrases for properties
- No `/** */` block comment syntax
- `Parameter`, `Returns`, `Throws` tags in that order
- Complex algorithms have inline comments explaining why, not what

### 8. Concurrency (if applicable)

Key checks:
- `@Sendable` closures don't capture mutable state
- Actors used for mutable shared state instead of locks
- `MainActor` for UI updates
- No data races — `nonisolated` used intentionally
- Structured concurrency (`async let`, `TaskGroup`) preferred over unstructured `Task {}`
- Cancellation handled properly

## Output Format

Structure the review as:

```
## Summary
<1-2 sentence overall assessment>

## Findings

### Critical
<issues that will cause bugs, crashes, or data loss>

### Important
<style violations, performance issues, missing tests>

### Suggestions
<minor improvements, alternative approaches>

## What's Done Well
<2-3 things the code does right — always include this>
```

For each finding, include:
- **File and line**: `Sources/Auth/TokenManager.swift:42`
- **Category**: which checklist item it falls under
- **Issue**: what's wrong
- **Fix**: concrete code suggestion or direction

Keep findings actionable. Don't flag things that are clearly intentional project
conventions unless they cause real problems.
