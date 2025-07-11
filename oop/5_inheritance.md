# Inheritance Problems and Solutions

## Problem Analysis Exercise

Before we dive into solutions, let's analyze some problematic inheritance patterns. Look at each example and identify the issues:

**Note**: Detailed analysis questions are in `exercises/inheritance_problems.md`, solutions in `exercises/inheritance_solutions.md`.

## Problem 1

```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def make_sound(self):
        return "Some sound"
    
    def eat(self):
        return f"{self.name} is eating"

class Mammal(Animal):
    def __init__(self, name, fur_color):
        super().__init__(name)
        self.fur_color = fur_color
    
    def nurse_young(self):
        return f"{self.name} is nursing young"

class Predator(Mammal):
    def __init__(self, name, fur_color, hunting_style):
        super().__init__(name, fur_color)
        self.hunting_style = hunting_style
    
    def hunt(self):
        return f"{self.name} hunts using {self.hunting_style}"

class Feline(Predator):
    def __init__(self, name, fur_color, hunting_style, claw_type):
        super().__init__(name, fur_color, hunting_style)
        self.claw_type = claw_type
    
    def retract_claws(self):
        return f"{self.name} retracts {self.claw_type} claws"

class DomesticCat(Feline):
    def __init__(self, name, fur_color, hunting_style, claw_type, owner):
        super().__init__(name, fur_color, hunting_style, claw_type)
        self.owner = owner
    
    def purr(self):
        return f"{self.name} purrs for {self.owner}"

# Usage
cat = DomesticCat("Whiskers", "orange", "stalking", "retractable", "Alice")
```

*Quick Question: What happens if you need to add a new behavior that only some animals have like flying or swimming? What if some animals are nocturnal(active at night) and others are not — where would you add that behavior in this hierarchy?*

## Problem 2

```python
class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
        self._on_change()
    
    def add(self, value):
        self.count += value
        self._on_change()
    
    def _on_change(self):
        pass  # Hook for subclasses

class LoggingCounter(Counter):
    def __init__(self):
        super().__init__()
        self.log = []
    
    def _on_change(self):
        self.log.append(f"Count changed to: {self.count}")

class BatchCounter(Counter):
    def __init__(self):
        super().__init__()
    
    def add_batch(self, values):
        for value in values:
            self.add(value)  # Uses inherited add() method

# What happens if Counter.add() is later "optimized"?
class Counter:  # Updated version
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
        self._on_change()
    
    def add(self, value):
        # New optimization: use increment for single values
        if value == 1:
            self.increment()  # This will call _on_change()
        else:
            self.count += value
            self._on_change()
```

*Quick Question: What unexpected behavior might BatchCounter.add_batch([1, 1, 1]) exhibit with the "optimized" base class?*

## Problem 3

```python
class Device:
    def __init__(self, name):
        self.name = name
        self.power_on = False
    
    def turn_on(self):
        self.power_on = True
        print(f"{self.name} powered on")
    
    def status(self):
        return f"{self.name}: {'On' if self.power_on else 'Off'}"

class NetworkDevice(Device):
    def __init__(self, name, ip_address):
        super().__init__(name)
        self.ip_address = ip_address
        self.connected = False
    
    def connect(self):
        if self.power_on:
            self.connected = True
            print(f"{self.name} connected to network")
    
    def status(self):
        base_status = super().status()
        network_status = "Connected" if self.connected else "Disconnected"
        return f"{base_status}, Network: {network_status}"

class StorageDevice(Device):
    def __init__(self, name, capacity):
        super().__init__(name)
        self.capacity = capacity
        self.mounted = False
    
    def mount(self):
        if self.power_on:
            self.mounted = True
            print(f"{self.name} storage mounted")
    
    def status(self):
        base_status = super().status()
        storage_status = "Mounted" if self.mounted else "Unmounted"
        return f"{base_status}, Storage: {storage_status}"

class NetworkAttachedStorage(NetworkDevice, StorageDevice):
    def __init__(self, name, ip_address, capacity):
        # Diamond problem: which parent to call first?
        NetworkDevice.__init__(self, name, ip_address)
        StorageDevice.__init__(self, name, capacity)
    
    def status(self):
        # Which status method gets called?
        return super().status()

# Usage
nas = NetworkAttachedStorage("MyNAS", "192.168.1.100", "2TB")
print(nas.status())  # What does this print?
print(NetworkAttachedStorage.__mro__)
```

*Quick Question: Which version of `status()` gets called? Does the `Device.__init__` get called twice?*

---

## Solution Patterns

Now let's explore modern solutions to these inheritance problems:

## Solution 1: Composition Over Inheritance

### Problem: Deep Hierarchies
Instead of deep inheritance chains, use composition to build complex objects:

