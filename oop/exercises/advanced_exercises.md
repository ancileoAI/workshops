# Advanced Exercises - Deep Dive Applications

## Exercise 1: Custom Validation Metaclass

### Challenge
Design and implement a metaclass system for automatic data validation with the following features:

```python
# Target usage:
class User(ValidatedModel):
    name: str = Required(min_length=2, max_length=50)
    email: str = Required(pattern=r'^[^@]+@[^@]+\.[^@]+$')
    age: int = Required(min_value=0, max_value=150)
    tags: list = Optional(default_factory=list)
    created_at: datetime = Auto(factory=datetime.now)

# Should work like this:
user = User(name="Alice", email="alice@example.com", age=30)
# user = User(name="", email="invalid", age=-5)  # Should raise ValidationError

# Should auto-generate validation methods:
assert hasattr(User, 'validate_name')
assert hasattr(User, 'validate_email')
assert hasattr(User, 'validate_age')
```

### Requirements:
1. Create field descriptor classes (`Required`, `Optional`, `Auto`)
2. Implement the `ValidatedModel` metaclass
3. Generate validation methods automatically
4. Handle type checking and custom validators
5. Provide meaningful error messages
6. Support default values and factory functions

### Bonus Features:
- Custom validation functions
- Field dependencies (e.g., end_date > start_date)
- Nested model validation
- Serialization to/from dict

---

## Exercise 2: Event-Driven Architecture with Protocols

### Challenge
Design a type-safe event system that supports:

```python
# Events with strong typing
@dataclass
class UserRegistered(Event):
    user_id: int
    email: str
    timestamp: datetime

@dataclass
class OrderPlaced(Event):
    order_id: int
    user_id: int
    amount: Decimal

# Handlers with type safety
class EmailHandler(EventHandler[UserRegistered]):
    async def handle(self, event: UserRegistered) -> None:
        await send_welcome_email(event.email)

class AnalyticsHandler(EventHandler[OrderPlaced]):
    async def handle(self, event: OrderPlaced) -> None:
        await track_revenue(event.amount)

# Multi-event handlers
class AuditHandler(EventHandler[UserRegistered | OrderPlaced]):
    async def handle(self, event: UserRegistered | OrderPlaced) -> None:
        await log_to_audit_trail(event)

# Event bus with type safety
bus = EventBus()
bus.subscribe(UserRegistered, EmailHandler())
bus.subscribe(OrderPlaced, AnalyticsHandler())
bus.subscribe_multi([UserRegistered, OrderPlaced], AuditHandler())

# Publishing events
await bus.publish(UserRegistered(123, "test@example.com", datetime.now()))
```

### Requirements:
1. Define base `Event` class and `EventHandler` protocol
2. Implement generic `EventHandler[T]` for type safety
3. Create `EventBus` with subscription management
4. Support both single-event and multi-event handlers
5. Ensure type checking works correctly
6. Handle async operations properly

### Advanced Features:
- Event middleware (logging, metrics, filtering)
- Event replay capability
- Dead letter queue for failed events
- Event versioning and migration

---

## Exercise 3: Advanced Generic Data Pipeline

### Challenge
Build a type-safe data processing pipeline system:

```python
# Pipeline with strong typing
pipeline = (Pipeline[dict]()
    .add_step(ValidateStep[dict](schema))
    .add_step(TransformStep[dict, UserData](transform_to_user))
    .add_step(EnrichStep[UserData](add_profile_data))
    .add_step(FilterStep[UserData](is_active_user))
    .add_step(OutputStep[UserData](save_to_database)))

# Type-safe execution
results: list[UserData] = await pipeline.execute(input_data)

# Reusable steps with different types
number_pipeline = (Pipeline[int]()
    .add_step(TransformStep[int, float](lambda x: x / 100))
    .add_step(FilterStep[float](lambda x: x > 0.5))
    .add_step(OutputStep[float](print)))

# Conditional steps
conditional_pipeline = (Pipeline[dict]()
    .add_step(ValidateStep[dict](schema))
    .add_conditional_step(
        condition=lambda data: data.get('type') == 'premium',
        step=EnrichStep[dict](add_premium_features)
    )
    .add_step(OutputStep[dict](save_result)))
```

### Requirements:
1. Design generic `Pipeline[T]` class
2. Create base `PipelineStep[Input, Output]` protocol
3. Implement specific step types (`ValidateStep`, `TransformStep`, etc.)
4. Support conditional steps and branching
5. Ensure type safety throughout the pipeline
6. Handle errors gracefully with retry logic

### Advanced Features:
- Parallel step execution
- Pipeline composition (combining pipelines)
- Step dependency management
- Pipeline visualization and debugging
- Metrics collection and monitoring

---

## Capstone Project: design your own framework

### The Ultimate Challenge
Choose one of these framework types and implement it using all the advanced OOP concepts from the workshop:

### Option A: ORM Framework
Create a lightweight ORM with:
- Model definitions with relationships
- Query builder with type safety
- Migration system
- Connection pooling
- Transaction management

### Option B: Testing Framework
Build a testing framework featuring:
- Test discovery and collection
- Fixtures and dependency injection
- Parameterized tests
- Assertion framework
- Test reporting and analytics

### Option C: Configuration Management
Design a configuration system with:
- Multiple sources (files, environment, remote)
- Type validation and conversion
- Hot reloading
- Schema validation
- Environment-specific overrides

### Option D: Event Processing Framework
Create an event processing system with:
- Event sourcing capabilities
- CQRS pattern implementation
- Event replay and snapshots
- Distributed processing
- Stream processing operators

### Requirements for All Options:
1. **Use Advanced OOP Concepts**: 
   - Metaclasses for code generation
   - Protocols for type safety
   - Composition over inheritance
   - Generics for reusability

2. **Design Principles**:
   - Single Responsibility Principle
   - Open/Closed Principle  
   - Dependency Inversion
   - Interface Segregation

3. **Modern Python Features**:
   - Type hints throughout
   - Python 3.12+ syntax where applicable
   - Async/await support
   - Context managers

4. **Documentation**:
   - API documentation
   - Usage examples
   - Design decisions rationale
   - Performance considerations

5. **Testing**:
   - Unit tests for core functionality
   - Integration tests
   - Performance benchmarks
   - Type checking with mypy

### Evaluation Criteria:
- **Design Quality** (40%): Clean architecture, proper abstractions
- **Implementation** (30%): Code quality, error handling, performance
- **Usability** (20%): API design, documentation, examples
- **Innovation** (10%): Creative use of advanced concepts

### Deliverables:
1. Complete framework implementation
2. Usage documentation with examples
3. Design document explaining architectural decisions
4. Test suite demonstrating functionality
5. Performance benchmarks
6. Comparison with existing solutions

---

*These advanced exercises are designed to push your understanding and application of the concepts. Focus on clear reasoning rather than perfect implementation. The journey of building these systems teaches more than the final result.*
