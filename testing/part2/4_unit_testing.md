## Unit Testing Deep Dive

### What to unit test

**Pure Functions**
```python
def calculate_total(items, tax_rate):
    subtotal = sum(item['price'] for item in items)
    tax = subtotal * tax_rate
    return subtotal + tax


def test_calculate_total_basic():
    items = [{'price': 10}, {'price': 20}]
    assert calculate_total(items, 0.1) == 33  # 30 + 3 tax

def test_calculate_total_empty_items():
    assert calculate_total([], 0.1) == 0  # Edge case: empty list

def test_calculate_total_zero_tax():
    items = [{'price': 50}]
    assert calculate_total(items, 0) == 50  # Boundary: no tax
```

**Why Pure Functions Matter:**
- **Deterministic behavior**: Generally same input = same output, making tests reliable
- **No hidden dependencies**: Everything the function needs is passed as parameters
- **Isolation by design**: No database calls, no API requests, no file I/O
- **Fast execution**: Microsecond test runs enable rapid feedback loops
- **Refactoring confidence**: Tests remain valid even when implementation changes

**Business Logic**
```python
from dataclasses import dataclass


@dataclass
class User:
    is_active: bool
    balance: float


@dataclass
class Item:
    price: float
    in_stock: bool


def can_user_purchase(user, item):
    return (
        user.is_active and 
        user.balance >= item.price and
        item.in_stock
    )

def test_active_user_with_sufficient_balance_can_purchase_in_stock_item():
    user = User(is_active=True, balance=100)
    item = Item(price=50, in_stock=True)
    assert can_user_purchase(user, item) == True

def test_inactive_user_cannot_purchase_even_with_balance():
    user = User(is_active=False, balance=100)
    item = Item(price=50, in_stock=True)
    assert can_user_purchase(user, item) == False

def test_out_of_stock_items_cannot_be_purchased():
    rich_user = User(is_active=True, balance=1000000)
    item = Item(price=50, in_stock=False)
    assert can_user_purchase(rich_user, item) == False
```

**Critical Concepts for Testing Business Logic:**
- **Test the intent/contract, not the implementation**: Focus on what the function promises to do
- **Each test should verify one business rule**: When a test fails, you know exactly which rule is broken
- **Use test names as documentation**: `test_inactive_user_cannot_purchase_regardless_of_balance()`
- **Consider all states**: Don't just test the happy path - what about suspended users, zero balance, pre-orders?

### The philosophy of edge cases

Edge cases aren't just about empty lists and null values - they're about understanding the boundaries of the system:

**Conceptual edge cases:**
- **State transitions**: What happens at the exact moment a user's subscription expires?
- **Concurrency edges**: Two requests modifying the same resource simultaneously
- **Precision boundaries**: Financial calculations at the limits of float precision
- **Business rule intersections**: When multiple rules conflict, which takes precedence?

**Why edge cases matter:**
- They reveal **implicit assumptions** in your code
- They force you to **define behavior explicitly**
- They often expose **architectural weaknesses**
- They're where **real-world bugs hide**

### Mocking and stubbing - understanding the why

**The Fundamental Principle**: Unit tests should test one unit in isolation. Mocking isn't about making tests easier - it's about achieving true isolation.

**What mocking really achieves:**
- **Deterministic tests**: Remove randomness and external variability
- **Speed**: Eliminate I/O operations that can make tests 1000x slower
- **Reliability**: No test failures due to network issues or database downtime
- **Design pressure**: Difficulty mocking often indicates tight coupling

**The mocking spectrum:**
```
Never mock ←────────────────────────→ Always mock
   |                                        |
DTOs                           External services
Value objects                  Current time
Domain models                  Random generators
Business logic                 File system
                               Database queries
```

**Critical mocking decisions:**
- **Mock at architectural boundaries**: Where code meets the outside world
- **Don't mock what you own**: If you mock your own classes extensively, you're testing mocks, not code
- **Consider test doubles hierarchy**: Dummy → Stub → Spy → Mock → Fake
- **Beware over-mocking**: Tests that only verify mock interactions provide false confidence

