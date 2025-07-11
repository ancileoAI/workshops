# Python Protocols: Structural Subtyping

## Protocol-Thinking: Python's Foundation

**Most Python stdlib and frameworks use Protocol-thinking even before formal Protocol existed!**

Python has always been built around implicit protocols - informal interfaces defined by behavior rather than inheritance:

```python
# The Iterator Protocol (pre-dating typing.Protocol)
class NumberGenerator:
    def __init__(self, max_num):
        self.max_num = max_num
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.max_num:
            self.current += 1
            return self.current
        raise StopIteration

# Works with for loops, list(), etc. - no inheritance needed!
for num in NumberGenerator(3):
    print(num)  # 1, 2, 3

# Context Manager Protocol
class DatabaseConnection:
    def __enter__(self):
        print("Connecting to database...")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection...")

# Works with 'with' statement automatically
with DatabaseConnection() as db:
    print("Using database")
```

**Framework Examples of Protocol-Thinking:**
- **Django**: `save()`, `delete()`, `clean()` methods expected on models
- **Flask**: WSGI callable - any callable that accepts `(environ, start_response)`
- **Requests**: File-like objects for uploads - anything with `.read()`
- **asyncio**: Awaitable objects - anything with `__await__()` method

The `typing.Protocol` just formalized what Python always did naturally!

## The Problem: Duck Typing vs Type Hints

Python's duck typing is powerful but creates challenges when adding type hints:

```python
# This works at runtime (duck typing)
def make_it_quack(animal):
    return animal.quack()

class Duck:
    def quack(self):
        return "Quack!"

class Penguing:
    def quack(self):
        return "Pretending to be a duck!"

make_it_quack(Duck())    # Works
make_it_quack(Penguin())  # Also works

# But how do we add type hints?
def make_it_quack(animal: "?") -> str:  # What type should animal be?
    return animal.quack()
```

**Traditional Solution: Inheritance**
```python
class QuackingThing:
    def quack(self):
        raise NotImplementedError

class Duck(QuackingThing):
    def quack(self):
        return "Quack!"

class Penguin(QuackingThing):  # Forced inheritance!
    def quack(self):
        return "Pretending to be a duck!"

def make_it_quack(animal: QuackingThing) -> str:
    return animal.quack()
```

**Problems with Inheritance Approach:**
- Forces artificial inheritance relationships
- Tightly couples unrelated classes
- Breaks the flexibility of duck typing
- Requires modifying existing classes

## Protocols: Structural Subtyping

Protocols solve this by checking structure, not inheritance:

```python
from typing import Protocol

class Quacker(Protocol):
    def quack(self) -> str:
        ...

# No inheritance needed!
class Duck:
    def quack(self) -> str:
        return "Quack!"

class Penguin:
    def quack(self) -> str:
        return "Pretending to be a duck!"

def make_it_quack(animal: Quacker) -> str:
    return animal.quack()

# Type checker is happy, no inheritance required
make_it_quack(Duck())    # ✓ Type checks
make_it_quack(Penguin())  # ✓ Type checks
```

## Protocols vs Abstract Base Classes: Side-by-Side

Let's compare both approaches for a file processing system:

### Abstract Base Class Approach

```python
from abc import ABC, abstractmethod
from typing import List

class FileProcessor(ABC):
    @abstractmethod
    def read_file(self, path: str) -> str:
        pass
    
    @abstractmethod
    def process_content(self, content: str) -> List[str]:
        pass
    
    @abstractmethod
    def write_output(self, data: List[str], output_path: str) -> None:
        pass

class CSVProcessor(FileProcessor):  # Must inherit
    def read_file(self, path: str) -> str:
        with open(path, 'r') as f:
            return f.read()
    
    def process_content(self, content: str) -> List[str]:
        lines = content.strip().split('\n')
        return [f"Processed: {line}" for line in lines]
    
    def write_output(self, data: List[str], output_path: str) -> None:
        with open(output_path, 'w') as f:
            f.write('\n'.join(data))

class JSONProcessor(FileProcessor):  # Must inherit
    def read_file(self, path: str) -> str:
        import json
        with open(path, 'r') as f:
            return json.load(f)
    
    def process_content(self, content: str) -> List[str]:
        # Process JSON differently
        return [f"JSON item: {item}" for item in content]
    
    def write_output(self, data: List[str], output_path: str) -> None:
        import json
        with open(output_path, 'w') as f:
            json.dump(data, f)

def process_file_abc(processor: FileProcessor, input_path: str, output_path: str):
    content = processor.read_file(input_path)
    processed = processor.process_content(content)
    processor.write_output(processed, output_path)
```

