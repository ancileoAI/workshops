## Instructions

For each problem:

1. **Identify the Issue**: What inheritance problem is demonstrated?
2. **Explain the Problem**: Why is this problematic for maintenance, testing, or design?
3. **Predict the Consequences**: What would happen if this code needs to change?
4. **Suggest Solutions**: What patterns could solve this problem?

**Note**: Solutions are provided in `inheritance_solutions.md`

---

## Problem 1

```python
class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.is_running = False
    
    def start(self):
        self.is_running = True
        return f"{self.make} {self.model} started"
    
    def stop(self):
        self.is_running = False
        return f"{self.make} {self.model} stopped"

class MotorVehicle(Vehicle):
    def __init__(self, make, model, year, engine_type):
        super().__init__(make, model, year)
        self.engine_type = engine_type
        self.fuel_level = 100
    
    def refuel(self):
        self.fuel_level = 100
        return "Refueled"

class Car(MotorVehicle):
    def __init__(self, make, model, year, engine_type, doors):
        super().__init__(make, model, year, engine_type)
        self.doors = doors
        self.trunk_open = False
    
    def open_trunk(self):
        self.trunk_open = True
        return "Trunk opened"

class Sedan(Car):
    def __init__(self, make, model, year, engine_type, doors, luxury_level):
        super().__init__(make, model, year, engine_type, doors)
        self.luxury_level = luxury_level
        self.climate_zones = 2 if luxury_level > 5 else 1
    
    def adjust_climate(self, zone, temperature):
        if zone <= self.climate_zones:
            return f"Climate zone {zone} set to {temperature}°C"
        return "Invalid climate zone"

class LuxurySedan(Sedan):
    def __init__(self, make, model, year, engine_type, doors, luxury_level, massage_seats):
        super().__init__(make, model, year, engine_type, doors, luxury_level)
        self.massage_seats = massage_seats
        self.valet_mode = False
    
    def enable_valet_mode(self):
        self.valet_mode = True
        return "Valet mode enabled - features restricted"

class ExecutiveSedan(LuxurySedan):
    def __init__(self, make, model, year, engine_type, doors, luxury_level, massage_seats, 
                 conference_setup):
        super().__init__(make, model, year, engine_type, doors, luxury_level, massage_seats)
        self.conference_setup = conference_setup
        self.privacy_partition = True
    
    def start_conference_mode(self):
        if self.conference_setup:
            return "Conference mode activated - Wi-Fi, screens, and partition ready"
        return "Conference setup not available"

# Usage
exec_car = ExecutiveSedan("Mercedes", "S-Class", 2023, "V8", 4, 10, True, True)
```

### Analysis Questions:
1. Count the inheritance levels. Is this reasonable?
2. What happens if you need to add a new feature that only some vehicles have?
3. How would you test the `start()` method inherited from Vehicle?
4. What if you need a `SportsCar` that doesn't fit neatly into this hierarchy?

---

## Problem 2

```python
class EventManager:
    def __init__(self):
        self.events = []
        self.listeners = []
    
    def add_event(self, event):
        self.events.append(event)
        self._notify_listeners(event)
    
    def add_multiple_events(self, events):
        for event in events:
            self.add_event(event)  # Uses the overrideable method
    
    def _notify_listeners(self, event):
        for listener in self.listeners:
            listener.on_event(event)
    
    def add_listener(self, listener):
        self.listeners.append(listener)

class LoggingEventManager(EventManager):
    def __init__(self):
        super().__init__()
        self.log = []
    
    def add_event(self, event):
        self.log.append(f"Adding event: {event}")
        super().add_event(event)
    
    def _notify_listeners(self, event):
        self.log.append(f"Notifying {len(self.listeners)} listeners about: {event}")
        super()._notify_listeners(event)

class CachingEventManager(EventManager):
    def __init__(self):
        super().__init__()
        self.event_cache = set()
    
    def add_event(self, event):
        if event not in self.event_cache:
            self.event_cache.add(event)
            super().add_event(event)
        else:
            print(f"Event {event} already processed, skipping")

# What happens if EventManager is "optimized" like this?
class OptimizedEventManager:
    def __init__(self):
        self.events = []
        self.listeners = []
    
    def add_event(self, event):
        self.events.append(event)
        self._notify_listeners(event)
    
    def add_multiple_events(self, events):
        # "Optimization": bulk add without individual notifications
        self.events.extend(events)
        # Then notify all at once
        for event in events:
            self._notify_listeners(event)
    
    def _notify_listeners(self, event):
        for listener in self.listeners:
            listener.on_event(event)
    
    def add_listener(self, listener):
        self.listeners.append(listener)

# Test scenario
class TestListener:
    def __init__(self):
        self.received_events = []
    
    def on_event(self, event):
        self.received_events.append(event)

# Usage that might break
listener = TestListener()
logging_manager = LoggingEventManager()
logging_manager.add_listener(listener)

# This calls add_event() multiple times - what gets logged?
logging_manager.add_multiple_events(["event1", "event2", "event3"])
```

