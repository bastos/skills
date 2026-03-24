# API Design & Naming Guidelines

Based on [Swift.org API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/)
and [Google Swift Style Guide - Naming](https://google.github.io/swift/#naming).

## Core Principle

**Clarity at the point of use** is the most important goal. Every API should be
unambiguous when read at the call site, not just where it's declared.

If you struggle to describe an API's functionality in simple terms, you may have
designed the wrong API.

## Naming Rules

### Case Conventions

| Entity | Case | Example |
|--------|------|---------|
| Types, protocols | `UpperCamelCase` | `URLSession`, `Encodable` |
| Functions, properties, variables, enum cases | `lowerCamelCase` | `makeIterator()`, `startIndex` |
| Global constants | `lowerCamelCase` | `defaultTimeout` (not `kDefaultTimeout` or `DEFAULT_TIMEOUT`) |

Acronyms follow case uniformly based on position:
- Start of lowerCamelCase: all lowercase — `utf8Bytes`, `urlString`
- Anywhere in UpperCamelCase or mid-word: all uppercase — `HTTPRequest`, `isASCII`

### Include All Necessary Words

Omit words only when they repeat information already present at the call site:

```swift
// ✗ Ambiguous — remove what?
employees.remove(x)

// ✓ Clear
employees.remove(at: x)
```

### Don't Repeat Type Information

```swift
// ✗ Redundant
let nameString: String
func addColor(_ color: UIColor)

// ✓ Roles, not types
let name: String
func add(_ color: UIColor)
```

### Name Variables by Role

```swift
// ✗ Named by type
var string = "Hello"
var mainView: UIView

// ✓ Named by role
var greeting = "Hello"
var contentView: UIView
```

### Compensate for Weak Types

When a parameter type is `Any`, `AnyObject`, `NSObject`, or a fundamental type like
`Int` or `String`, use a descriptive noun before the parameter:

```swift
// ✗ Unclear what the string represents
func add(_ observer: NSObject, for keyPath: String)

// ✓ The noun clarifies the role
func addObserver(_ observer: NSObject, forKeyPath path: String)
```

## Method Naming

### Fluent Usage

Methods should read as grammatical English at the call site:

```swift
// ✓ "x, insert y at z"
x.insert(y, at: z)

// ✗ Awkward — "x, insert y position z"
x.insert(y, position: z)

// ✓ "friends, remove at index"
friends.remove(at: index)
```

### Side Effects Determine Form

**No side effects → noun phrase:**
```swift
x.distance(to: y)
collection.sorted()
i.successor()
```

**Side effects → imperative verb:**
```swift
x.sort()
x.append(y)
print(x)
```

### Mutating / Nonmutating Pairs

When an operation has both forms, name them consistently:

| Mutating (verb) | Nonmutating (noun/participle) |
|-----------------|-------------------------------|
| `x.sort()` | `z = x.sorted()` |
| `x.append(y)` | `z = x.appending(y)` |
| `x.reverse()` | `z = x.reversed()` |
| `y.formUnion(z)` | `x = y.union(z)` |

Rule: if the operation is naturally a verb, mutating uses the imperative and
nonmutating uses `-ed` or `-ing`. If it's naturally a noun, nonmutating uses the
noun and mutating prefixes with `form`.

### Factory Methods

Begin with `make`:
```swift
x.makeIterator()
factory.makeWidget(color: .red)
```

### Boolean Properties

Read as assertions about the receiver:
```swift
line1.intersects(line2)    // "line1 intersects line2"
collection.isEmpty         // "collection is empty"
view.isHidden              // "view is hidden"
```

## Protocol Naming

| Describes... | Naming pattern | Examples |
|-------------|---------------|----------|
| What something is | Noun | `Collection`, `Sequence`, `View` |
| A capability | `-able`, `-ible`, `-ing` | `Equatable`, `Hashable`, `ProgressReporting` |

Don't add `Protocol` suffix to avoid conflicts — rename the non-protocol type instead.

## Argument Labels

### When to Omit the First Label

**Value-preserving type conversions:**
```swift
Int64(someUInt32)          // omit label — widening conversion
String(describing: x)     // keep label — this isn't a simple conversion
```

**When the first argument completes a grammatical phrase with the method name:**
```swift
view.addSubview(y)         // "add subview y"
names.contains("Taylor")   // "names contains Taylor"
```

**When arguments can't be usefully distinguished:**
```swift
min(x, y)
zip(sequence1, sequence2)
```

### When to Include Labels

**Prepositional phrases:**
```swift
removeBoxes(havingLength: 12)
```

**All arguments after the first**, unless the call would be unambiguous without them.

**Arguments with default values** — always label these.

### Label Conventions for Delegates

Single argument (the source object) is unlabeled:
```swift
func scrollViewDidBeginScrolling(_ scrollView: UIScrollView)
func scrollViewShouldScrollToTop(_ scrollView: UIScrollView) -> Bool
func numberOfSections(in scrollView: UIScrollView) -> Int
```

Multiple arguments — source unlabeled, rest labeled with verbs/conditions:
```swift
func tableView(
    _ tableView: UITableView,
    willDisplayCell cell: UITableViewCell,
    forRowAt indexPath: IndexPath
)
```

## Documentation

Every public declaration needs a `///` doc comment:

```swift
/// Returns the element at the specified position.
///
/// - Parameter index: The position of the element to access. `index`
///   must be a valid index of the collection that is not equal to the
///   `endIndex` property.
/// - Returns: The element at the specified position.
/// - Throws: `CollectionError.outOfBounds` if the index is invalid.
/// - Complexity: O(1)
subscript(index: Index) -> Element { get }
```

Rules:
- Begin with a single-sentence summary (verb phrase for methods, noun phrase for properties)
- Tags in order: `Parameter(s)`, `Returns`, `Throws`, `Complexity`
- Use `///` format, never `/** */`
- If the summary tells the whole story, omit the tags

## Terminology

- Use established terms of art; don't invent synonyms
- Use `Array` not `List`, even if "list" is simpler
- Abbreviations allowed only when universally understood (`URL`, `ID`, `min`, `max`)
- If a term has an established meaning in the domain, use it precisely
