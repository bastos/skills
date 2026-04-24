# Memory Management

Based on [Apple's documentation on preventing memory-use regressions](https://developer.apple.com/documentation/xcode/preventing-memory-use-regressions)
and [responding to low-memory warnings](https://developer.apple.com/documentation/xcode/responding-to-low-memory-warnings).

## ARC and Retain Cycles

### The Core Problem

ARC (Automatic Reference Counting) frees objects when their reference count reaches
zero. Retain cycles happen when two objects hold strong references to each other —
neither can be freed.

### Closures Are the Most Common Source

```swift
// ✗ Retain cycle — self holds closure, closure holds self
class ViewController: UIViewController {
    var onComplete: (() -> Void)?

    func setup() {
        onComplete = {
            self.dismiss(animated: true)  // strong capture of self
        }
    }
}

// ✓ Break the cycle with [weak self]
func setup() {
    onComplete = { [weak self] in
        self?.dismiss(animated: true)
    }
}
```

### When to Use Weak vs Unowned

| Modifier | Behavior when target deallocates | Use when... |
|----------|--------------------------------|-------------|
| `weak` | Becomes `nil` (must be optional) | Target might be deallocated first |
| `unowned` | Crashes (trap) | You're certain target outlives the reference |

**Default to `weak`** — the `nil` check is cheap and safe. Use `unowned` only when
the lifetime relationship is guaranteed and documented:

```swift
// ✓ weak — ViewController might be dismissed while request is in-flight
networkClient.fetch { [weak self] result in
    guard let self else { return }
    self.update(with: result)
}

// ✓ unowned — parent always outlives child in this design
class Child {
    unowned let parent: Parent  // parent created child, will outlive it
}
```

### Delegates Must Be Weak

```swift
// ✓
protocol DownloadDelegate: AnyObject {
    func downloadDidComplete(_ download: Download)
}

class Download {
    weak var delegate: DownloadDelegate?
}
```

The `: AnyObject` constraint is required to use `weak` — value types can't be weak
references.

### Common Retain Cycle Patterns

**Timer retains its target:**
```swift
// ✗ Timer retains self strongly
timer = Timer.scheduledTimer(
    timeInterval: 1.0,
    target: self,        // strong reference
    selector: #selector(tick),
    userInfo: nil,
    repeats: true
)

// ✓ Use closure-based API with weak capture
timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
    self?.tick()
}
```

**NotificationCenter (pre-iOS 9 or block-based):**
```swift
// ✓ Store token, remove in deinit
private var token: NSObjectProtocol?

func setup() {
    token = NotificationCenter.default.addObserver(
        forName: .didUpdate,
        object: nil,
        queue: .main
    ) { [weak self] notification in
        self?.handleUpdate(notification)
    }
}

deinit {
    if let token {
        NotificationCenter.default.removeObserver(token)
    }
}
```

**Combine subscriptions:**
```swift
// ✓ Store in cancellable set
private var cancellables = Set<AnyCancellable>()

publisher
    .sink { [weak self] value in
        self?.process(value)
    }
    .store(in: &cancellables)
```

## Memory Pressure and Caching

### Use NSCache for Discardable Resource Caches

`NSCache` can evict entries under memory pressure and supports count/cost limits,
which makes it a good fit for transient, recomputable resources. Its limits are
not strict guarantees, and raw dictionaries are still appropriate for
deterministic maps or non-discardable data when they are explicitly bounded:

```swift
// OK for deterministic, bounded maps that must retain their values
var imageCache: [URL: UIImage] = [:]

// Good for discardable image data
let imageCache = NSCache<NSURL, UIImage>()
imageCache.countLimit = 100
imageCache.totalCostLimit = 50 * 1024 * 1024  // 50 MB
```

### Respond to Memory Warnings

```swift
// UIKit
override func didReceiveMemoryWarning() {
    super.didReceiveMemoryWarning()
    clearNonEssentialCaches()
}

// Or observe the notification
NotificationCenter.default.addObserver(
    forName: UIApplication.didReceiveMemoryWarningNotification,
    object: nil,
    queue: .main
) { [weak self] _ in
    self?.clearNonEssentialCaches()
}
```

What to release on memory warning:
- Cached images and data that can be recreated
- Precomputed results that can be recomputed
- Off-screen view hierarchies
- Downloaded content that can be re-fetched

What NOT to release:
- User's unsaved work
- Active network connections
- State needed to restore the current screen

### Image Memory

Images are the biggest memory consumer in most iOS apps:

```swift
// ✓ Downsample large images to display size
func downsample(imageAt url: URL, to pointSize: CGSize, scale: CGFloat) -> UIImage? {
    let maxDimensionInPixels = max(pointSize.width, pointSize.height) * scale
    let options = [kCGImageSourceShouldCache: false] as CFDictionary
    guard let source = CGImageSourceCreateWithURL(url as CFURL, options) else { return nil }

    let downsampleOptions = [
        kCGImageSourceCreateThumbnailFromImageAlways: true,
        kCGImageSourceShouldCacheImmediately: true,
        kCGImageSourceCreateThumbnailWithTransform: true,
        kCGImageSourceThumbnailMaxPixelSize: maxDimensionInPixels,
    ] as CFDictionary

    guard let cgImage = CGImageSourceCreateThumbnailAtIndex(source, 0, downsampleOptions) else {
        return nil
    }
    return UIImage(cgImage: cgImage)
}

// ✗ Loading full-resolution image into a small thumbnail view
cell.imageView.image = UIImage(contentsOfFile: path)  // might be 4000x3000
```

### Autorelease Pools

Use `autoreleasepool` in tight loops that create many temporary Objective-C objects:

```swift
// ✓ Prevents memory spike from accumulated autoreleased objects
for path in thousandsOfPaths {
    autoreleasepool {
        let image = UIImage(contentsOfFile: path)
        let thumbnail = image?.preparingThumbnail(of: thumbnailSize)
        saveThumbnail(thumbnail, for: path)
    }
}
```

This is mainly relevant when interoperating with Objective-C APIs. Pure Swift value
types don't use autorelease pools.

## Preventing Leaks

### Diagnosis Checklist

When investigating memory issues:

1. **Instruments > Leaks**: finds objects that are allocated but unreachable
2. **Instruments > Allocations**: shows growth over time — look for steady climbs
3. **Memory Graph Debugger** (Xcode): visualizes reference relationships — follow
   the arrows to find cycles
4. **Malloc Stack Logging**: records allocation backtraces

### Common Leak Patterns

| Pattern | Fix |
|---------|-----|
| Closure captures `self` strongly | `[weak self]` or `[unowned self]` |
| Delegate is strong reference | `weak var delegate` |
| Timer retains target | Use closure-based timer with `[weak self]` |
| NotificationCenter observer not removed | Store token, remove in `deinit` |
| Combine sink without `[weak self]` | Add `[weak self]` to sink closure |
| KVO observation not invalidated | Store and invalidate tokens |
| Strong reference in collection | Use `NSHashTable.weakObjects()` or `NSMapTable` |
| Dispatch work item captures self | Capture weakly or cancel in `deinit` |

### Testing for Memory Leaks

```swift
// Track that an object is deallocated after use
func testViewControllerDeallocated() {
    var vc: MyViewController? = MyViewController()
    weak var weakVC = vc

    // Exercise the view controller
    vc?.loadViewIfNeeded()
    vc?.viewDidAppear(false)

    // Release it
    vc = nil

    // Verify it was deallocated
    XCTAssertNil(weakVC, "ViewController should have been deallocated")
}
```

## Concurrency and Memory

### Actor Isolation Prevents Data Races (Not Leaks)

Actors prevent concurrent access but don't solve retain cycles. You still need
`[weak self]` in closures that capture actor-isolated objects:

```swift
actor DataManager {
    private var cache: [String: Data] = [:]

    func fetch(key: String) async -> Data? {
        if let cached = cache[key] { return cached }
        let data = await networkFetch(key)
        cache[key] = data
        return data
    }
}
```

### Task Cancellation and Cleanup

```swift
// ✓ Check for cancellation to avoid unnecessary work
func processLargeDataset() async throws {
    for chunk in dataset.chunks(ofCount: 1000) {
        try Task.checkCancellation()
        await process(chunk)
    }
}
```

Unstructured `Task {}` blocks capture their context — make sure to cancel them
when the enclosing scope is done:

```swift
class ViewModel {
    private var fetchTask: Task<Void, Never>?

    func startFetching() {
        fetchTask = Task { [weak self] in
            // ...
        }
    }

    deinit {
        fetchTask?.cancel()
    }
}
```
