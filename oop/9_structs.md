# Structs vs Classes

## Understanding the Spectrum

Different programming languages offer various approaches to organizing data and behavior. Understanding when to use simple data structures versus full object-oriented classes is crucial for writing maintainable, performant code.

### The Data Structure Spectrum

```
Simple Data → Rich Data → Behavior + Data → Complex Objects
    |            |           |                |
  Tuples      Dataclasses   Classes        Frameworks
 NamedTuple   Struct-like   Methods       Complex OOP
```

## What Are Structs?

### Structs in Different Languages

**C Struct:**
```c
// Pure data container
struct Point {
    int x;
    int y;
};

struct Point p = {10, 20};
```

**Rust Struct:**
```rust
// Data with associated methods
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
    
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}
```

**Go Struct:**
```go
// Data with methods
type Person struct {
    Name string
    Age  int
}

func (p Person) Greet() string {
    return fmt.Sprintf("Hello, I'm %s", p.Name)
}
```

### Key Characteristics of Structs

1. **Data-focused**: Primary purpose is to group related data
2. **Value semantics**: Often copied rather than referenced
3. **Simple**: Minimal complexity, easy to understand
4. **Performance**: Usually more memory-efficient than classes
5. **Immutability**: Often immutable or encourage immutable patterns

## Python's Struct-Like Options

### 1. Named Tuples

```python
from typing import NamedTuple

# Immutable, memory-efficient
class Point(NamedTuple):
    x: int
    y: int
    
    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

# Usage
p1 = Point(3, 4)
p2 = Point(0, 0)

print(p1.distance_from_origin())  # 5.0
print(p1.x, p1.y)  # 3 4

# Immutable
# p1.x = 5  # AttributeError: can't set attribute

# Memory efficient
import sys
print(f"Point size: {sys.getsizeof(p1)} bytes")

# Tuple unpacking works
x, y = p1
print(f"Coordinates: ({x}, {y})")
```

### 2. Data Classes

```python
from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class Person:
    """Mutable data container with automatic methods"""
    name: str
    age: int
    email: str = ""
    friends: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_friend(self, friend: str) -> None:
        self.friends.append(friend)
    
    def is_adult(self) -> bool:
        return self.age >= 18

# Automatic __init__, __repr__, __eq__
person = Person("Alice", 30, "alice@example.com")
print(person)  # Person(name='Alice', age=30, email='alice@example.com', ...)

# Mutable by default
person.age = 31
person.add_friend("Bob")

# Comparison works automatically
person2 = Person("Alice", 31, "alice@example.com")
print(person == person2)  # False (different friends list)
```

### 3. Frozen Data Classes (Immutable)

```python
@dataclass(frozen=True)
class ImmutablePoint:
    """Immutable data class"""
    x: float
    y: float
    
    def translate(self, dx: float, dy: float) -> 'ImmutablePoint':
        """Return new point with translation applied"""
        return ImmutablePoint(self.x + dx, self.y + dy)
    
    def distance_to(self, other: 'ImmutablePoint') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

# Immutable operations
point = ImmutablePoint(1.0, 2.0)
new_point = point.translate(3.0, 4.0)

print(f"Original: {point}")    # ImmutablePoint(x=1.0, y=2.0)
print(f"Translated: {new_point}")  # ImmutablePoint(x=4.0, y=6.0)

# point.x = 5  # FrozenInstanceError: cannot assign to field 'x'

# Hashable (can be used in sets/dicts)
points = {point, new_point}
point_dict = {point: "origin", new_point: "moved"}
```

### 4. Pydantic Models (Validation + Structure)

```python
from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    """Data model with validation"""
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    email: str
    signup_date: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

# Automatic validation
try:
    user = User(name="Alice", age=30, email="alice@example.com")
    print(user.json())  # JSON serialization
except ValueError as e:
    print(f"Validation error: {e}")

# Invalid data raises validation errors
try:
    invalid_user = User(name="", age=-5, email="invalid")
except ValueError as e:
    print(f"Validation failed: {e}")
```

## When to Use What: Decision Framework

### Data Complexity Matrix