```python
from dataclasses import dataclass
from typing import Optional, Protocol

# Define capabilities as separate classes
@dataclass
class AnimalInfo:
    name: str
    species: str

@dataclass
class MammalTraits:
    fur_color: str
    
    def nurse_young(self, animal_name: str) -> str:
        return f"{animal_name} is nursing young"

@dataclass
class HuntingBehavior:
    hunting_style: str
    
    def hunt(self, animal_name: str) -> str:
        return f"{animal_name} hunts using {self.hunting_style}"

@dataclass
class FelineTraits:
    claw_type: str
    
    def retract_claws(self, animal_name: str) -> str:
        return f"{animal_name} retracts {self.claw_type} claws"

@dataclass
class DomesticTraits:
    owner: str
    
    def purr(self, animal_name: str) -> str:
        return f"{animal_name} purrs for {self.owner}"

# Compose instead of inherit
class DomesticCat:
    def __init__(self, name: str, fur_color: str, hunting_style: str, 
                 claw_type: str, owner: str):
        self.info = AnimalInfo(name, "cat")
        self.mammal_traits = MammalTraits(fur_color)
        self.hunting = HuntingBehavior(hunting_style)
        self.feline_traits = FelineTraits(claw_type)
        self.domestic_traits = DomesticTraits(owner)
    
    def make_sound(self) -> str:
        return "Meow"
    
    def eat(self) -> str:
        return f"{self.info.name} is eating"
    
    # Delegate to composed objects
    def nurse_young(self) -> str:
        return self.mammal_traits.nurse_young(self.info.name)
    
    def hunt(self) -> str:
        return self.hunting.hunt(self.info.name)
    
    def retract_claws(self) -> str:
        return self.feline_traits.retract_claws(self.info.name)
    
    def purr(self) -> str:
        return self.domestic_traits.purr(self.info.name)

# Easy to create animals with different trait combinations
class WildCat:
    def __init__(self, name: str, fur_color: str, hunting_style: str, claw_type: str):
        self.info = AnimalInfo(name, "wild_cat")
        self.mammal_traits = MammalTraits(fur_color)
        self.hunting = HuntingBehavior(hunting_style)
        self.feline_traits = FelineTraits(claw_type)
        # No domestic traits
    
    def make_sound(self) -> str:
        return "Roar"
    
    # ... other methods
```

**Benefits:**
- Flexible trait combinations
- Clear responsibilities
- Easy to test individual components
- No deep inheritance chains

## Solution 2: Observer Pattern + Dependency Injection

### Problem: Fragile Base Class
Replace inheritance-based hooks with explicit observer patterns:

```python
from abc import ABC, abstractmethod
from typing import List, Protocol

class CounterObserver(Protocol):
    def on_count_changed(self, old_value: int, new_value: int) -> None:
        ...

class Counter:
    def __init__(self):
        self._count = 0
        self._observers: List[CounterObserver] = []
    
    @property
    def count(self) -> int:
        return self._count
    
    def add_observer(self, observer: CounterObserver) -> None:
        self._observers.append(observer)
    
    def remove_observer(self, observer: CounterObserver) -> None:
        self._observers.remove(observer)
    
    def _notify_observers(self, old_value: int, new_value: int) -> None:
        for observer in self._observers:
            observer.on_count_changed(old_value, new_value)
    
    def increment(self) -> None:
        old_value = self._count
        self._count += 1
        self._notify_observers(old_value, self._count)
    
    def add(self, value: int) -> None:
        old_value = self._count
        self._count += value
        self._notify_observers(old_value, self._count)

# Separate observer implementations
class LoggingObserver:
    def __init__(self):
        self.log: List[str] = []
    
    def on_count_changed(self, old_value: int, new_value: int) -> None:
        self.log.append(f"Count changed from {old_value} to {new_value}")

class AlertObserver:
    def __init__(self, threshold: int):
        self.threshold = threshold
    
    def on_count_changed(self, old_value: int, new_value: int) -> None:
        if new_value >= self.threshold:
            print(f"Alert: Counter reached {new_value}")

# Usage with dependency injection
counter = Counter()
logger = LoggingObserver()
alerter = AlertObserver(threshold=10)

counter.add_observer(logger)
counter.add_observer(alerter)

counter.increment()  # Both observers notified
counter.add(5)       # Both observers notified

# Robust against base class changes
class BatchCounter:
    def __init__(self, counter: Counter):
        self.counter = counter  # Dependency injection
    
    def add_batch(self, values: List[int]) -> None:
        for value in values:
            self.counter.add(value)  # Always calls the same method

batch_counter = BatchCounter(counter)
batch_counter.add_batch([1, 2, 3])
```

**Benefits:**
- Explicit dependencies
- Robust against base class changes
- Multiple observers possible
- Easy to test in isolation

## Solution 3: Mixins + Protocols

### Problem: Diamond Problem
Use mixins for shared behavior and protocols for interfaces:

