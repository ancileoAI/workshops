# Reflection and Introspection

## What is Reflection?
Reflection is the ability of a program to examine and modify its own structure and behavior at runtime. Python provides powerful introspection capabilities that allow you to inspect objects, classes, and modules dynamically.

**Introspection**: Examining objects at runtime (read-only)
**Reflection**: Examining AND modifying objects at runtime (read-write)

Python actually blurs this line - most "introspection" functions can also be used for modification.

## Basic Introspection Functions

### Core Functions

```python
class Person:
    species = "Homo sapiens"
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, I'm {self.name}"
    
    def _private_method(self):
        return "private method"

person = Person("Alice", 30)

# Basic type inspection
print(type(person))                    # <class '__main__.Person'>
print(isinstance(person, Person))      # True
print(issubclass(Person, object))      # True

# Check for attributes and methods
print(hasattr(person, 'name'))         # True
print(hasattr(person, 'fly'))          # False

# Get attribute values
print(getattr(person, 'name'))         # Alice
print(getattr(person, 'height', 'N/A')) # N/A (default value)

# Set attributes dynamically
setattr(person, 'height', 170)
print(person.height)                   # 170

# Delete attributes
delattr(person, 'height')
# print(person.height)                 # AttributeError
```

### Advanced Introspection

```python
# Get all attributes and methods
print(dir(person))
# ['__class__', '__delattr__', '__dict__', '__doc__', ...]

# Get object's dictionary
print(person.__dict__)
# {'name': 'Alice', 'age': 30}

# Get class dictionary
print(Person.__dict__)
# {'__module__': '__main__', 'species': 'Homo sapiens', ...}

# Check if something is callable
print(callable(person.greet))          # True
print(callable(person.name))           # False

# Get object ID and check identity
person2 = Person("Bob", 25)
print(id(person), id(person2))         # Different IDs
print(person is person2)               # False
```

## The `inspect` Module

The `inspect` module provides more extensive introspection capabilities:

```python
import inspect

class Calculator:
    """A simple calculator class"""
    
    def __init__(self, name="Default"):
        self.name = name
    
    def add(self, a: int, b: int) -> int:
        """Add two numbers"""
        return a + b
    
    def divide(self, a: float, b: float) -> float:
        """Divide two numbers"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    @property
    def description(self):
        return f"Calculator named {self.name}"
    
    @staticmethod
    def multiply(a, b):
        """Multiply two numbers"""
        return a * b
    
    @classmethod
    def create_scientific(cls):
        """Create a scientific calculator"""
        return cls("Scientific")

calc = Calculator("MyCalc")

# Inspect classes and objects
print(inspect.isclass(Calculator))
print(inspect.isfunction(Calculator.add))
print(inspect.ismethod(calc.add))

# Get source code (if available)
try:
    print(inspect.getsource(Calculator.add))
except OSError:
    print("Source not available")

# Get signature information
sig = inspect.signature(Calculator.add)
print(sig)  # (self, a: int, b: int) -> int

# Examine parameters
for param_name, param in sig.parameters.items():
    print(f"{param_name}: {param.annotation}")

# Get members of a class
for name, obj in inspect.getmembers(Calculator):
    if not name.startswith('_'):
        print(f"{name}: {type(obj)}")

# Classify members
methods = inspect.getmembers(Calculator, inspect.isfunction)
properties = inspect.getmembers(Calculator, lambda x: isinstance(x, property))

print("Methods:", [name for name, _ in methods])
print("Properties:", [name for name, _ in properties])
```

## Dynamic Method Calling

```python
class MathOperations:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        return a / b if b != 0 else float('inf')

# Dynamic method calling
math_ops = MathOperations()

# Using getattr to call methods dynamically
operation = "add"
result = getattr(math_ops, operation)(10, 5)
print(f"{operation}: {result}")  # add: 15

# Safe dynamic calling with error handling
def safe_call_method(obj, method_name, *args, **kwargs):
    if hasattr(obj, method_name):
        method = getattr(obj, method_name)
        if callable(method):
            try:
                return method(*args, **kwargs)
            except Exception as e:
                return f"Error calling {method_name}: {e}"
    return f"Method {method_name} not found"

# Test dynamic calling
operations = ["add", "subtract", "multiply", "divide", "power"]
for op in operations:
    result = safe_call_method(math_ops, op, 10, 2)
    print(f"{op}: {result}")
```

## Dynamic Class Creation

```python
# Create classes dynamically using type()
def init_method(self, value):
    self.value = value

def get_value(self):
    return self.value

def double_value(self):
    return self.value * 2

# Create class dynamically
DynamicClass = type(
    'DynamicClass',           # Class name
    (object,),                # Base classes
    {                         # Class dictionary
        '__init__': init_method,
        'get_value': get_value,
        'double_value': double_value,
        'class_variable': 'Dynamic!'
    }
)

# Use the dynamically created class
obj = DynamicClass(42)
print(obj.get_value())      # 42
print(obj.double_value())   # 84
print(obj.class_variable)   # Dynamic!

# Add methods dynamically to existing classes
def square_value(self):
    return self.value ** 2

# Add method to existing class
DynamicClass.square_value = square_value
print(obj.square_value())   # 1764
```