| Data Needs | Behavior Needs | Best Choice | Example Use Case |
|------------|----------------|-------------|------------------|
| **Simple** | **None** | `NamedTuple` | Coordinates, RGB colors |
| **Simple** | **Minimal** | `dataclass` | Configuration, DTOs |
| **Medium** | **Some** | `dataclass` + methods | User profiles, products |
| **Complex** | **Rich** | `class` | Business entities, services |
| **Validated** | **Any** | `Pydantic` | API models, config files |

### Performance Comparison

```python
import sys
import timeit
from dataclasses import dataclass
from typing import NamedTuple

# Different approaches for same data
class RegularClass:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

@dataclass
class DataClass:
    x: int
    y: int
    z: int

class TupleClass(NamedTuple):
    x: int
    y: int
    z: int

# Memory usage
regular = RegularClass(1, 2, 3)
data_obj = DataClass(1, 2, 3)
tuple_obj = TupleClass(1, 2, 3)

print("Memory Usage:")
print(f"Regular class: {sys.getsizeof(regular)} bytes")
print(f"Data class: {sys.getsizeof(data_obj)} bytes")
print(f"Named tuple: {sys.getsizeof(tuple_obj)} bytes")

# Creation performance
def time_creation():
    regular_time = timeit.timeit(
        lambda: RegularClass(1, 2, 3), 
        number=100000
    )
    
    data_time = timeit.timeit(
        lambda: DataClass(1, 2, 3), 
        number=100000
    )
    
    tuple_time = timeit.timeit(
        lambda: TupleClass(1, 2, 3), 
        number=100000
    )
    
    print("\nCreation Performance (100k instances):")
    print(f"Regular class: {regular_time:.4f}s")
    print(f"Data class: {data_time:.4f}s")
    print(f"Named tuple: {tuple_time:.4f}s")

time_creation()
```

## Practical Design Patterns

### 1. Progressive Enhancement Pattern

```python
# Start simple, enhance as needed

# Phase 1: Simple data container
@dataclass(frozen=True)
class SimpleUser:
    name: str
    email: str

# Phase 2: Add validation
@dataclass(frozen=True)
class ValidatedUser:
    name: str
    email: str
    
    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        if '@' not in self.email:
            raise ValueError("Invalid email")

# Phase 3: Add behavior
@dataclass(frozen=True)
class EnhancedUser:
    name: str
    email: str
    role: str = "user"
    
    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        if '@' not in self.email:
            raise ValueError("Invalid email")
    
    def display_name(self) -> str:
        return self.name.title()
    
    def is_admin(self) -> bool:
        return self.role == "admin"
    
    def to_dict(self) -> dict:
        return {"name": self.name, "email": self.email, "role": self.role}

# Phase 4: Full class when complexity demands it
class ComplexUser:
    def __init__(self, name: str, email: str, role: str = "user"):
        self._validate_input(name, email)
        self._name = name.strip()
        self._email = email.lower()
        self._role = role
        self._permissions = self._load_permissions()
        self._audit_log = []
    
    def _validate_input(self, name: str, email: str):
        # Complex validation logic
        pass
    
    def _load_permissions(self) -> set:
        # Load permissions based on role
        return set()
    
    # Rich behavior with state management
    def update_role(self, new_role: str):
        old_role = self._role
        self._role = new_role
        self._permissions = self._load_permissions()
        self._audit_log.append(f"Role changed from {old_role} to {new_role}")
    
    # Properties for controlled access
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
```

### 2. Value Objects Pattern

```python
from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class Money:
    """Value object for monetary amounts"""
    amount: int  # Store in cents to avoid floating point issues
    currency: str = "USD"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if len(self.currency) != 3:
            raise ValueError("Currency must be 3 characters")
    
    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __mul__(self, factor: Union[int, float]) -> 'Money':
        return Money(int(self.amount * factor), self.currency)
    
    def to_decimal(self) -> float:
        return self.amount / 100
    
    def __str__(self) -> str:
        return f"{self.to_decimal():.2f} {self.currency}"

@dataclass(frozen=True)
class Color:
    """Value object for colors"""
    red: int
    green: int
    blue: int
    
    def __post_init__(self):
        for component in [self.red, self.green, self.blue]:
            if not 0 <= component <= 255:
                raise ValueError("Color components must be 0-255")
    
    def to_hex(self) -> str:
        return f"#{self.red:02x}{self.green:02x}{self.blue:02x}"
    
    def brightness(self) -> float:
        return (self.red + self.green + self.blue) / (3 * 255)
    
    def is_dark(self) -> bool:
        return self.brightness() < 0.5

# Usage
price = Money(2550, "USD")  # $25.50
tax = Money(255, "USD")     # $2.55
total = price + tax         # $28.05

color = Color(255, 0, 0)    # Red
print(color.to_hex())       # #ff0000
print(color.is_dark())      # False
```