```python
from typing import Protocol

# Define protocols for capabilities
class Powerable(Protocol):
    def turn_on(self) -> None: ...
    def turn_off(self) -> None: ...
    @property
    def is_powered_on(self) -> bool: ...

class Networkable(Protocol):
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    @property
    def is_connected(self) -> bool: ...

class Mountable(Protocol):
    def mount(self) -> None: ...
    def unmount(self) -> None: ...
    @property
    def is_mounted(self) -> bool: ...

# Mixin classes provide reusable implementations
class PowerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._powered_on = False
    
    def turn_on(self) -> None:
        self._powered_on = True
        print(f"{getattr(self, 'name', 'Device')} powered on")
    
    def turn_off(self) -> None:
        self._powered_on = False
        print(f"{getattr(self, 'name', 'Device')} powered off")
    
    @property
    def is_powered_on(self) -> bool:
        return self._powered_on

class NetworkMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._connected = False
        self.ip_address = kwargs.get('ip_address', '0.0.0.0')
    
    def connect(self) -> None:
        if hasattr(self, 'is_powered_on') and not self.is_powered_on:
            raise RuntimeError("Cannot connect: device not powered on")
        self._connected = True
        print(f"{getattr(self, 'name', 'Device')} connected to network")
    
    def disconnect(self) -> None:
        self._connected = False
        print(f"{getattr(self, 'name', 'Device')} disconnected")
    
    @property
    def is_connected(self) -> bool:
        return self._connected

class StorageMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mounted = False
        self.capacity = kwargs.get('capacity', '0GB')
    
    def mount(self) -> None:
        if hasattr(self, 'is_powered_on') and not self.is_powered_on:
            raise RuntimeError("Cannot mount: device not powered on")
        self._mounted = True
        print(f"{getattr(self, 'name', 'Device')} storage mounted")
    
    def unmount(self) -> None:
        self._mounted = False
        print(f"{getattr(self, 'name', 'Device')} storage unmounted")
    
    @property
    def is_mounted(self) -> bool:
        return self._mounted

# Base device class
class Device:
    def __init__(self, name: str, **kwargs):
        self.name = name
        super().__init__(**kwargs)
    
    def status(self) -> str:
        return f"{self.name}"

# Compose devices with needed capabilities
class NetworkAttachedStorage(Device, PowerMixin, NetworkMixin, StorageMixin):
    def __init__(self, name: str, ip_address: str, capacity: str):
        super().__init__(name=name, ip_address=ip_address, capacity=capacity)
    
    def status(self) -> str:
        base = super().status()
        power = "On" if self.is_powered_on else "Off"
        network = "Connected" if hasattr(self, '_connected') and self.is_connected else "Disconnected"
        storage = "Mounted" if hasattr(self, '_mounted') and self.is_mounted else "Unmounted"
        return f"{base}: Power={power}, Network={network}, Storage={storage}"

class SimpleNetworkDevice(Device, PowerMixin, NetworkMixin):
    def __init__(self, name: str, ip_address: str):
        super().__init__(name=name, ip_address=ip_address)
    
    def status(self) -> str:
        base = super().status()
        power = "On" if self.is_powered_on else "Off"
        network = "Connected" if self.is_connected else "Disconnected"
        return f"{base}: Power={power}, Network={network}"

# Usage
nas = NetworkAttachedStorage("MyNAS", "192.168.1.100", "2TB")
nas.turn_on()
nas.connect()
nas.mount()
print(nas.status())

router = SimpleNetworkDevice("Router", "192.168.1.1")
router.turn_on()
router.connect()
print(router.status())
```

**Benefits:**
- No diamond problem (mixins don't call super() on the same method)
- Flexible composition
- Clear separation of concerns
- Protocol-based type safety

## Solution 4: Strategy Pattern + Dependency Injection

For cases where behavior varies significantly:

```python
from typing import Protocol

class StatusReporter(Protocol):
    def get_status(self, device_name: str) -> str: ...

class PowerStatusReporter:
    def __init__(self, is_powered_on: bool):
        self.is_powered_on = is_powered_on
    
    def get_status(self, device_name: str) -> str:
        status = "On" if self.is_powered_on else "Off"
        return f"{device_name}: Power={status}"

class DetailedStatusReporter:
    def __init__(self, power: bool, network: bool, storage: bool):
        self.power = power
        self.network = network
        self.storage = storage
    
    def get_status(self, device_name: str) -> str:
        power_status = "On" if self.power else "Off"
        network_status = "Connected" if self.network else "Disconnected"
        storage_status = "Mounted" if self.storage else "Unmounted"
        return f"{device_name}: Power={power_status}, Network={network_status}, Storage={storage_status}"

class FlexibleDevice:
    def __init__(self, name: str, status_reporter: StatusReporter):
        self.name = name
        self._status_reporter = status_reporter
    
    def status(self) -> str:
        return self._status_reporter.get_status(self.name)
```

## Questions

1.Each solution has different trade-offs. When would you choose composition over mixins? When would you use the strategy pattern?
2. You have an existing codebase with deep inheritance. What would be your step-by-step approach to refactor it?
3. Which pattern would be easier for you to adopt? What are the learning curve considerations?


*Inheritance is a tool, not a goal. Use it when it genuinely simplifies your design, not just because you can.*
