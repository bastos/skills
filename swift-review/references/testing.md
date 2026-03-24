# Testing Best Practices

Based on [Apple's documentation on adding tests to Xcode projects](https://developer.apple.com/documentation/xcode/adding-tests-to-your-xcode-project)
and Swift testing conventions.

## Test Organization

### Project Structure

```
MyApp/
├── Sources/
│   ├── Models/
│   ├── Services/
│   └── Views/
├── Tests/
│   ├── UnitTests/          # Fast, isolated tests
│   │   ├── Models/
│   │   └── Services/
│   └── UITests/            # Slow, full-app tests
│       └── Flows/
```

- Mirror the source directory structure in tests
- Keep unit tests and UI tests in separate targets
- One test file per source file (e.g., `Parser.swift` → `ParserTests.swift`)

### Test Naming

Names should describe the scenario and expected outcome:

```swift
// Pattern: test_<methodOrScenario>_<expectedBehavior>
func test_parse_validJSON_returnsUser() { ... }
func test_parse_invalidJSON_throwsDecodingError() { ... }
func test_parse_emptyData_returnsNil() { ... }

// Also acceptable: descriptive camelCase
func testParseValidJSONReturnsUser() { ... }
func testParseInvalidJSONThrowsDecodingError() { ... }
```

Avoid vague names:
```swift
// ✗ What does it test?
func testParse() { ... }
func testSuccess() { ... }
func testError() { ... }
```

## XCTest Patterns

### Basic Structure

```swift
import XCTest
@testable import MyApp

final class ParserTests: XCTestCase {

    // MARK: - Properties

    private var sut: Parser!  // system under test

    // MARK: - Setup / Teardown

    override func setUp() {
        super.setUp()
        sut = Parser()
    }

    override func tearDown() {
        sut = nil
        super.tearDown()
    }

    // MARK: - Tests

    func test_parse_validInput_returnsExpectedResult() {
        let input = "valid data"

        let result = sut.parse(input)

        XCTAssertEqual(result.name, "expected")
    }
}
```

### Arrange-Act-Assert

Every test should have three clear sections:

```swift
func test_calculateTotal_withDiscount_appliesCorrectly() {
    // Arrange
    let items = [Item(price: 100), Item(price: 200)]
    let discount = Discount(percentage: 10)

    // Act
    let total = calculator.calculateTotal(items: items, discount: discount)

    // Assert
    XCTAssertEqual(total, 270.0, accuracy: 0.01)
}
```

### One Concept Per Test

```swift
// ✗ Testing multiple unrelated things
func testUser() {
    XCTAssertEqual(user.name, "Alice")
    XCTAssertTrue(user.isActive)
    XCTAssertEqual(user.friends.count, 3)
    XCTAssertNotNil(user.avatar)
}

// ✓ Focused tests
func test_newUser_hasCorrectName() {
    XCTAssertEqual(user.name, "Alice")
}

func test_newUser_isActive() {
    XCTAssertTrue(user.isActive)
}
```

Multiple related assertions within the same concept are fine:
```swift
// ✓ Multiple assertions about the same concept (coordinate parsing)
func test_parseCoordinate_validInput_returnsCorrectValues() {
    let coord = Coordinate.parse("37.7749,-122.4194")

    XCTAssertEqual(coord?.latitude, 37.7749, accuracy: 0.0001)
    XCTAssertEqual(coord?.longitude, -122.4194, accuracy: 0.0001)
}
```

### Test Independence

Each test must stand alone — no dependencies on execution order or shared mutable state:

```swift
// ✗ Tests depend on each other
func testCreateUser() {
    user = User(name: "Alice")  // shared state
    XCTAssertNotNil(user)
}

func testUserName() {
    XCTAssertEqual(user.name, "Alice")  // depends on testCreateUser
}

// ✓ Each test creates its own state
func test_user_creation() {
    let user = User(name: "Alice")
    XCTAssertNotNil(user)
}

func test_user_name() {
    let user = User(name: "Alice")
    XCTAssertEqual(user.name, "Alice")
}
```

## Swift Testing Framework

For projects using the newer Swift Testing framework (available from Xcode 16+):

```swift
import Testing
@testable import MyApp

struct ParserTests {
    let sut = Parser()

    @Test("Parsing valid JSON returns User")
    func parseValidJSON() throws {
        let json = #"{"name": "Alice", "age": 30}"#.data(using: .utf8)!

        let user = try sut.parse(json)

        #expect(user.name == "Alice")
        #expect(user.age == 30)
    }

    @Test("Parsing invalid JSON throws")
    func parseInvalidJSON() {
        let data = "not json".data(using: .utf8)!

        #expect(throws: DecodingError.self) {
            try sut.parse(data)
        }
    }

    @Test("Parsing with various formats", arguments: [
        ("compact", #"{"name":"Alice"}"#),
        ("pretty", #"{ "name" : "Alice" }"#),
    ])
    func parseFormats(label: String, json: String) throws {
        let data = json.data(using: .utf8)!
        let user = try sut.parse(data)
        #expect(user.name == "Alice")
    }
}
```

## Async Testing

### XCTest Async

```swift
func test_fetchUser_returnsValidUser() async throws {
    let user = try await service.fetchUser(id: "123")

    XCTAssertEqual(user.name, "Alice")
}
```

### Expectations for Callback-Based APIs

```swift
func test_download_completesSuccessfully() {
    let expectation = expectation(description: "Download completes")

    downloader.download(url: testURL) { result in
        if case .success = result {
            expectation.fulfill()
        }
    }

    waitForExpectations(timeout: 5.0)
}
```

## Test Doubles

### Use Protocols for Testability

```swift
// Production code depends on protocol
protocol NetworkClient {
    func fetch(_ url: URL) async throws -> Data
}

// Real implementation
struct URLSessionClient: NetworkClient {
    func fetch(_ url: URL) async throws -> Data {
        let (data, _) = try await URLSession.shared.data(from: url)
        return data
    }
}

// Test double
struct MockNetworkClient: NetworkClient {
    var stubbedData: Data = Data()
    var stubbedError: Error?

    func fetch(_ url: URL) async throws -> Data {
        if let error = stubbedError { throw error }
        return stubbedData
    }
}
```

### No Network Calls in Unit Tests

Unit tests must be fast and deterministic — never hit the network:

```swift
// ✗ Flaky — depends on network
func test_fetchUsers() async throws {
    let users = try await realAPIClient.fetchUsers()
    XCTAssertFalse(users.isEmpty)
}

// ✓ Deterministic — uses mock
func test_fetchUsers_returnsDecodedUsers() async throws {
    let mockData = """
    [{"name": "Alice"}, {"name": "Bob"}]
    """.data(using: .utf8)!
    let client = MockNetworkClient(stubbedData: mockData)
    let service = UserService(client: client)

    let users = try await service.fetchUsers()

    XCTAssertEqual(users.count, 2)
    XCTAssertEqual(users[0].name, "Alice")
}
```

## Edge Cases to Cover

Every test suite should consider:

| Category | Examples |
|----------|----------|
| Empty/nil | Empty string, empty array, nil optional |
| Boundary | First/last element, max/min values, zero |
| Error paths | Invalid input, network failure, permission denied |
| Concurrency | Concurrent access, cancellation, timeout |
| Unicode | Emoji, RTL text, multi-byte characters |
| Large data | Performance with 10K+ items |

## Testing for Memory Leaks

```swift
func test_viewController_deallocatesAfterDismissal() {
    var vc: MyViewController? = MyViewController()
    weak var weakVC = vc

    vc?.loadViewIfNeeded()
    vc = nil

    XCTAssertNil(weakVC, "Expected ViewController to be deallocated")
}
```

## Force Unwrap in Tests

Force-unwrap (`!`) and force-try (`try!`) are acceptable in tests because failure
causes the test to fail (which is the desired outcome):

```swift
func test_decode_validJSON() {
    let data = validJSON.data(using: .utf8)!  // ✓ OK in tests
    let user = try! decoder.decode(User.self, from: data)  // ✓ OK in tests

    XCTAssertEqual(user.name, "Alice")
}
```

However, prefer `XCTUnwrap` for clearer failure messages:

```swift
func test_decode_validJSON() throws {
    let data = try XCTUnwrap(validJSON.data(using: .utf8))
    let user = try decoder.decode(User.self, from: data)

    XCTAssertEqual(user.name, "Alice")
}
```