### Protocol Approach

```python
from typing import Protocol, List

class FileProcessor(Protocol):
    def read_file(self, path: str) -> str:
        ...
    
    def process_content(self, content: str) -> List[str]:
        ...
    
    def write_output(self, data: List[str], output_path: str) -> None:
        ...

# No inheritance required!
class CSVProcessor:
    def read_file(self, path: str) -> str:
        with open(path, 'r') as f:
            return f.read()
    
    def process_content(self, content: str) -> List[str]:
        lines = content.strip().split('\n')
        return [f"Processed: {line}" for line in lines]
    
    def write_output(self, data: List[str], output_path: str) -> None:
        with open(output_path, 'w') as f:
            f.write('\n'.join(data))

class JSONProcessor:
    def read_file(self, path: str) -> str:
        import json
        with open(path, 'r') as f:
            return json.load(f)
    
    def process_content(self, content: str) -> List[str]:
        return [f"JSON item: {item}" for item in content]
    
    def write_output(self, data: List[str], output_path: str) -> None:
        import json
        with open(output_path, 'w') as f:
            json.dump(data, f)

# Works with any class that has the right methods
class DatabaseProcessor:  # Completely independent class
    def __init__(self, db_connection):
        self.db = db_connection
    
    def read_file(self, path: str) -> str:
        # Read from database instead of file
        return self.db.query(f"SELECT data FROM files WHERE path='{path}'")
    
    def process_content(self, content: str) -> List[str]:
        return content.split(',')
    
    def write_output(self, data: List[str], output_path: str) -> None:
        self.db.execute(f"INSERT INTO results VALUES ('{output_path}', '{data}')")

def process_file_protocol(processor: FileProcessor, input_path: str, output_path: str):
    content = processor.read_file(input_path)
    processed = processor.process_content(content)
    processor.write_output(processed, output_path)

# All work without any inheritance!
csv_proc = CSVProcessor()
json_proc = JSONProcessor()
db_proc = DatabaseProcessor(db_connection)

process_file_protocol(csv_proc, "data.csv", "output.csv")
process_file_protocol(json_proc, "data.json", "output.json")
process_file_protocol(db_proc, "table_data", "results")
```

## Decision Matrix: When to Use What?

| Scenario | Use Protocol | Use ABC | Reasoning |
|----------|-------------|---------|-----------|
| **Third-party classes** | ✅ | ❌ | Can't modify inheritance |
| **Multiple inheritance concerns** | ✅ | ⚠️ | Protocols avoid diamond problem |
| **Duck typing compatibility** | ✅ | ❌ | Maintains Python's flexibility |
| **Runtime type checking needed** | ⚠️ | ✅ | ABC has built-in isinstance support |
| **Shared implementation** | ❌ | ✅ | ABC can provide concrete methods |
| **Strict interface enforcement** | ❌ | ✅ | ABC prevents instantiation |
| **Framework/library design** | ✅ | ✅ | Both work, choose based on use case |
| **Legacy codebase integration** | ✅ | ❌ | No need to refactor existing classes |

## Protocol Features

### Runtime Checkable Protocols

**What `@runtime_checkable` Does:**
The decorator enables `isinstance()` and `issubclass()` checks on protocols by inspecting the object's structure at runtime.

**Performance Note:** Runtime checking has overhead - use sparingly in performance-critical code.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None:
        ...

class Circle:
    def draw(self) -> None:
        print("Drawing a circle")

class Square:
    def draw(self) -> None:
        print("Drawing a square")

class NotDrawable:
    def paint(self) -> None:
        print("Painting something")

# Runtime checking
circle = Circle()
square = Square()
other = NotDrawable()

