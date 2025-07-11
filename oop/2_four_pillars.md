# Four Pillars of OOP

### 1. Encapsulation

**Definition**: Bundling data and methods that operate on that data within a single unit (class), while controlling access to internal implementation details.

### Python Implementation

```python
class BankAccount:
    def __init__(self, initial_balance=0):
        self._balance = initial_balance  # Protected
        self.__transaction_log = []      # Private (name mangling)
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self.__log_transaction("deposit", amount)
    
    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            self.__log_transaction("withdrawal", amount)
            return amount
        raise ValueError("Insufficient funds")
    
    def get_balance(self):
        return self._balance
    
    def __log_transaction(self, type, amount):
        self.__transaction_log.append(f"{type}: {amount}")
        print(f"{type}: {amount}")
    
    def fn():
        # Python automatically mangles __log_transaction to _BankAccount__log_transaction
        # This prevents accidental access from outside the class
        # You can still access it if you really want: obj._BankAccount__log_transaction()
        # But this breaks encapsulation and is not recommended
        pass

# Usage
account = BankAccount(1000)
account.deposit(500)
print(account.get_balance())  # 1500

# Direct access violations
# account._balance = 999999     # ?
# account.__transaction_log     # ? 
```

### Access Control Levels
- **Public**: `self.attribute` - accessible everywhere
- **Protected**: `self._attribute` - convention for internal use
- **Private**: `self.__attribute` - name mangling prevents access

### 2. Abstraction

**Definition**: Hiding implementation complexity while exposing only necessary interfaces for interaction.

### Interfaces and Abstract Classes

An interface defines a contract - a set of method signatures that implementing classes must provide, without specifying how these methods work.

```
// Pseudocode
interface Drawable {
    method draw()
    method getColor()
    method setColor(color)
}

// Any class implementing Drawable MUST provide these methods
class Circle implements Drawable {
    method draw() { /* circle-specific drawing */ }
    method getColor() { /* return circle color */ }
    method setColor(color) { /* set circle color */ }
}
```

**Python's Abstract Base Classes (ABCs)**

```python
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    def description(self) -> str:
        return f"A {self.__class__.__name__} with area {self.area():.2f}"

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

# Abstract class cannot be instantiated
# shape = Shape()  # TypeError

# But concrete implementations work
circle = Circle(5)
rectangle = Rectangle(4, 6)

shapes = [circle, rectangle]
for shape in shapes:
    print(shape.description())  # Polymorphism
```

**Interface Comparison: Python vs Statically Typed Languages**

| Aspect | Java/C# | Python |
|--------|---------|---------|
| **Interface Definition** | `interface Drawable { ... }` | `class Shape(ABC): @abstractmethod ...` |
| **Enforcement** | Compile-time error if not implemented | Runtime error when instantiated |
| **Multiple Interfaces** | `class Circle implements Drawable, Serializable` | `class Circle(Shape, Serializable):` (multiple inheritance) |
| **Duck Typing** | Not supported - explicit interface required | Supported - if it has the methods, it works |
| **Type Checking** | Compile-time guarantee | Runtime discovery (or static analysis with mypy) |
| **Flexibility** | Rigid - must declare interface implementation | Flexible - can work with any object with matching methods |

**Important Note: Interfaces/Abstract Classes ≠ Inheritance**

Don't confuse interfaces and abstract classes with inheritance:

- **Interfaces/Abstract Classes**: Define contracts (what methods must exist) - about **capability**
- **Inheritance**: Shares code and creates "is-a" relationships - about **implementation reuse**

```python
# Interface/Abstract Class: "What can you do?"
class Flyable(ABC):
    @abstractmethod
    def fly(self) -> None: pass

# Inheritance: "What are you?"
class Bird(Animal):  # Bird IS-A Animal
    def fly(self) -> None: pass

class Airplane(Vehicle, Flyable):  # Airplane IS-A Vehicle AND CAN fly
    def fly(self) -> None: pass
```

### 3. Inheritance

