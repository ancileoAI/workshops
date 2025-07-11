# Inheritance Problems - Solutions and Analysis

## Problem 1: Deep Inheritance Hierarchy

### Issues Identified:
- **6 levels of inheritance** (Vehicle → MotorVehicle → Car → Sedan → LuxurySedan → ExecutiveSedan)
- **Tight coupling** - changes ripple through entire hierarchy
- **Inflexible design** - hard to add features that don't fit the hierarchy
- **Complex initialization** - each level must call super() correctly
- **Testing nightmare** - testing ExecutiveSedan requires understanding entire chain

### Consequences:
- Adding a `Motorcycle` requires duplicating MotorVehicle logic
- Adding `start_engine()` method requires changes to 5+ classes
- Cannot easily create a `Convertible` that could be either a sedan or sports car
- Bug in `Vehicle.start()` affects all 6 classes

### Solution: Composition Over Inheritance

```python
from dataclasses import dataclass
from typing import Optional, List

# Feature-based components
@dataclass
class VehicleInfo:
    make: str
    model: str
    year: int

@dataclass
class Engine:
    engine_type: str
    fuel_level: int = 100
    is_running: bool = False
    
    def start(self):
        self.is_running = True
        return f"Engine started"
    
    def stop(self):
        self.is_running = False
        return f"Engine stopped"
    
    def refuel(self):
        self.fuel_level = 100

@dataclass
class TrunkFeature:
    is_open: bool = False
    
    def open(self):
        self.is_open = True
        return "Trunk opened"
    
    def close(self):
        self.is_open = False
        return "Trunk closed"

@dataclass
class ClimateControl:
    zones: int
    current_temps: dict = None
    
    def __post_init__(self):
        if self.current_temps is None:
            self.current_temps = {i: 22 for i in range(1, self.zones + 1)}
    
    def set_temperature(self, zone: int, temp: int):
        if 1 <= zone <= self.zones:
            self.current_temps[zone] = temp
            return f"Zone {zone} set to {temp}°C"
        return "Invalid zone"

@dataclass
class ConferenceFeatures:
    enabled: bool = False
    privacy_partition: bool = False
    
    def start_conference_mode(self):
        if self.enabled:
            return "Conference mode activated"
        return "Conference features not available"

# Composed vehicle
class Vehicle:
    def __init__(self, info: VehicleInfo, engine: Optional[Engine] = None):
        self.info = info
        self.engine = engine
        self.features = {}
    
    def add_feature(self, name: str, feature):
        self.features[name] = feature
    
    def get_feature(self, name: str):
        return self.features.get(name)
    
    def start(self):
        if self.engine:
            return self.engine.start()
        return "No engine to start"

# Easy to create different combinations
def create_executive_sedan():
    info = VehicleInfo("Mercedes", "S-Class", 2023)
    engine = Engine("V8")
    
    vehicle = Vehicle(info, engine)
    vehicle.add_feature("trunk", TrunkFeature())
    vehicle.add_feature("climate", ClimateControl(zones=4))
    vehicle.add_feature("conference", ConferenceFeatures(enabled=True, privacy_partition=True))
    
    return vehicle

def create_sports_car():
    info = VehicleInfo("Porsche", "911", 2023)
    engine = Engine("Flat-6")
    
    vehicle = Vehicle(info, engine)
    # No trunk feature (it's a sports car!)
    vehicle.add_feature("climate", ClimateControl(zones=2))
    
    return vehicle

# Usage
exec_sedan = create_executive_sedan()
print(exec_sedan.start())
print(exec_sedan.get_feature("conference").start_conference_mode())

sports_car = create_sports_car()
print(sports_car.start())
# print(sports_car.get_feature("trunk"))  # Returns None - no trunk feature
```

### Benefits:
- ✅ Easy to add new features without modifying existing code
- ✅ Flexible combinations - any vehicle can have any compatible features
- ✅ Simple testing - test each component in isolation
- ✅ Clear responsibilities - each class has one job

---

## Problem 2: Fragile Base Class

### Issues Identified:
- **Hidden dependencies** - subclasses depend on base class implementation details
- **Brittle inheritance** - optimization breaks subclasses
- **Method coupling** - `add_multiple_events` depends on `add_event` behavior
- **Unpredictable behavior** - changes in base class break child classes

### Consequences:
- `LoggingEventManager.add_multiple_events([1,2,3])` logs each event individually
- After "optimization", it would log once for the batch, not per event
- `CachingEventManager` might cache incorrectly if base implementation changes
- Unit tests pass for base class but fail for subclasses

### Solution: Observer Pattern + Dependency Injection