### 3. Configuration Objects Pattern

```python
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import json
from pathlib import Path

@dataclass
class DatabaseConfig:
    """Database configuration"""
    host: str = "localhost"
    port: int = 5432
    database: str = "myapp"
    username: str = "user"
    password: str = ""
    pool_size: int = 10
    
    def connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

@dataclass
class CacheConfig:
    """Cache configuration"""
    enabled: bool = True
    ttl_seconds: int = 3600
    max_size: int = 1000
    redis_url: Optional[str] = None

@dataclass
class AppConfig:
    """Main application configuration"""
    debug: bool = False
    secret_key: str = "change-me"
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    feature_flags: Dict[str, bool] = field(default_factory=dict)
    
    @classmethod
    def from_file(cls, config_path: Path) -> 'AppConfig':
        """Load configuration from JSON file"""
        with open(config_path) as f:
            data = json.load(f)
        
        # Handle nested configurations
        db_data = data.pop('database', {})
        cache_data = data.pop('cache', {})
        
        return cls(
            database=DatabaseConfig(**db_data),
            cache=CacheConfig(**cache_data),
            **data
        )
    
    def to_file(self, config_path: Path) -> None:
        """Save configuration to JSON file"""
        # Convert to dict for JSON serialization
        config_dict = {
            'debug': self.debug,
            'secret_key': self.secret_key,
            'database': {
                'host': self.database.host,
                'port': self.database.port,
                'database': self.database.database,
                'username': self.database.username,
                'password': self.database.password,
                'pool_size': self.database.pool_size,
            },
            'cache': {
                'enabled': self.cache.enabled,
                'ttl_seconds': self.cache.ttl_seconds,
                'max_size': self.cache.max_size,
                'redis_url': self.cache.redis_url,
            },
            'feature_flags': self.feature_flags
        }
        
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)

# Usage
config = AppConfig(
    debug=True,
    database=DatabaseConfig(host="prod-db", database="myapp_prod"),
    feature_flags={"new_ui": True, "beta_feature": False}
)

print(config.database.connection_string())
```

## Real-World Design Decisions

### 1. API Response Models

```python
# Bad: Over-engineered for simple data transfer
class BadApiResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self._status_code = status_code
        self._headers = {}
        self._meta = {}
    
    def add_header(self, key, value):
        self._headers[key] = value
    
    def set_meta(self, key, value):
        self._meta[key] = value
    
    def to_dict(self):
        return {
            "data": self._data,
            "status": self._status_code,
            "headers": self._headers,
            "meta": self._meta
        }

# Good: Simple data container for DTOs
@dataclass
class ApiResponse:
    """Data transfer object for API responses"""
    data: Any
    status_code: int = 200
    message: str = ""
    
    def to_dict(self) -> dict:
        return {
            "data": self.data,
            "status": self.status_code,
            "message": self.message
        }

@dataclass
class UserResponse:
    """Specific response type with validation"""
    id: int
    name: str
    email: str
    is_active: bool = True
    
    @classmethod
    def from_user_model(cls, user_model) -> 'UserResponse':
        """Convert from complex user model to simple response"""
        return cls(
            id=user_model.id,
            name=user_model.display_name,
            email=user_model.email,
            is_active=user_model.is_active
        )
```

### 2. Event Data Structures

