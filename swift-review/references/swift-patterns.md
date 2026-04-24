# Swift Patterns & Idioms

Based on [Google Swift Style Guide](https://google.github.io/swift/),
[Swift.org API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/),
and patterns from [Apple's open-source Swift projects](https://github.com/apple/container).

## Value Types vs Reference Types

Prefer `struct` and `enum` over `class` unless you need:
- Identity (comparing with `===`)
- Inheritance
- Shared mutable state (consider actors first)
- Objective-C interop

Value types give you:
- Better local reasoning and fewer accidental shared mutations
- Predictable copy semantics
- Compiler optimizations (stack allocation, copy-on-write)

Value types do not guarantee thread safety on their own; shared mutable storage,
copy-on-write collections, and reference-typed members still require normal
concurrency discipline.

```swift
// ✓ Value type — no identity needed
struct Coordinate {
    var latitude: Double
    var longitude: Double
}

// ✓ Reference type — shared mutable state
class CacheManager {
    static let shared = CacheManager()
    private var store: [String: Data] = [:]
}
```

## Optionals

### Prefer Optional Over Sentinels

```swift
// ✗ Sentinel value
func indexOf(_ element: Element) -> Int  // returns -1 if not found

// ✓ Optional communicates absence
func indexOf(_ element: Element) -> Int?
```

### Safe Unwrapping

```swift
// ✓ guard for early exit
guard let user = fetchUser() else {
    return
}

// ✓ if-let for conditional use
if let name = user.nickname {
    greet(name)
}

// ✓ nil-coalescing for defaults
let name = user.nickname ?? "Anonymous"

// ✓ Optional chaining
let count = user.friends?.count

// ✗ Force unwrap without justification
let name = user.nickname!

// Acceptable: force unwrap with documented invariant
let regex = try! NSRegularExpression(pattern: "^[a-z]+$")
// Pattern is a compile-time constant — only fails if programmer made a typo
```

### Implicitly Unwrapped Optionals

Only permitted for:
- `@IBOutlet` properties (lifecycle-managed by storyboard)
- Test fixtures initialized in `setUp()`
- Rare documented lifecycle invariants where the value is valid before every
  possible access. Prefer initializer injection or normal optionals.

```swift
class ViewController: UIViewController {
    @IBOutlet weak var titleLabel: UILabel!  // ✓ IBOutlet

    var viewModel: ViewModel!  // ✗ Prefer optional or non-optional init
}
```

## Error Handling

### Throw Errors, Don't Merge with Return Types

```swift
// ✗ Error merged with return — caller might ignore
func parse(_ data: Data) -> Result?

// ✓ Errors are explicit
func parse(_ data: Data) throws -> Result
```

### Error Type Design

Nest error types inside the type they relate to:

```swift
struct Parser {
    enum Error: Swift.Error {
        case invalidFormat(String)
        case unexpectedToken(Token)
        case overflow
    }

    func parse(_ input: String) throws -> AST {
        // ...
    }
}
```

### Force-Try Rules

- **Prohibited** in production code without a comment explaining the invariant
- **Permitted** in tests (failure = test failure, which is the desired outcome)
- **Permitted** for compile-time constants (regex literals, known-good JSON)

## Access Control

### Prefer Explicit Access Levels

Use access control to communicate intent, not just naming conventions:

```swift
// ✓ Access control makes intent clear
public struct APIClient {
    public let baseURL: URL

    private let session: URLSession
    private let decoder: JSONDecoder

    public func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        // ...
    }

    private func buildRequest(for endpoint: Endpoint) -> URLRequest {
        // ...
    }
}
```

### Guidelines

- `private` for implementation details used only in the current declaration
- `fileprivate` when access is needed across declarations in the same file
- `internal` (default) for module-internal APIs
- `public` for module API surface
- `open` only when subclassing/overriding is a designed extension point

Don't use `open` by default on classes — use `final` unless you've designed for inheritance.

## Guard and Early Exits

`guard` shines when the main logic is the common case and errors/edge cases should
exit early:

```swift
// ✓ Guard — main logic stays flush left
func processOrder(_ order: Order?) throws -> Receipt {
    guard let order = order else {
        throw OrderError.missing
    }
    guard order.items.isEmpty == false else {
        throw OrderError.empty
    }
    guard order.paymentMethod.isValid else {
        throw OrderError.invalidPayment
    }

    // Main logic here — no nesting
    let total = order.items.reduce(0) { $0 + $1.price }
    return Receipt(total: total)
}

// ✗ Nested ifs — pyramid of doom
func processOrder(_ order: Order?) throws -> Receipt {
    if let order = order {
        if !order.items.isEmpty {
            if order.paymentMethod.isValid {
                let total = order.items.reduce(0) { $0 + $1.price }
                return Receipt(total: total)
            }
        }
    }
    throw OrderError.invalid
}
```

## For-Where Loops

When the entire loop body is a single `if` block, use `where`:

```swift
// ✗
for item in items {
    if item.isActive {
        process(item)
    }
}

// ✓
for item in items where item.isActive {
    process(item)
}
```

## Protocol-Oriented Design

### Use Protocols for Abstraction

```swift
// ✓ Protocol defines capability
protocol DataStore {
    func save(_ data: Data, forKey key: String) throws
    func load(forKey key: String) throws -> Data?
    func delete(forKey key: String) throws
}

// ✓ Default implementations via extension
extension DataStore {
    func exists(forKey key: String) -> Bool {
        (try? load(forKey: key)) != nil
    }
}
```

### Prefer Composition Over Inheritance

```swift
// ✗ Deep inheritance hierarchy
class BaseViewController: UIViewController { ... }
class ListViewController: BaseViewController { ... }
class FilterableListViewController: ListViewController { ... }

// ✓ Protocol composition
protocol Filterable { ... }
protocol Searchable { ... }

class ListViewController: UIViewController, Filterable, Searchable { ... }
```

## Nesting for Scope

Nest types when they're only meaningful in the context of their parent:

```swift
struct NetworkClient {
    enum Error: Swift.Error {
        case timeout
        case unauthorized
        case serverError(Int)
    }

    struct Configuration {
        var baseURL: URL
        var timeout: TimeInterval
        var retryCount: Int
    }
}

// Usage reads clearly
let config = NetworkClient.Configuration(...)
catch NetworkClient.Error.timeout { ... }
```

## Prefer Let Over Var

Use `let` by default. Only use `var` when the value needs to change:

```swift
// ✓
let name = user.fullName
let items = order.lineItems.filter { $0.isActive }

// Only var when mutation is needed
var total = 0.0
for item in items {
    total += item.price
}
```

## Final by Default

Mark classes `final` unless designed for subclassing:

```swift
// ✓ Not designed for inheritance
final class APIClient { ... }

// ✓ Designed extension point — document why
open class Theme {
    /// Override to provide custom colors for your brand.
    open var primaryColor: UIColor { .systemBlue }
}
```

`final` enables compiler optimizations (static dispatch) and communicates that the
class's behavior is not meant to be customized through subclassing.

## Custom Operators

Generally avoid. They reduce readability for anyone not familiar with them:

```swift
// ✗ Custom operator — what does this mean?
let result = data <~~ "key"

// ✓ Clear method call
let result = data.decode(key: "key")
```

Acceptable when the operator has clear domain meaning (mathematical notation)
and significantly improves readability.

## Switch Exhaustiveness

Let the compiler verify exhaustiveness for local or frozen enums — avoid
`default` when all cases are known:

```swift
// ✓ Compiler catches new cases
switch state {
case .loading:
    showSpinner()
case .loaded(let data):
    display(data)
case .error(let error):
    showError(error)
}

// ✗ default hides new cases
switch state {
case .loading:
    showSpinner()
default:
    break
}
```

For non-frozen enums imported from Apple SDKs or other resilient modules, handle
known cases and add `@unknown default` so the compiler warns when new cases are
introduced:

```swift
switch style {
case .light:
    configureLight()
case .dark:
    configureDark()
@unknown default:
    configureFallback()
}
```

## Apple Container Patterns

Patterns observed in Apple's open-source Swift projects like
[apple/container](https://github.com/apple/container):

- **Modular architecture**: separate modules per domain (`Build`, `Commands`, `Log`,
  `Persistence`, `Plugin`, `Resource`, `Version`)
- **Prefixed module names**: `ContainerBuild`, `ContainerLog` — namespace clarity at
  the module level
- **Infrastructure layers**: `CLI`, `Services`, `DNSServer` as standalone modules
- **Helpers and utilities**: shared code in a `Helpers` module, not scattered
- **XPC integration**: inter-process communication as its own module
- **Separation of concerns**: persistence, commands, and resources are distinct modules
  even when they collaborate