### Test Isolation - Beyond the Basics

**Isolation isn't just about independent tests:**

1. **Temporal isolation**: tests shouldn't depend on when they run
   - System clock dependencies
   - Timezone assumptions
   - Date-based business logic

2. **Data isolation**: tests shouldn't share mutable state
   - Class-level variables
   - Module-level caches
   - Database records
   - File system artifacts

3. **Execution order isolation**: test suite should pass regardless of execution order
   - No test should require another test to run first
   - Random test execution order can reveal hidden dependencies

4. **Environmental isolation**: tests should work on any machine
   - No hardcoded paths
   - No assumptions about installed software
   - No dependencies on specific OS behaviors

**The hidden dependencies that break isolation:**
- **Singleton patterns**: Global state in disguise
- **Class variables in Python**: Shared across all instances
- **Default mutable arguments**: The classic `def func(items=[])`
- **Import-time code execution**: Code that runs when module loads
- **Thread-local storage**: Can leak between tests in same thread

### Advanced concepts

**Test Doubles and Their Purposes:**

- **Dummy**: Passed around but never used (parameter fillers)
- **Stub**: Provides canned answers to calls
- **Spy**: Records information about how it was called
- **Mock**: Pre-programmed with expectations that form a specification
- **Fake**: Working implementation but simplified (in-memory database)

**The Testing Pyramid vs Testing Trophy:**
```
Testing pyramid:          Testing trophy:
    /\                        ____
   /E2E\                     /    \
  /------\                  /  E2E  \
 /Integr. \                /----------\
/-----------\             / Integration \
/ Unit Tests \           /----------------\
                        /   Unit Tests     \
```

The trophy emphasizes more integration tests because:
- Modern frameworks handle many unit-level concerns
- Integration tests catch more realistic bugs
- The cost of integration tests has decreased with better tools

**Property-based testing philosophy:**
Instead of thinking of specific examples, define properties that should always hold:
- Invariants: "The sum of parts equals the whole"
- Idempotence: "Doing it twice is the same as doing it once"
- Round-trip: "Encoding then decoding returns the original"
- Commutativity: "Order doesn't matter for this operation"

### Testing anti-patterns to avoid

**Test-induced design damage**: when you compromise your design just to make it "testable"
- Making everything public
- Adding test-only parameters
- Breaking encapsulation to verify state

**The mockist vs classicist**:
- **Mockist**: Mock all dependencies, test in complete isolation
- **Classicist**: Use real objects where possible, mock only at boundaries
- **In reality**: Use judgment based on the situation

**False confidence anti-patterns**:
- **Testing implementation details**: tests break with every refactor
- **Excessive mocking**: testing mock configuration instead of real behavior
- **Meaningless assertions**: `assert result is not None` tells you nothing
- **Test-after development**: missing the design feedback loop

### Psychological aspects of unit testing

**The testing mindset shift**:
- From "Does my code work?" to "How can my code break?"
- From "Testing slows me down" to "Testing speeds up my debugging"
- From "I'll test it later" to "I can't code without tests"

**Test-Driven Development as design tool**:
- Forces you to think about API before implementation
- Makes you consider error cases upfront
- Encourages smaller, focused functions
- Provides immediate feedback on design decisions

**The Confidence Gradient**:
```
No tests → Some tests → Good coverage → Comprehensive tests → Over-testing
           ↑                              ↑                    ↑
    Anxiety about changes         Sweet spot of confidence    Diminishing returns
```

### Measuring test quality (beyond coverage)

**Mutation testing**: introduce bugs and see if tests catch them
**Test effectiveness**: how many real bugs do tests prevent?
**Test maintainability**: how often do tests need updating?
**Test clarity**: can a new developer understand what's being tested?
**Test speed**: do tests run fast enough to be run frequently?
