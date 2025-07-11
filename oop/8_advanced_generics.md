# Advanced Generics and Modern Python Features

## Understanding Generic Types

Generic types allow you to write flexible, reusable code while maintaining type safety. They enable you to create classes and functions that work with different types while preserving type information.

### Basic Generic Classes

```python
from typing import TypeVar, Generic, List, Optional

# Define a type variable
T = TypeVar('T')

class Stack(Generic[T]):
    """Generic stack implementation"""
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        if self._items:
            return self._items.pop()
        return None
    
    def peek(self) -> Optional[T]:
        if self._items:
            return self._items[-1]
        return None
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
    
    def size(self) -> int:
        return len(self._items)

# Usage with type safety
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
int_stack.push(3)

# Type checker knows this is Optional[int]
top_item = int_stack.pop()

string_stack: Stack[str] = Stack()
string_stack.push("hello")
string_stack.push("world")

# This would be a type error:
# int_stack.push("string")  # Type error!
```

### Bounded Type Variables

```python
from typing import TypeVar, Protocol, List, Generic
from abc import ABC, abstractmethod

# Bounded by a protocol
class Comparable(Protocol):
    def __lt__(self, other: 'Comparable') -> bool: ...
    def __gt__(self, other: 'Comparable') -> bool: ...
    def __eq__(self, other: 'Comparable') -> bool: ...

T_Comparable = TypeVar('T_Comparable', bound=Comparable)

class SortedList(Generic[T_Comparable]):
    """Generic sorted list that requires comparable items"""
    
    def __init__(self) -> None:
        self._items: List[T_Comparable] = []
    
    def add(self, item: T_Comparable) -> None:
        # Binary search insertion to maintain sort order
        left, right = 0, len(self._items)
        while left < right:
            mid = (left + right) // 2
            if self._items[mid] < item:
                left = mid + 1
            else:
                right = mid
        self._items.insert(left, item)
    
    def get_items(self) -> List[T_Comparable]:
        return self._items.copy()

# Works with built-in comparable types
sorted_ints = SortedList[int]()
sorted_ints.add(3)
sorted_ints.add(1)
sorted_ints.add(2)
print(sorted_ints.get_items())  # [1, 2, 3]

# Works with custom comparable types
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def __lt__(self, other: 'Person') -> bool:
        return self.age < other.age
    
    def __eq__(self, other: 'Person') -> bool:
        return self.age == other.age
    
    def __repr__(self) -> str:
        return f"Person({self.name}, {self.age})"

sorted_people = SortedList[Person]()
sorted_people.add(Person("Alice", 30))
sorted_people.add(Person("Bob", 25))
sorted_people.add(Person("Charlie", 35))
print(sorted_people.get_items())  # Sorted by age
```

### Multiple Type Variables

```python
from typing import TypeVar, Generic, Tuple, Dict, Callable

K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type
R = TypeVar('R')  # Result type

class Cache(Generic[K, V]):
    """Generic cache with key and value types"""
    
    def __init__(self, max_size: int = 100):
        self._cache: Dict[K, V] = {}
        self._access_order: List[K] = []
        self._max_size = max_size
    
    def get(self, key: K) -> Optional[V]:
        if key in self._cache:
            # Move to end (most recently used)
            self._access_order.remove(key)
            self._access_order.append(key)
            return self._cache[key]
        return None
    
    def put(self, key: K, value: V) -> None:
        if key in self._cache:
            # Update existing
            self._cache[key] = value
            self._access_order.remove(key)
            self._access_order.append(key)
        else:
            # Add new
            if len(self._cache) >= self._max_size:
                # Remove least recently used
                oldest_key = self._access_order.pop(0)
                del self._cache[oldest_key]
            
            self._cache[key] = value
            self._access_order.append(key)
    
    def transform_values(self, func: Callable[[V], R]) -> 'Cache[K, R]':
        """Transform all values using the provided function"""
        new_cache: Cache[K, R] = Cache(self._max_size)
        for key in self._access_order:
            old_value = self._cache[key]
            new_value = func(old_value)
            new_cache.put(key, new_value)
        return new_cache

# Usage
string_to_int_cache: Cache[str, int] = Cache()
string_to_int_cache.put("one", 1)
string_to_int_cache.put("two", 2)

# Transform to string cache
string_to_string_cache = string_to_int_cache.transform_values(str)
print(string_to_string_cache.get("one"))  # "1"
```

## Python 3.12+ Generic Syntax

Python 3.12 introduced a new, cleaner syntax for generics using square brackets:

### Old Syntax vs New Syntax

