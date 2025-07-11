# Basic Exercises - Individual and Group

## Exercise 1: Four Pillars

For each code snippet, identify which OOP pillar is being demonstrated and explain how.

```python
# Snippet A
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Note the double underscore
    
    def get_balance(self):
        return self.__balance
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

# Snippet B
from abc import ABC, abstractmethod

class A(ABC):
    @abstractmethod
    def method1(self):
        pass
    
    def method2(self):
        return "method2"

# Snippet C
class Animal:
    def make_sound(self):
        return "Some generic sound"

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

def animal_concert(animals):
    for animal in animals:
        print(animal.make_sound())

# Snippet D
class Vehicle:
    def start(self):
        return "Vehicle started"

class Car(Vehicle):
    def start(self):
        return "Car engine started"
    
    def open_trunk(self):
        return "Trunk opened"
```

---

## Exercise 2: Metaclass

Analyze this framework code and explain how it works:

```python
class ConfigMeta(type):
    def __new__(cls, name, bases, dct):
        if name == 'BaseConfig':
            return super().__new__(cls, name, bases, dct)
        
        # Collect config field definitions
        config_fields = {}
        for key, value in list(dct.items()):
            if isinstance(value, ConfigField):
                config_fields[key] = value
                # Load actual value from environment
                env_value = os.getenv(value.env_var, value.default)
                if env_value is None and value.required:
                    raise ValueError(f"Required config {value.env_var} not found")
                dct[key] = value.convert(env_value) if env_value else None
        
        dct['_config_fields'] = config_fields
        return super().__new__(cls, name, bases, dct)

class ConfigField:
    def __init__(self, env_var, default=None, field_type=str, required=False):
        self.env_var = env_var
        self.default = default
        self.field_type = field_type
        self.required = required
    
    def convert(self, value):
        if value is None:
            return None
        if self.field_type == bool:
            return str(value).lower() in ('true', '1', 'yes')
        return self.field_type(value)

class BaseConfig(metaclass=ConfigMeta):
    pass

# Usage
import os
os.environ['DATABASE_URL'] = 'postgresql://localhost/myapp'
os.environ['DEBUG'] = 'true'
os.environ['MAX_WORKERS'] = '8'

class AppConfig(BaseConfig):
    database_url = ConfigField('DATABASE_URL', 'sqlite:///app.db')
    debug_mode = ConfigField('DEBUG', False, bool)
    api_key = ConfigField('API_KEY', required=True)
    max_workers = ConfigField('MAX_WORKERS', 4, int)
    cache_timeout = ConfigField('CACHE_TIMEOUT', 300, int)

# This works:
print(AppConfig.database_url)  # "postgresql://localhost/myapp"
print(AppConfig.debug_mode)    # True
print(AppConfig.max_workers)   # 8
print(AppConfig.cache_timeout) # 300 (default value)

# This would fail:
# class BadConfig(BaseConfig):
#     secret = ConfigField('MISSING_SECRET', required=True)  # ValueError
```

### Questions:
- What transformation does the metaclass perform on the AppConfig class definition?
- When does the environment variable loading actually happen - at class definition time or when you access AppConfig.database_url?
- Why don't we see database_url, debug_mode, etc. as ConfigField instances anymore after the class is created?
- What happens if you try to set AppConfig.debug_mode = False after the class is created? Would it work?
- How could you add configuration validation (e.g., database_url must start with 'postgresql://' or 'sqlite://')?

---

## Exercise 3: Protocol vs ABC Design

You need to design a system for different payment processors. Compare two approaches:

### Approach A: Abstract Base Class
```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> bool:
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str) -> bool:
        pass
    
    def log_transaction(self, message: str):
        print(f"Transaction: {message}")

class StripeProcessor(PaymentProcessor):
    def process_payment(self, amount: float, currency: str) -> bool:
        self.log_transaction(f"Stripe: ${amount} {currency}")
        return True
    
    def refund_payment(self, transaction_id: str) -> bool:
        self.log_transaction(f"Stripe refund: {transaction_id}")
        return True
```

### Approach B: Protocol
```python
from typing import Protocol

class PaymentProcessor(Protocol):
    def process_payment(self, amount: float, currency: str) -> bool:
        ...
    
    def refund_payment(self, transaction_id: str) -> bool:
        ...

class StripeProcessor:
    def process_payment(self, amount: float, currency: str) -> bool:
        print(f"Stripe: ${amount} {currency}")
        return True
    
    def refund_payment(self, transaction_id: str) -> bool:
        print(f"Stripe refund: {transaction_id}")
        return True

class LegacyPayPalProcessor:
    # This class already exists and can't be modified
    def charge(self, amount: float, currency: str) -> bool:
        print(f"PayPal charge: ${amount} {currency}")
        return True
    
    def reverse_charge(self, transaction_id: str) -> bool:
        print(f"PayPal reversal: {transaction_id}")
        return True
```

### Questions:
1. Which approach allows you to use `LegacyPayPalProcessor` without modification?
2. How would you create an adapter for the legacy processor in each approach?
3. What are the pros and cons of each approach?
4. When would you