print(isinstance(circle, Drawable))  # True
print(isinstance(square, Drawable))  # True
print(isinstance(other, Drawable))   # False

def draw_if_possible(obj):
    if isinstance(obj, Drawable):
        obj.draw()
    else:
        print("Object cannot be drawn")

# When NOT to use @runtime_checkable:
# - High-performance code (checking overhead)
# - Static typing is sufficient
# - Simple function signatures

# When TO use @runtime_checkable:
# - Dynamic dispatch needed
# - Working with user plugins
# - Defensive programming at API boundaries
```

### Generic Protocols

```python
from typing import Protocol, TypeVar, Generic

T = TypeVar('T')

class Comparable(Protocol[T]):
    def __lt__(self, other: T) -> bool:
        ...
    
    def __eq__(self, other: T) -> bool:
        ...

def sort_items(items: list[Comparable[T]]) -> list[T]:
    return sorted(items)

# Works with any comparable type
numbers = [3, 1, 4, 1, 5]
words = ["banana", "apple", "cherry"]

sorted_numbers = sort_items(numbers)  # list[int]
sorted_words = sort_items(words)      # list[str]
```

### Protocol Inheritance

```python
from typing import Protocol

class Readable(Protocol):
    def read(self) -> str:
        ...

class Writable(Protocol):
    def write(self, data: str) -> None:
        ...

class ReadWritable(Readable, Writable, Protocol):
    """A protocol that combines reading and writing"""
    pass

class File:
    def __init__(self, filename: str):
        self.filename = filename
    
    def read(self) -> str:
        with open(self.filename, 'r') as f:
            return f.read()
    
    def write(self, data: str) -> None:
        with open(self.filename, 'w') as f:
            f.write(data)

def backup_data(source: Readable, target: Writable) -> None:
    data = source.read()
    target.write(data)

def sync_files(file1: ReadWritable, file2: ReadWritable) -> None:
    # Can read from and write to both files
    data1 = file1.read()
    data2 = file2.read()
    file1.write(data2)
    file2.write(data1)
```

## Protocols vs Duck Typing: Best of Both Worlds

```python
from typing import Protocol, Union

class Emailer(Protocol):
    def send_email(self, to: str, subject: str, body: str) -> bool:
        ...

# Multiple implementations without inheritance
class SMTPEmailer:
    def send_email(self, to: str, subject: str, body: str) -> bool:
        print(f"Sending via SMTP to {to}: {subject}")
        return True

class SendGridEmailer:
    def send_email(self, to: str, subject: str, body: str) -> bool:
        print(f"Sending via SendGrid to {to}: {subject}")
        return True

class MockEmailer:
    def send_email(self, to: str, subject: str, body: str) -> bool:
        print(f"Mock email to {to}: {subject}")
        return True

# Type-safe duck typing
def notify_user(emailer: Emailer, user_email: str, message: str) -> None:
    success = emailer.send_email(
        to=user_email,
        subject="Notification",
        body=message
    )
    if success:
        print("Notification sent successfully")

# All work seamlessly
emailers = [SMTPEmailer(), SendGridEmailer(), MockEmailer()]
for emailer in emailers:
    notify_user(emailer, "user@example.com", "Hello!")
```

## Protocol Variance: Covariance and Contravariance

Variance controls how protocol inheritance behaves with type parameters - a crucial concept for type safety:

```python
from typing import Protocol, TypeVar

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)        # Covariant
T_contra = TypeVar('T_contra', contravariant=True)  # Contravariant

class Producer(Protocol[T_co]):
    """Covariant: can return more specific types"""
    def produce(self) -> T_co: ...

class Consumer(Protocol[T_contra]):
    """Contravariant: can accept more general types"""  
    def consume(self, item: T_contra) -> None: ...

class Processor(Protocol[T]):
    """Invariant: must match exactly"""
    def process(self, item: T) -> T: ...
```

**Covariance Example:**
```python
class Animal: 
    def speak(self): return "Some sound"

class Dog(Animal): 
    def speak(self): return "Woof"

class DogProducer:
    def produce(self) -> Dog:
        return Dog()

class AnimalProducer:
    def produce(self) -> Animal:
        return Animal()