### Analysis Questions:
1. What assumption does `LoggingEventManager` make about how `add_multiple_events` works?
2. How would the "optimization" in `OptimizedEventManager` break the logging functionality?
3. What happens to `CachingEventManager` if the base class changes?
4. How can you make this design more robust to base class changes?

---

## Problem 3

```python
class Device:
    def __init__(self, name):
        self.name = name
        self.power_on = False
        print(f"Device.__init__ called for {name}")
    
    def turn_on(self):
        self.power_on = True
        print(f"{self.name} powered on")
    
    def get_status(self):
        power_status = "ON" if self.power_on else "OFF"
        return f"{self.name}: {power_status}"

class NetworkDevice(Device):
    def __init__(self, name, ip_address):
        super().__init__(name)
        self.ip_address = ip_address
        self.connected = False
        print(f"NetworkDevice.__init__ called for {name}")
    
    def connect(self):
        if self.power_on:
            self.connected = True
            print(f"{self.name} connected to network at {self.ip_address}")
        else:
            print(f"Cannot connect {self.name} - device not powered on")
    
    def get_status(self):
        base_status = super().get_status()
        connection_status = "CONNECTED" if self.connected else "DISCONNECTED"
        return f"{base_status}, Network: {connection_status}"

class StorageDevice(Device):
    def __init__(self, name, capacity):
        super().__init__(name)
        self.capacity = capacity
        self.mounted = False
        print(f"StorageDevice.__init__ called for {name}")
    
    def mount(self):
        if self.power_on:
            self.mounted = True
            print(f"{self.name} storage mounted ({self.capacity})")
        else:
            print(f"Cannot mount {self.name} - device not powered on")
    
    def get_status(self):
        base_status = super().get_status()
        mount_status = "MOUNTED" if self.mounted else "UNMOUNTED"
        return f"{base_status}, Storage: {mount_status} ({self.capacity})"

class NetworkAttachedStorage(NetworkDevice, StorageDevice):
    def __init__(self, name, ip_address, capacity):
        print(f"NAS.__init__ starting for {name}")
        # Which parent should we call first?
        NetworkDevice.__init__(self, name, ip_address)
        StorageDevice.__init__(self, name, capacity)
        print(f"NAS.__init__ completed for {name}")
    
    def backup_data(self):
        if self.power_on and self.connected and self.mounted:
            return f"Backing up data on {self.name}"
        else:
            missing = []
            if not self.power_on:
                missing.append("power")
            if not self.connected:
                missing.append("network")
            if not self.mounted:
                missing.append("storage")
            return f"Cannot backup - missing: {', '.join(missing)}"
    
    def get_status(self):
        # Which get_status() method gets called by super()?
        return super().get_status()

# Usage
print("Creating NAS device:")
nas = NetworkAttachedStorage("BackupNAS", "192.168.1.100", "2TB")

print(f"\nMRO: {NetworkAttachedStorage.__mro__}")

print(f"\nInitial status: {nas.get_status()}")

print(f"\nTurning on device:")
nas.turn_on()

print(f"\nConnecting to network:")
nas.connect()

print(f"\nMounting storage:")
nas.mount()

print(f"\nFinal status: {nas.get_status()}")

print(f"\nBackup attempt: {nas.backup_data()}")
```

### Analysis Questions:
1. How many times is `Device.__init__` called? Why is this a problem?
2. Which `get_status()` method is called when you call `nas.get_status()`?
3. What information is lost due to the method resolution order?
4. How would you ensure all device information is included in the status?
5. What happens if `Device` gains a new attribute that both `NetworkDevice` and `StorageDevice` try to modify?

---

## Problem 4

```python
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value
    
    def area(self):
        return self._width * self._height
    
    def perimeter(self):
        return 2 * (self._width + self._height)

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Side must be positive")
        self._width = value
        self._height = value  # Maintain square property
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Side must be positive")
        self._width = value  # Maintain square property
        self._height = value

# Function that works with rectangles
def resize_rectangle(rect: Rectangle, new_width: int, new_height: int):
    """Resize a rectangle to new dimensions"""
    original_area = rect.area()
    
    rect.width = new_width
    rect.height = new_height
    
    expected_area = new_width * new_height
    actual_area = rect.area()
    
    print(f"Original area: {original_area}")
    print(f"Expected area: {expected_area}")
    print(f"Actual area: {actual_area}")
    print(f"Width: {rect.width}, Height: {rect.height}")
    
    return actual_area == expected_area

def test_rectangle_behavior():
    print("Testing with Rectangle:")
    rect = Rectangle(4, 5)
    result = resize_rectangle(rect, 3, 7)
    print(f"Behaves as expected: {result}\n")
    
    print("Testing with Square:")
    square = Square(4)
    result = resize_rectangle(square, 3, 7)
    print(f"Behaves as expected: {result}\n")

# Another problematic example
class Bird:
    def fly(self):
        return "Flying through the air"
    
    def make_sound(self):
        return "Generic bird sound"

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("Penguins cannot fly!")
    
    def make_sound(self):
        return "Penguin noise"
    
    def swim(self):
        return "Swimming in the ocean"

def bird_migration(birds: list[Bird]):
    """Simulate bird migration"""
    for bird in birds:
        print(f"Bird is {bird.fly()}")

# Usage
if __name__ == "__main__":
    test_rectangle_behavior()
    
    # This will crash!
    birds = [Bird(), Penguin()]
    bird_migration(birds)
```