## Practical Applications

### 1. Generic Object Serializer

```python
import json
from datetime import datetime
from typing import Any, Dict

class ObjectSerializer:
    """Generic object serializer using reflection"""
    
    @staticmethod
    def to_dict(obj: Any) -> Dict[str, Any]:
        """Convert object to dictionary using reflection"""
        if hasattr(obj, '__dict__'):
            result = {'__class__': obj.__class__.__name__}
            
            for key, value in obj.__dict__.items():
                if key.startswith('_'):  # Skip private attributes
                    continue
                
                # Handle different types
                if isinstance(value, (str, int, float, bool)) or value is None:
                    result[key] = value
                elif isinstance(value, datetime):
                    result[key] = value.isoformat()
                elif hasattr(value, '__dict__'):  # Nested object
                    result[key] = ObjectSerializer.to_dict(value)
                elif isinstance(value, (list, tuple)):
                    result[key] = [ObjectSerializer.to_dict(item) if hasattr(item, '__dict__') 
                                 else item for item in value]
                else:
                    result[key] = str(value)  # Fallback to string representation
            
            return result
        else:
            return str(obj)
    
    @staticmethod
    def to_json(obj: Any) -> str:
        """Convert object to JSON string"""
        return json.dumps(ObjectSerializer.to_dict(obj), indent=2)

# Test the serializer
class Address:
    def __init__(self, street, city, country):
        self.street = street
        self.city = city
        self.country = country

class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address
        self.created_at = datetime.now()
        self._secret = "hidden"  # This won't be serialized

person = Person("Alice", 30, Address("123 Main St", "New York", "USA"))
print(ObjectSerializer.to_json(person))
```

### 2. Dynamic Plugin System

```python
import importlib
import os
from abc import ABC, abstractmethod

class PluginInterface(ABC):
    """Interface for plugins"""
    
    @abstractmethod
    def execute(self, data):
        pass
    
    @property
    @abstractmethod
    def name(self):
        pass

class PluginManager:
    """Dynamic plugin manager using reflection"""
    
    def __init__(self):
        self.plugins = {}
    
    def discover_plugins(self, plugin_dir: str):
        """Discover and load plugins from directory"""
        if not os.path.exists(plugin_dir):
            return
        
        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                module_name = filename[:-3]  # Remove .py extension
                
                try:
                    # Dynamic import
                    spec = importlib.util.spec_from_file_location(
                        module_name, 
                        os.path.join(plugin_dir, filename)
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Find plugin classes using reflection
                    for name in dir(module):
                        obj = getattr(module, name)
                        
                        if (inspect.isclass(obj) and 
                            issubclass(obj, PluginInterface) and 
                            obj != PluginInterface):
                            
                            # Instantiate and register plugin
                            plugin_instance = obj()
                            self.plugins[plugin_instance.name] = plugin_instance
                            print(f"Loaded plugin: {plugin_instance.name}")
                
                except Exception as e:
                    print(f"Failed to load plugin {module_name}: {e}")
    
    def execute_plugin(self, plugin_name: str, data):
        """Execute a specific plugin"""
        if plugin_name in self.plugins:
            return self.plugins[plugin_name].execute(data)
        else:
            raise ValueError(f"Plugin {plugin_name} not found")
    
    def list_plugins(self):
        """List all available plugins"""
        return list(self.plugins.keys())

# Example plugin implementation
class UpperCasePlugin(PluginInterface):
    @property
    def name(self):
        return "uppercase"
    
    def execute(self, data):
        return str(data).upper()

class ReversePlugin(PluginInterface):
    @property
    def name(self):
        return "reverse"
    
    def execute(self, data):
        return str(data)[::-1]

# Usage
plugin_manager = PluginManager()
# In real scenario, these would be separate files in a plugins directory
plugin_manager.plugins["uppercase"] = UpperCasePlugin()
plugin_manager.plugins["reverse"] = ReversePlugin()

print(plugin_manager.list_plugins())
print(plugin_manager.execute_plugin("uppercase", "hello world"))
print(plugin_manager.execute_plugin("reverse", "hello world"))
```

### 3. Automatic API Generator