**Definition**: Mechanism allowing a class to inherit properties and behaviors from another class, enabling code reuse and extensibility.

```python

# Square inherits from Rectangle
class Square(Rectangle):
    def __init__(self, side: float):
        super().__init__(side, side)
    
    def __str__(self):
        return f"Square with side {self.width}"

class Ellipse(Shape):
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b
    
    def area(self) -> float:
        return math.pi * self.a * self.b
    
    def perimeter(self) -> float:
        return math.pi * (3 * (self.a + self.b) - math.sqrt((3 * self.a + self.b) * (self.a + 3 * self.b)))

# Usage
square = Square(4)        # Square inherits Rectangle's methods
ellipse = Ellipse(3, 2)   # Ellipse inherits Shape's description method

print(square.area())      # 16 (inherited from Rectangle)
print(square.perimeter()) # 16 (inherited from Rectangle)
print(ellipse.description()) # "An Ellipse with area 18.85" (inherited from Shape)
```

### Method Resolution Order (MRO)

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):  # Multiple inheritance
    pass

d = D()
print(d.method())  # Output: "B"
print(D.__mro__)   # (<class '__main__.D'>, <class '__main__.B'>, 
                   #  <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
```

### 4. Polymorphism

**Definition**: The ability to treat objects of different classes uniformly through a common interface, with method calls resolved at runtime.

### Runtime Polymorphism with Shapes

```python
# Polymorphic function - works with any Shape
def calculate_total_area(shapes: list[Shape]) -> float:
    total = 0
    for shape in shapes:
        total += shape.area()  # Polymorphism: area() method resolved at runtime
        print(f"{shape.__class__.__name__}: {shape.area():.2f}")
    return total

def print_shape_info(shapes: list[Shape]):
    for shape in shapes:
        # Each shape implements area() and perimeter() differently
        print(f"{shape.__class__.__name__}: Area={shape.area():.2f}, Perimeter={shape.perimeter():.2f}")

# Usage - same functions, different behaviors
shapes = [
    Circle(5),
    Rectangle(4, 6),
    Square(3),
    Ellipse(2, 4)
]

print("Individual areas:")
total_area = calculate_total_area(shapes)
print(f"Total area: {total_area:.2f}")

print("\nDetailed info:")
print_shape_info(shapes)
# Output shows polymorphism in action:
# Circle: Area=78.54, Perimeter=31.42
# Rectangle: Area=24.00, Perimeter=20.00  
# Square: Area=9.00, Perimeter=12.00
# Ellipse: Area=25.13, Perimeter=18.96
```

### Duck Typing (Python's Polymorphism)

```python
class FileWriter:
    def write(self, data: str):
        with open("output.txt", "w") as f:
            f.write(data)

class ConsoleWriter:
    def write(self, data: str):
        print(f"Console: {data}")

class NetworkWriter:
    def write(self, data: str):
        # Simulate network write
        print(f"Sending to network: {data}")

# Polymorphic usage - no inheritance
def save_data(writer, data: str):
    writer.write(data)  # Duck typing: if it has write(), it's a writer

# All work the same way
writers = [FileWriter(), ConsoleWriter(), NetworkWriter()]
for writer in writers:
    save_data(writer, "Hello, World!")
```

## Verification Questions

**Q1: Encapsulation**
Given this code, what will happen and why?
```python
class SecureData:
    def __init__(self):
        self.__secret = "classified"

data = SecureData()
print(data.__secret)  # What happens here?
```

**Q1: Abstraction**
Why might you choose an abstract base class over a regular class with placeholder methods that raise `NotImplementedError`?

**Q2: Inheritance**
In the Vehicle example, if both Car and Motorcycle had a `start_engine()` method, which one would be called and why?

**Q3: Polymorphism**
How does Python's duck typing differ from polymorphism in statically typed languages like Java or C#?


## Key Takeaway

These four pillars aren't just academic concepts - they're practical tools for managing code complexity. As we move into advanced topics, you'll see how modern Python builds upon these foundations while addressing their limitations.