### Analysis Questions:
1. Why does the `Square` class violate the Liskov Substitution Principle?
2. What assumptions does `resize_rectangle()` make that `Square` breaks?
3. How does the `Penguin` class violate LSP?
4. What would be better design alternatives for both examples?
5. How can you design hierarchies that don't violate LSP?

---

## Problem 5

```python
# Current inheritance-based design
class Employee:
    def __init__(self, name, employee_id, salary):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
        self.benefits = []
    
    def add_benefit(self, benefit):
        self.benefits.append(benefit)
    
    def get_annual_cost(self):
        benefit_cost = sum(benefit.annual_cost for benefit in self.benefits)
        return self.salary + benefit_cost

class Manager(Employee):
    def __init__(self, name, employee_id, salary, department):
        super().__init__(name, employee_id, salary)
        self.department = department
        self.subordinates = []
    
    def add_subordinate(self, employee):
        self.subordinates.append(employee)
    
    def get_team_cost(self):
        team_cost = sum(emp.get_annual_cost() for emp in self.subordinates)
        return self.get_annual_cost() + team_cost

class Developer(Employee):
    def __init__(self, name, employee_id, salary, programming_languages):
        super().__init__(name, employee_id, salary)
        self.programming_languages = programming_languages
        self.projects = []
    
    def add_project(self, project):
        self.projects.append(project)
    
    def can_work_on(self, technology):
        return technology in self.programming_languages

class DevManager(Manager, Developer):
    """A manager who is also a developer - multiple inheritance!"""
    def __init__(self, name, employee_id, salary, department, programming_languages):
        Manager.__init__(self, name, employee_id, salary, department)
        Developer.__init__(self, name, employee_id, salary, programming_languages)
    
    def can_review_code(self, technology):
        return self.can_work_on(technology)
    
    def assign_technical_task(self, subordinate, project, technology):
        if isinstance(subordinate, Developer) and subordinate.can_work_on(technology):
            subordinate.add_project(project)
            return f"Assigned {project} to {subordinate.name}"
        return f"Cannot assign {project} - {subordinate.name} lacks {technology} skills"

# What happens when we need more combinations?
class SeniorDeveloper(Developer):
    def __init__(self, name, employee_id, salary, programming_languages, mentees):
        super().__init__(name, employee_id, salary, programming_languages)
        self.mentees = mentees
    
    def mentor(self, junior_dev, skill):
        return f"Mentoring {junior_dev.name} in {skill}"

class Architect(SeniorDeveloper):
    def __init__(self, name, employee_id, salary, programming_languages, mentees, certifications):
        super().__init__(name, employee_id, salary, programming_languages, mentees)
        self.certifications = certifications
    
    def design_system(self, requirements):
        return f"Designing system for: {requirements}"

# New requirement: What if we need a "Senior Manager" or "Architect Manager"?
# Do we need SeniorManager, ArchitectManager, SeniorDevManager, etc.?

# Usage
dev_manager = DevManager("Alice", 101, 95000, "Engineering", ["Python", "Java"])
senior_dev = SeniorDeveloper("Bob", 102, 85000, ["Python", "Go"], [])
architect = Architect("Charlie", 103, 120000, ["Python", "Java", "AWS"], [], ["AWS Solutions Architect"])

dev_manager.add_subordinate(senior_dev)
dev_manager.add_subordinate(architect)

print(dev_manager.assign_technical_task(senior_dev, "API Service", "Go"))
print(f"Team cost: ${dev_manager.get_team_cost():,}")
```

### Analysis Questions:
1. What problems arise from the multiple inheritance in `DevManager`?
2. How many classes would you need to represent all possible combinations of roles?
3. What happens if you need to add a new role like "ProductManager" or "Designer"?
4. How would you handle an employee who changes roles?
5. What would a composition-based design look like instead?

---

*The goal isn't to never use inheritance, but to use it thoughtfully and recognize when other patterns might serve you better.*