```python
from typing import get_type_hints
import inspect

class APIGenerator:
    """Generate REST API endpoints from class methods using reflection"""
    
    def __init__(self, obj):
        self.obj = obj
        self.endpoints = self._generate_endpoints()
    
    def _generate_endpoints(self):
        """Generate endpoint information using reflection"""
        endpoints = {}
        
        for name, method in inspect.getmembers(self.obj, inspect.ismethod):
            if name.startswith('_'):  # Skip private methods
                continue
            
            # Get method signature
            sig = inspect.signature(method)
            
            # Get type hints
            type_hints = get_type_hints(method)
            
            # Generate endpoint info
            endpoint_info = {
                'method': method,
                'parameters': [],
                'return_type': type_hints.get('return', 'Any')
            }
            
            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue
                
                param_info = {
                    'name': param_name,
                    'type': type_hints.get(param_name, 'Any'),
                    'required': param.default == param.empty,
                    'default': param.default if param.default != param.empty else None
                }
                endpoint_info['parameters'].append(param_info)
            
            endpoints[name] = endpoint_info
        
        return endpoints
    
    def call_endpoint(self, endpoint_name: str, **kwargs):
        """Call an endpoint with provided arguments"""
        if endpoint_name not in self.endpoints:
            raise ValueError(f"Endpoint {endpoint_name} not found")
        
        endpoint = self.endpoints[endpoint_name]
        method = endpoint['method']
        
        # Validate required parameters
        required_params = [p['name'] for p in endpoint['parameters'] if p['required']]
        missing_params = [p for p in required_params if p not in kwargs]
        
        if missing_params:
            raise ValueError(f"Missing required parameters: {missing_params}")
        
        return method(**kwargs)
    
    def get_api_spec(self):
        """Get OpenAPI-like specification"""
        spec = {"endpoints": {}}
        
        for name, endpoint in self.endpoints.items():
            spec["endpoints"][name] = {
                "parameters": [
                    {
                        "name": p['name'],
                        "type": str(p['type']),
                        "required": p['required'],
                        "default": p['default']
                    } for p in endpoint['parameters']
                ],
                "return_type": str(endpoint['return_type'])
            }
        
        return spec

# Example service class
class UserService:
    def __init__(self):
        self.users = {}
    
    def create_user(self, name: str, age: int, email: str = None) -> dict:
        """Create a new user"""
        user_id = len(self.users) + 1
        user = {"id": user_id, "name": name, "age": age, "email": email}
        self.users[user_id] = user
        return user
    
    def get_user(self, user_id: int) -> dict:
        """Get user by ID"""
        return self.users.get(user_id, {})
    
    def list_users(self, limit: int = 10) -> list:
        """List all users with optional limit"""
        return list(self.users.values())[:limit]

# Generate API
service = UserService()
api = APIGenerator(service)

# Get API specification
import json
print(json.dumps(api.get_api_spec(), indent=2))

# Call endpoints dynamically
user = api.call_endpoint("create_user", name="Alice", age=30, email="alice@example.com")
print(user)

users = api.call_endpoint("list_users", limit=5)
print(users)
```

## Best Practices and Considerations

### When to Use Reflection

**Good Use Cases:**
- Framework development (ORM, serialization, API generation)
- Plugin systems and dynamic loading
- Debugging and development tools
- Configuration-driven behavior
- Generic utilities (serializers, validators)

**Avoid Reflection When:**
- Simple, direct approach exists
- Performance is critical
- Code clarity would suffer
- Type safety is paramount

### Performance Considerations

```python
import time

class Example:
    def method(self):
        return "result"

obj = Example()

# Direct access (fastest)
start = time.time()
for _ in range(100000):
    result = obj.method()
direct_time = time.time() - start

# Reflection access (slower)
start = time.time()
for _ in range(100000):
    result = getattr(obj, 'method')()
reflection_time = time.time() - start

print(f"Direct access: {direct_time:.4f}s")
print(f"Reflection access: {reflection_time:.4f}s")
print(f"Reflection is {reflection_time/direct_time:.1f}x slower")

# Caching getattr calls improves performance
method = getattr(obj, 'method')
start = time.time()
for _ in range(100000):
    result = method()
cached_time = time.time() - start

print(f"Cached reflection: {cached_time:.4f}s")
```

### Security Considerations

```python
# Be careful with dynamic attribute access from user input
class SafeAttributeAccess:
    allowed_attributes = {'name', 'age', 'email'}
    
    def __init__(self):
        self.name = "Alice"
        self.age = 30
        self.email = "alice@example.com"
        self._secret = "sensitive data"
    
    def safe_getattr(self, attr_name):
        """Safely get attribute with whitelist"""
        if attr_name in self.allowed_attributes:
            return getattr(self, attr_name, None)
        else:
            raise ValueError(f"Access to {attr_name} not allowed")

# Example of safe usage
obj = SafeAttributeAccess()
print(obj.safe_getattr('name'))  # OK
# print(obj.safe_getattr('_secret'))  # Raises ValueError
```

## Key Takeaways

- Enables dynamic behavior and generic solutions
- Can make code harder to understand and debug
- Reflection is slower than direct access
- Be careful with user-controlled attribute access
- Essential tool for building flexible, reusable systems
- Store reflected information to improve performance

*As they say "With great power comes great responsibility" - use reflection when it genuinely improves your design, not just because you can.*
