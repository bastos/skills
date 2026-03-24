# Build Performance & Optimization

Based on [Apple's documentation on improving build efficiency](https://developer.apple.com/documentation/xcode/improving-build-efficiency-with-good-coding-practices)
and general Swift performance best practices.

## Build Time Optimization

### Type-Checker Complexity

The Swift type-checker's time grows exponentially with expression complexity.
These patterns slow builds significantly:

**Break complex expressions into sub-expressions:**

```swift
// ✗ Slow — type-checker infers all at once
let result = items.filter { $0.isActive }.map { $0.name }.sorted().joined(separator: ", ")

// ✓ Faster — explicit intermediate types
let activeItems = items.filter { $0.isActive }
let names: [String] = activeItems.map { $0.name }
let result = names.sorted().joined(separator: ", ")
```

**Add explicit types to complex closures:**

```swift
// ✗ Slow — compiler infers closure types across chains
let totals = orders.map { order in
    order.items.reduce(0) { $0 + $1.price * Double($1.quantity) }
}

// ✓ Faster — explicit types reduce inference work
let totals: [Double] = orders.map { (order: Order) -> Double in
    order.items.reduce(0.0) { (sum: Double, item: LineItem) -> Double in
        sum + item.price * Double(item.quantity)
    }
}
```

**Avoid complex collection literals without type annotations:**

```swift
// ✗ Slow — compiler infers deeply nested structure
let config = [
    "network": ["timeout": 30, "retries": 3],
    "cache": ["maxSize": 1024, "ttl": 3600],
]

// ✓ Faster
let config: [String: [String: Int]] = [
    "network": ["timeout": 30, "retries": 3],
    "cache": ["maxSize": 1024, "ttl": 3600],
]
```

**Avoid chained ternary operators and complex conditionals:**

```swift
// ✗ Slow
let value = a ? b : c ? d : e ? f : g

// ✓ Faster and clearer
let value: ResultType
switch (a, c, e) {
case (true, _, _): value = b
case (_, true, _): value = d
case (_, _, true): value = f
default: value = g
}
```

### String Concatenation

```swift
// ✗ Slow with many operands — type-checker checks all operator combinations
let message = "Hello " + name + ", you have " + String(count) + " items in " + location

// ✓ Use interpolation
let message = "Hello \(name), you have \(count) items in \(location)"
```

### Minimize Unnecessary Recompilation

- Keep files focused — changes to a large file recompile more dependents
- Use `private` and `fileprivate` — changing private APIs doesn't trigger
  recompilation of other files
- Prefer `struct` over `class` — value types have simpler dependency graphs
- Avoid circular imports between modules

## Runtime Performance

### Use Final and Static Dispatch

```swift
// ✓ final enables direct dispatch (faster than vtable)
final class Parser {
    func parse(_ input: String) -> AST { ... }
}

// ✓ static/class methods on final classes use direct dispatch
final class Formatter {
    static func format(_ date: Date) -> String { ... }
}

// ✓ private methods are implicitly final
class ViewModel {
    private func computeLayout() { ... }  // direct dispatch
}
```

Whole-module optimization (`-whole-module-optimization`) can infer finality
automatically, but explicit `final` makes intent clear and works in debug builds too.

### Avoid Unnecessary Dynamic Dispatch

```swift
// ✗ @objc/dynamic forces message dispatch (slowest)
class MyClass {
    @objc dynamic func update() { ... }  // only if needed for KVO/selectors
}

// ✓ Omit @objc unless Objective-C interop requires it
class MyClass {
    func update() { ... }
}
```

### Use Value Types for Performance-Critical Paths

Value types (structs, enums) avoid:
- Reference counting overhead
- Heap allocation (small structs live on the stack)
- Cache misses from pointer indirection

```swift
// ✓ Value type for frequently created/destroyed objects
struct Point {
    var x: Double
    var y: Double
}

// Beware: large structs negate the benefit — copying becomes expensive
// If your struct has many stored properties or contains reference types,
// measure before assuming struct is faster
```

### Copy-on-Write for Large Value Types

Swift's standard library types (`Array`, `Dictionary`, `String`, `Set`) use
copy-on-write. Custom large value types should implement CoW if they're frequently
copied:

```swift
struct LargeData {
    private var storage: Storage

    // CoW pattern
    private var storageForWriting: Storage {
        mutating get {
            if !isKnownUniquelyReferenced(&storage) {
                storage = storage.copy()
            }
            return storage
        }
    }
}
```

### Prefer Lazy Initialization

```swift
// ✓ Computed only when first accessed
lazy var dateFormatter: DateFormatter = {
    let formatter = DateFormatter()
    formatter.dateStyle = .medium
    formatter.timeStyle = .short
    return formatter
}()

// ✓ Lazy sequences avoid allocating intermediate arrays
let firstTenActive = items.lazy.filter { $0.isActive }.prefix(10)
```

### Protocol Existentials vs Generics

```swift
// ✗ Existential — dynamic dispatch, heap allocation for large values
func process(items: [any Processable]) { ... }

// ✓ Generic — static dispatch, specialized at compile time
func process<T: Processable>(items: [T]) { ... }

// ✓ some — opaque type, same benefits as generic
func makeView() -> some View { ... }
```

Use `any` protocol types only when you truly need heterogeneous collections.
Prefer `some` or generic constraints for homogeneous use.

### Collection Performance

```swift
// ✓ Reserve capacity when size is known
var results: [String] = []
results.reserveCapacity(items.count)

// ✓ Use contains instead of filter(...).isEmpty
if items.contains(where: { $0.isExpired }) { ... }

// ✓ Use first(where:) instead of filter(...).first
if let match = items.first(where: { $0.id == targetID }) { ... }

// ✓ Use Dictionary(grouping:by:) for grouping
let grouped = Dictionary(grouping: users, by: { $0.department })
```

### Avoid Unnecessary Allocations in Loops

```swift
// ✗ Creates a new DateFormatter every iteration
for date in dates {
    let formatter = DateFormatter()
    formatter.dateStyle = .medium
    labels.append(formatter.string(from: date))
}

// ✓ Reuse the formatter
let formatter = DateFormatter()
formatter.dateStyle = .medium
for date in dates {
    labels.append(formatter.string(from: date))
}
```
