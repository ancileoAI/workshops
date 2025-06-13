## Types of Testing

### The Testing Pyramid

```
                    /\
                   /  \
                  / E2E \     ← Slow, Expensive, Few
                 /  Tests \
                /----------\
               /Integration \  ← Medium Speed, Some
              /    Tests     \
             /----------------\
            /   Unit Tests     \ ← Fast, Cheap, Many
           /____________________\
```

This is a conceptual model for balancing test types:

- **Unit Tests**: Most of your tests. They're fast, easy to write, and catch logic bugs early.
- **Integration Tests**: Test interactions between components. Fewer than unit tests but critical for confidence.
- **End-to-End (E2E) Tests**: Simulate real user behavior across the entire system. Valuable but costly, so keep them few.

### Types

#### Unit Tests
- **What**: Test individual functions/methods in isolation
- **Speed**: Very fast (milliseconds)
- **Scope**: Single function or class
- **Dependencies**: Mocked or stubbed
- **Example**: Testing a single responsibility function

#### Integration Tests
- **What**: Test how components work together
- **Speed**: Moderate (seconds)
- **Scope**: Multiple components
- **Dependencies**: Some real, some mocked
- **Example**: Testing API endpoint with database

#### End-to-End (E2E) Tests
- **What**: Test complete user workflows
- **Speed**: Slow (minutes)
- **Scope**: Entire application
- **Dependencies**: All real
- **Example**: User login → create order → payment → confirmation

### Other Important Types

#### Functional Testing
- **What**: Verifies that the system behaves according to business requirements.
- **How**: Black-box style — test inputs and expected outputs without knowing internal code.
- **Example**: If a user enters a valid email, they should receive a confirmation.

#### Non-Functional Testing
- **What**: Evaluates *how well* the system performs rather than *what* it does.
- **Types**:
  - **Performance testing**: Can the system handle 1000 users at once?
  - **Load testing**: How does it behave under heavy traffic?
  - **Security testing**: Can an attacker exploit a vulnerability?
  - **Usability testing**: Is the UI intuitive?

#### Regression Testing
- **What**: Ensures that new code doesn’t break existing features.
- **When**: Run automatically after every change or deployment.
- **How**: Usually part of your CI/CD pipeline.
- **Goal**: Avoid “bad” moments after pushing new features.

#### Smoke Testing
- **What**: Quick sanity check to see if the app “starts” and the basics work.
- **Example**: Can the API respond to a health check? Does the homepage load?
- **When**: After deployment or big merges.
- **Goal**: Fast feedback — "is the build broken?"
