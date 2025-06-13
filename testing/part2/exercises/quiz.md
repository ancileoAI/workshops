## Interactive exercises

### Exercise 1
Given these test scenarios, categorize them into Unit/Integration/E2E:

1. Test that email validation regex works correctly
2. Test user can complete full purchase flow
3. Test database connection pooling
4. Test calculation of shopping cart total
5. Test API rate limiting
6. Test password hashing function
7. Test microservices communication
8. Test frontend form submission
9. Test JWT token generation algorithm
10. Test Redis cache hit/miss behavior
11. Test order status state machine transitions
12. Test payment webhook processing
13. Test user permission checking logic
14. Test PDF report generation
15. Test real-time notification delivery

### Exercise 2

For each scenario, decide: mock it (+) or use real implementation (-)

1. Testing a service that calculates tax rates
2. Testing a function that sends SMS notifications
3. Testing a data validation function
4. Testing interaction with Stripe payment API
5. Testing your custom User model
6. Testing current timestamp in a logging function
7. Testing your business logic service class
8. Testing file upload to AWS S3
9. Testing a sorting algorithm
10. Testing database transaction rollback


### Exercise 2

**True or False:**
1. 100% code coverage guarantees bug-free code
2. Unit tests should test implementation details
3. Integration tests can use mocks for external services
4. E2E tests should cover every possible user path
5. Tests should be written after the code is complete
6. A failing test is always bad
7. Mocking your own business logic is a good practice
8. Test names should describe what the test verifies
9. Flaky tests are acceptable if they pass most of the time
10. Performance tests belong in the unit test suite


### Exercise 9

Without seeing code, diagnose these test failure patterns:

**Pattern A:** "Test passes locally but fails in CI"
**Pattern B:** "Test passes when run alone but fails in test suite"
**Pattern C:** "Test passes Monday-Friday but fails on weekends"
**Pattern D:** "Test passes on developer machines but fails on QA environment"
**Pattern E:** "Test alternates between pass and fail with no changes"

For each pattern:
- What are likely causes?
- How would you investigate?
- How would you prevent it?