```python
from datetime import datetime
from enum import Enum
from uuid import uuid4, UUID

class EventType(Enum):
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    ORDER_PLACED = "order_placed"
    PAYMENT_PROCESSED = "payment_processed"

# Simple event structure using dataclass
@dataclass(frozen=True)
class Event:
    """Immutable event for event sourcing"""
    id: UUID = field(default_factory=uuid4)
    event_type: EventType = field()
    aggregate_id: str = field()
    data: Dict[str, Any] = field()
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: int = 1
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "event_type": self.event_type.value,
            "aggregate_id": self.aggregate_id,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        return cls(
            id=UUID(data["id"]),
            event_type=EventType(data["event_type"]),
            aggregate_id=data["aggregate_id"],
            data=data["data"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            version=data["version"]
        )

# Usage for event sourcing
user_created_event = Event(
    event_type=EventType.USER_CREATED,
    aggregate_id="user_123",
    data={"name": "Alice", "email": "alice@example.com"}
)

# Serialization for storage
event_json = json.dumps(user_created_event.to_dict())
restored_event = Event.from_dict(json.loads(event_json))
```

### 3. Game Development Entities

```python
# Simple struct-like entities for performance
@dataclass
class Position:
    x: float
    y: float
    
    def distance_to(self, other: 'Position') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

@dataclass
class Velocity:
    dx: float
    dy: float
    
    def magnitude(self) -> float:
        return (self.dx ** 2 + self.dy ** 2) ** 0.5

@dataclass
class GameEntity:
    """Simple entity for game objects"""
    entity_id: int
    position: Position
    velocity: Velocity
    health: int = 100
    is_active: bool = True
    
    def update(self, delta_time: float) -> None:
        """Update entity position based on velocity"""
        if self.is_active:
            self.position.x += self.velocity.dx * delta_time
            self.position.y += self.velocity.dy * delta_time
    
    def take_damage(self, damage: int) -> None:
        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.is_active = False

# For complex game logic, use full classes
class Player:
    """Complex player with rich behavior"""
    
    def __init__(self, entity: GameEntity, name: str):
        self.entity = entity
        self.name = name
        self.inventory = {}
        self.skills = {}
        self.quest_log = []
    
    def move(self, direction: str, speed: float) -> None:
        # Complex movement logic
        direction_map = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        
        if direction in direction_map:
            dx, dy = direction_map[direction]
            self.entity.velocity.dx = dx * speed
            self.entity.velocity.dy = dy * speed
    
    def use_item(self, item_name: str) -> bool:
        # Complex item usage logic
        if item_name in self.inventory:
            # Use item logic here
            return True
        return False
```

## Cross-Language Insights

### Rust's Approach: Structs + Traits

```rust
// Rust separates data (structs) from behavior (traits)
struct User {
    name: String,
    email: String,
    age: u32,
}

trait Validator {
    fn is_valid(&self) -> bool;
}

trait Serializable {
    fn to_json(&self) -> String;
}

impl Validator for User {
    fn is_valid(&self) -> bool {
        !self.name.is_empty() && self.email.contains('@')
    }
}

impl Serializable for User {
    fn to_json(&self) -> String {
        format!("{{\"name\":\"{}\",\"email\":\"{}\",\"age\":{}}}", 
                self.name, self.email, self.age)
    }
}
```

**Python Equivalent using Protocols:**

```python
from typing import Protocol

class Validator(Protocol):
    def is_valid(self) -> bool: ...

class Serializable(Protocol):
    def to_json(self) -> str: ...

@dataclass
class User:
    name: str
    email: str
    age: int
    
    def is_valid(self) -> bool:
        return bool(self.name.strip()) and '@' in self.email
    
    def to_json(self) -> str:
        import json
        return json.dumps({"name": self.name, "email": self.email, "age": self.age})

# Works with protocols without inheritance
def validate_and_serialize(obj: Validator & Serializable) -> str:
    if obj.is_valid():
        return obj.to_json()
    raise ValueError("Invalid object")
```

### Go's Composition Over Inheritance

```go
// Go uses struct embedding for composition
type User struct {
    Name  string
    Email string
}

type Employee struct {
    User          // Embedded struct
    EmployeeID   int
    Department   string
}

type Manager struct {
    Employee      // Embedded struct
    TeamSize     int
}
```