# This works: DogProducer can substitute Producer[Animal]
# because Dog IS-A Animal (more specific → more general)
animal_producer: Producer[Animal] = DogProducer()
animal = animal_producer.produce()  # Returns Dog, but that's fine as Animal
```

**Contravariance Example:**
```python
class AnimalHandler:
    def consume(self, animal: Animal) -> None:
        print(f"Handling: {animal.speak()}")

class DogHandler:
    def consume(self, dog: Dog) -> None:
        print(f"Dog handling: {dog.speak()}")

# This works: AnimalHandler can substitute Consumer[Dog]
# because it can handle ANY Animal (including Dogs)
dog_consumer: Consumer[Dog] = AnimalHandler()
dog_consumer.consume(Dog())  # AnimalHandler accepts Dog just fine

# This would NOT work:
# animal_consumer: Consumer[Animal] = DogHandler()  # Type error!
# animal_consumer.consume(Animal())  # DogHandler can't handle generic Animals
```

**Key Intuition:**
- **Covariance** (return types): "You can return something more specific than promised"
- **Contravariance** (parameter types): "You can accept something more general than required"
- **Invariance**: "Must match exactly"

**Real-World Example:**
```python
# Event system with variance
class Event: pass
class ClickEvent(Event): pass
class KeyEvent(Event): pass

# Covariant: Event producers
class EventSource(Protocol[T_co]):
    def get_next_event(self) -> T_co: ...

class MouseSource:
    def get_next_event(self) -> ClickEvent: ...

class KeyboardSource:  
    def get_next_event(self) -> KeyEvent: ...

# Both can be used as EventSource[Event]
mouse: EventSource[Event] = MouseSource()    # ClickEvent is Event
keyboard: EventSource[Event] = KeyboardSource()  # KeyEvent is Event

# Contravariant: Event handlers  
class EventHandler(Protocol[T_contra]):
    def handle(self, event: T_contra) -> None: ...

class GeneralHandler:
    def handle(self, event: Event) -> None:
        print("Handling any event")

class ClickHandler:
    def handle(self, event: ClickEvent) -> None:
        print("Handling click")

# GeneralHandler can handle specific events
click_handler: EventHandler[ClickEvent] = GeneralHandler()  # Can handle any Event
click_handler.handle(ClickEvent())  # Works fine

# But not the reverse:
# general_handler: EventHandler[Event] = ClickHandler()  # Type error!
# general_handler.handle(KeyEvent())  # ClickHandler can't handle KeyEvent
```

## Common pitfalls and solutions

### Pitfall 1: Accidental Protocol Satisfaction

```python
class Message(Protocol):
    def encode(self) -> bytes:
        ...

def send_message(msg: Message) -> None:
    data = msg.encode()
    print(f"Sending: {data}")

# Problem: str accidentally satisfies the protocol!
send_message("Hello World")  # Works but possibly wrong

# Solution: Be more specific
class NetworkMessage(Protocol):
    def encode(self) -> bytes:
        ...
    
    def get_headers(self) -> dict[str, str]:
        ...
    
    def get_destination(self) -> str:
        ...
```

### Pitfall 2: Protocol vs Implementation Confusion

```python
# Don't do this - mixing protocol and implementation
class BadFileHandler(Protocol):
    def read_file(self, path: str) -> str:
        # Don't put implementation in protocols!
        with open(path, 'r') as f:
            return f.read()

# Do this instead - pure protocol
class FileHandler(Protocol):
    def read_file(self, path: str) -> str:
        ...

# Separate implementation
class TextFileHandler:
    def read_file(self, path: str) -> str:
        with open(path, 'r') as f:
            return f.read()
```

## Discussion Questions

1. **Flexibility vs Safety**: Protocols provide more flexibility but less runtime safety than ABCs. In what scenarios would you prefer each approach?
2. **Migration Strategy**: You have an existing codebase using ABCs. How would you gradually migrate to protocols? What would be your migration criteria?
3. **Testing Strategy**: How would you test code that uses protocols? What are the testing advantages and challenges compared to ABC-based code?

*Protocols are about capabilities, not relationships. If it walks like a duck and quacks like a duck, it satisfies the Duck protocol - no inheritance required!*