```python
# Python < 3.12 (still supported)
from typing import TypeVar, Generic

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class OldStack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)

class OldDict(Generic[K, V]):
    def __init__(self) -> None:
        self._data: dict[K, V] = {}

# Python 3.12+ syntax
class NewStack[T]:
    """Much cleaner syntax!"""
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)

class NewDict[K, V]:
    """Multiple type parameters"""
    def __init__(self) -> None:
        self._data: dict[K, V] = {}

# Bounded generics with new syntax
class SortedContainer[T: Comparable]:
    """Bounded type parameter"""
    def __init__(self) -> None:
        self._items: list[T] = []

# Function generics with new syntax
def swap[T](a: T, b: T) -> tuple[T, T]:
    """Generic function"""
    return b, a

def process_pair[T, U](first: T, second: U) -> tuple[U, T]:
    """Multiple type parameters in function"""
    return second, first
```

### Modern Generic Patterns

```python
# Generic factory pattern (Python 3.12+)
class Factory[T]:
    """Generic factory for creating objects"""
    
    def __init__(self, creator: Callable[..., T]):
        self._creator = creator
    
    def create(self, *args, **kwargs) -> T:
        return self._creator(*args, **kwargs)
    
    def create_batch(self, count: int, *args, **kwargs) -> list[T]:
        return [self.create(*args, **kwargs) for _ in range(count)]

# Usage
person_factory = Factory(Person)
people = person_factory.create_batch(3, "Unknown", 0)

# Generic builder pattern
class Builder[T]:
    """Generic builder pattern"""
    
    def __init__(self, target_type: type[T]):
        self._target_type = target_type
        self._attributes: dict[str, any] = {}
    
    def set(self, key: str, value: any) -> 'Builder[T]':
        self._attributes[key] = value
        return self
    
    def build(self) -> T:
        return self._target_type(**self._attributes)

# Usage
person = (Builder(Person)
          .set("name", "Alice")
          .set("age", 30)
          .build())
```

## Advanced Generic Concepts

### Covariance and Contravariance

see section `8.1_variance.md`

### Generic Protocols

```python
from typing import Protocol, TypeVar

T = TypeVar('T')

class Addable(Protocol[T]):
    """Protocol for types that can be added"""
    def __add__(self, other: T) -> T: ...

class Container(Protocol[T]):
    """Protocol for container types"""
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> T: ...

def sum_items[T: Addable[T]](items: Container[T]) -> T:
    """Sum items in a container of addable objects"""
    if len(items) == 0:
        raise ValueError("Cannot sum empty container")
    
    result = items[0]
    for i in range(1, len(items)):
        result = result + items[i]
    
    return result

# Works with different types
numbers = [1, 2, 3, 4, 5]
result = sum_items(numbers)  # 15

strings = ["Hello", " ", "World", "!"]
text = sum_items(strings)  # "Hello World!"
```

### Generic Decorators

```python
from typing import TypeVar, Callable, Any, ParamSpec
import functools
import time

# Python 3.10+ ParamSpec for better type hints with decorators
P = ParamSpec('P')
R = TypeVar('R')

def timed[P, R](func: Callable[P, R]) -> Callable[P, R]:
    """Generic timing decorator with proper type preservation"""
    
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    
    return wrapper

def retry[P, R](max_attempts: int = 3) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Generic retry decorator"""
    
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(0.1 * (2 ** attempt))  # Exponential backoff
            
            raise last_exception
        
        return wrapper
    return decorator

# Usage preserves exact type signatures
@timed
@retry(max_attempts=3)
def calculate_something(x: int, y: float) -> str:
    if x < 0:
        raise ValueError("x must be positive")
    return f"Result: {x * y}"

# Type checker knows the exact signature
result: str = calculate_something(5, 2.5)
```

## Practical Applications

### 1. Generic Repository Pattern

```python
from typing import TypeVar, Generic, Protocol, Optional, List
from abc import ABC, abstractmethod

# Entity protocol
class Entity(Protocol):
    id: int

T_Entity = TypeVar('T_Entity', bound=Entity)

class Repository(Generic[T_Entity], ABC):
    """Generic repository interface"""
    
    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Optional[T_Entity]:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[T_Entity]:
        pass
    
    @abstractmethod
    async def save(self, entity: T_Entity) -> T_Entity:
        pass
    
    @abstractmethod
    async def delete(self, entity_id: int) -> bool:
        pass

class InMemoryRepository(Repository[T_Entity]):
    """In-memory implementation of repository"""
    
    def __init__(self):
        self._data: Dict[int, T_Entity] = {}
        self._next_id = 1
    
    async def get_by_id(self, entity_id: int) -> Optional[T_Entity]:
        return self._data.get(entity_id)
    
    async def get_all(self) -> List[T_Entity]:
        return list(self._data.values())
    
    async def save(self, entity: T_Entity) -> T_Entity:
        if not hasattr(entity, 'id') or entity.id is None:
            entity.id = self._next_id
            self._next_id += 1
        
        self._data[entity.id] = entity
        return entity
    
    async def delete(self, entity_id: int) ->