**Python Equivalent:**

```python
@dataclass
class User:
    name: str
    email: str

@dataclass
class Employee:
    user: User  # Composition instead of inheritance
    employee_id: int
    department: str
    
    # Delegate to user when needed
    @property
    def name(self) -> str:
        return self.user.name
    
    @property
    def email(self) -> str:
        return self.user.email

@dataclass
class Manager:
    employee: Employee  # Composition
    team_size: int
    
    # Can access nested data
    @property
    def name(self) -> str:
        return self.employee.user.name
```

## Decision Guidelines

### Choose NamedTuple When:
- Data is truly immutable
- Memory efficiency is critical
- You need tuple-like behavior (unpacking, indexing)
- Simple data containers without methods

### Choose Dataclass When:
- You need automatic `__init__`, `__repr__`, `__eq__`
- Data might need to be mutable
- You want to add methods for data processing
- Configuration objects, DTOs, simple entities

### Choose Regular Class When:
- Complex initialization logic needed
- Rich behavior and state management
- Need inheritance hierarchies
- Complex property management with getters/setters
- Integration with frameworks that expect classes

### Choose Pydantic When:
- Data validation is critical
- API request/response models
- Configuration with complex validation rules
- JSON serialization/deserialization needed

## Performance Implications

### Memory Layout

```python
import sys
from dataclasses import dataclass
from typing import NamedTuple

# Compare memory usage
class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

@dataclass
class DataPoint:
    x: int
    y: int

class TuplePoint(NamedTuple):
    x: int
    y: int

# Create instances
regular = RegularPoint(1, 2)
data_point = DataPoint(1, 2)
tuple_point = TuplePoint(1, 2)

print("Memory usage comparison:")
print(f"Regular class: {sys.getsizeof(regular)} + {sys.getsizeof(regular.__dict__)} = {sys.getsizeof(regular) + sys.getsizeof(regular.__dict__)} bytes")
print(f"Dataclass: {sys.getsizeof(data_point)} + {sys.getsizeof(data_point.__dict__)} = {sys.getsizeof(data_point) + sys.getsizeof(data_point.__dict__)} bytes")
print(f"NamedTuple: {sys.getsizeof(tuple_point)} bytes")

# Slots can reduce memory usage
@dataclass
class SlottedDataPoint:
    __slots__ = ['x', 'y']
    x: int
    y: int

slotted = SlottedDataPoint(1, 2)
print(f"Slotted dataclass: {sys.getsizeof(slotted)} bytes")
```

### Access Performance

```python
import timeit

# Access time comparison
def time_access():
    regular = RegularPoint(1, 2)
    data_point = DataPoint(1, 2)
    tuple_point = TuplePoint(1, 2)
    
    # Attribute access
    regular_time = timeit.timeit(lambda: regular.x + regular.y, number=1000000)
    data_time = timeit.timeit(lambda: data_point.x + data_point.y, number=1000000)
    tuple_time = timeit.timeit(lambda: tuple_point.x + tuple_point.y, number=1000000)
    
    print("\nAttribute access performance (1M operations):")
    print(f"Regular class: {regular_time:.4f}s")
    print(f"Dataclass: {data_time:.4f}s")
    print(f"NamedTuple: {tuple_time:.4f}s")

time_access()
```

## Key Takeaways

**Design Philosophy:**
- Start simple, add complexity only when needed
- Prefer immutable data structures when possible
- Use composition over inheritance for data structures
- Choose the right tool for the right job

**Performance Guidelines:**
- NamedTuple for immutable, memory-efficient data
- Dataclass for balanced flexibility and performance
- Regular classes for complex behavior
- Use `__slots__` when memory is critical

**Maintainability:**
- Struct-like patterns are easier to test
- Immutable data reduces bugs
- Clear separation of data and behavior
- Explicit is better than implicit

**Cross-Language Learning:**
- Rust's struct + traits model provides inspiration
- Go's composition patterns work well in Python
- C's simplicity has value for performance-critical code
- Functional programming concepts enhance struct-like patterns

*The best data structure is the simplest one that meets your needs. Don't over-engineer when a simple dataclass or NamedTuple will suffice.*
