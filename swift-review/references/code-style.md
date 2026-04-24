# Code Style & Formatting

Based on [Google Swift Style Guide](https://google.github.io/swift/).

## File Organization

### File Naming
- Single-type files: `MyType.swift`
- Protocol conformance extensions: `MyType+MyProtocol.swift`
- General extensions: `MyType+Additions.swift`

### Import Ordering
Group imports in this order, separated by blank lines, lexicographic within each group:
1. Standard/system modules (`Foundation`, `UIKit`)
2. Individual declaration imports
3. `@testable` imports

```swift
import CoreData
import Foundation
import UIKit

@testable import MyApp
```

### Type Organization
- One top-level type per file (related types like a class + delegate protocol are OK)
- Use `// MARK:` to group members logically
- Use `// MARK: -` to create visual dividers
- Overloaded methods appear sequentially with no intervening code

## Formatting Rules

### Line Length
- **100-character maximum** per line
- Exceptions: long URLs in comments, import statements

### Braces (K&R Style)
Opening brace on same line, closing brace on its own line:

```swift
if condition {
    doSomething()
} else {
    doOther()
}

func method() {
    // body
}
```

Exceptions:
- Empty blocks: `{}`
- Single-statement blocks may be on one line: `guard condition else { return }`

### Semicolons
Never. Not to terminate, not to separate.

### One Statement Per Line
```swift
// ✗
let a = 1; let b = 2

// ✓
let a = 1
let b = 2
```

### One Variable Per Declaration
```swift
// ✗
let a = 1, b = 2

// ✓
let a = 1
let b = 2
```

Exception: tuple destructuring is OK: `let (x, y) = point`

### Line-Wrapping

**Cardinal rules:**
1. If the whole thing fits on one line, keep it there
2. Comma-delimited lists: all horizontal OR all vertical (don't mix)
3. Continuation lines indented +2 from original
4. Opening brace stays with the final continuation line

**Function declarations:**
```swift
// Short — one line
func move(from start: Point, to end: Point) { ... }

// Long — each param on its own line, indented +2
func move(
  from start: Point,
  to end: Point,
  duration: TimeInterval,
  completion: @escaping () -> Void
) {
    // body
}
```

**Function calls:**
```swift
// Short — one line
let result = calculate(x: 1, y: 2)

// Long — each argument on its own line
let result = calculate(
  x: longVariableName,
  y: anotherLongVariable,
  z: thirdParameter
)
```

**Guard statements:**
Keep `else {` together:
```swift
guard let value = optional else {
    return
}

guard
  let first = a,
  let second = b,
  first > second
else {
    return
}
```

### Horizontal Whitespace

**Space required:**
- After `if`, `guard`, `while`, `switch`, `for` before `(`
- Both sides of `{` and `}` when on same line as other code
- Both sides of binary and ternary operators
- After `,` in lists
- After `:` in type annotations, dictionary literals, case items
- Before and after `//` in end-of-line comments

**No space:**
- Around `.` for member access
- Around `..<` and `...` range operators
- Before `:` in superclass/protocol conformance

### Vertical Whitespace
- Single blank line between type members
- Blank lines optional between closely related properties
- Blank lines between logical sections of a function body
- Multiple consecutive blank lines are OK if used consistently (not generally recommended)

### Trailing Commas
**Required** in multiline array and dictionary literals (cleaner diffs):

```swift
let colors = [
    .red,
    .green,
    .blue,   // ← trailing comma
]
```

### Comments
- Use `//` only. Never `/* */`.
- Non-doc comments get at least two spaces before `//`

### Switch Statements
- Cases at same indentation as `switch`
- Case body indented +2

```swift
switch value {
case .first:
    handleFirst()
case .second, .third:
    handleOther()
default:
    break
}
```

### Enum Cases
- One case per line generally
- No empty parentheses on cases without associated values
- `indirect enum` preferred over `indirect case` when all cases are indirect

### Trailing Closures
- Single closure as final argument → trailing syntax
- Multiple trailing closures are valid Swift; use them when they improve
  readability or match project/SwiftUI style, otherwise keep all closures inside
  parentheses and labeled
- No empty `()` when function called with only a trailing closure

```swift
// ✓ Single closure — use trailing syntax
items.map { $0.name }

// ✓ Multiple closures — labeled inside parens
UIView.animate(
    withDuration: 0.3,
    animations: { view.alpha = 0 },
    completion: { _ in view.removeFromSuperview() }
)

// ✓ Multiple trailing closures — idiomatic in SwiftUI-style APIs
UIView.animate(withDuration: 0.3) {
    view.alpha = 0
} completion: { _ in
    view.removeFromSuperview()
}
```

## Type Shorthand

Always use shorthand:

| Shorthand | Long form (avoid) |
|-----------|-------------------|
| `[Element]` | `Array<Element>` |
| `[Key: Value]` | `Dictionary<Key, Value>` |
| `Wrapped?` | `Optional<Wrapped>` |

Use long form only when the compiler requires it (e.g., `Array<Element>.Index`).

For function types: return `Void`, parameter `()`.

## Numeric Literals

Use underscores for readability in long numbers:
```swift
let million = 1_000_000
let hexColor = 0xFF_AA_00
let binary = 0b1010_1100
```

## Attributes

- Parameterized attributes (`@available(...)`) on their own line
- Non-parameterized attributes may share a line with the declaration

```swift
@available(iOS 15, *)
@MainActor
public func fetchData() async throws -> Data {
    // ...
}
```