```python
from abc import ABC, abstractmethod
from typing import List, Protocol

# Event listener protocol
class EventListener(Protocol):
    def on_event(self, event) -> None: ...

# Event logger as separate responsibility
class EventLogger:
    def __init__(self):
        self.log = []
    
    def log_event_added(self, event):
        self.log.append(f"Adding event: {event}")
    
    def log_notification(self, event, listener_count):
        self.log.append(f"Notifying {listener_count} listeners about: {event}")

# Event cache as separate responsibility
class EventCache:
    def __init__(self):
        self.processed_events = set()
    
    def is_duplicate(self, event) -> bool:
        return event in self.processed_events
    
    def mark_processed(self, event):
        self.processed_events.add(event)

# Notification strategy
class NotificationStrategy(ABC):
    @abstractmethod
    def notify_listeners(self, listeners: List[EventListener], event) -> None:
        pass

class ImmediateNotification(NotificationStrategy):
    def notify_listeners(self, listeners: List[EventListener], event) -> None:
        for listener in listeners:
            listener.on_event(event)

class BatchNotification(NotificationStrategy):
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
        self.pending_events = []
    
    def notify_listeners(self, listeners: List[EventListener], event) -> None:
        self.pending_events.append(event)
        if len(self.pending_events) >= self.batch_size:
            self.flush(listeners)
    
    def flush(self, listeners: List[EventListener]):
        for event in self.pending_events:
            for listener in listeners:
                listener.on_event(event)
        self.pending_events.clear()

# Robust event manager using composition
class EventManager:
    def __init__(self, 
                 notification_strategy: NotificationStrategy,
                 logger: EventLogger = None,
                 cache: EventCache = None):
        self.events = []
        self.listeners = []
        self.notification_strategy = notification_strategy
        self.logger = logger
        self.cache = cache
    
    def add_event(self, event):
        # Check cache if available
        if self.cache and self.cache.is_duplicate(event):
            print(f"Event {event} already processed, skipping")
            return
        
        # Log if available
        if self.logger:
            self.logger.log_event_added(event)
        
        # Add event
        self.events.append(event)
        
        # Mark as processed
        if self.cache:
            self.cache.mark_processed(event)
        
        # Notify listeners
        if self.logger:
            self.logger.log_notification(event, len(self.listeners))
        
        self.notification_strategy.notify_listeners(self.listeners, event)
    
    def add_multiple_events(self, events):
        # Clear implementation - no hidden dependencies
        for event in events:
            self.add_event(event)
    
    def add_listener(self, listener: EventListener):
        self.listeners.append(listener)

# Usage - explicit dependencies
def create_logging_event_manager():
    logger = EventLogger()
    strategy = ImmediateNotification()
    return EventManager(strategy, logger=logger), logger

def create_caching_event_manager():
    cache = EventCache()
    strategy = ImmediateNotification()
    return EventManager(strategy, cache=cache), cache

def create_logging_caching_manager():
    logger = EventLogger()
    cache = EventCache()
    strategy = ImmediateNotification()
    return EventManager(strategy, logger=logger, cache=cache), logger, cache

# Test
class TestListener:
    def __init__(self):
        self.received_events = []
    
    def on_event(self, event):
        self.received_events.append(event)

# Robust against implementation changes
manager, logger = create_logging_event_manager()
listener = TestListener()
manager.add_listener(listener)

manager.add_multiple_events(["event1", "event2", "event3"])
print("Events received:", listener.received_events)
print("Log entries:", logger.log)
```

### Benefits:
- ✅ Explicit dependencies - no hidden coupling
- ✅ Robust to base class changes
- ✅ Easy to test each component
- ✅ Flexible combinations of behaviors

---

## Problem 3: Diamond Problem

### Issues Identified:
- **Multiple inheritance** creates diamond inheritance pattern
- **`Device.__init__` called twice** - potential for corrupted state
- **Method resolution ambiguity** - which `get_status()` is called?
- **Information loss** - only one parent's status is shown
- **Initialization order problems** - complex constructor logic

### Analysis of Current Code:
```python
# MRO: NetworkAttachedStorage -> NetworkDevice -> StorageDevice -> Device -> object
# This means:
# 1. Device.__init__ is called twice (once for each path)
# 2. super().get_status() calls NetworkDevice.get_status() (first in MRO)
# 3. StorageDevice.get_status() is never called
```

### Solution: Mixins + Protocols

```python
from typing import Protocol

# Define protocols for capabilities
class Powerable(Protocol):
    def turn_on(self) -> None: ...
    def is_powered_on(self) -> bool: ...

class Networkable(Protocol):
    def connect(self) -> None: ...
    def is_connected(self) -> bool: ...

class Mountable(Protocol):
    def mount(self) -> None: ...
    def is_mounted(self) -> bool: ...

# Base device class - single responsibility
class Device:
    def __init__(self, name: str):
        self.name = name
        self._powered_on = False
        print(f"Device created: {name}")
    
    def turn_on(self) -> None:
        self._powere
