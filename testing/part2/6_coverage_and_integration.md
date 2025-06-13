## Code coverage and continuous integration

### Understanding code coverage

**What coverage really measures:**
Code coverage tells you what code was **executed**, not what was **tested**. High coverage doesn't guarantee quality - it's a metric, not a goal.

**Types of Coverage:**
- **Line coverage**: Percentage of code lines executed
- **Branch coverage**: Percentage of decision paths taken
- **Function coverage**: Percentage of functions called
- **Statement coverage**: Percentage of statements executed
- **Condition coverage**: Percentage of boolean sub-expressions evaluated
- **Path coverage**: Percentage of possible paths through code

**The Coverage Pyramid of Value:**
```
Path Coverage (most valuable, hardest to achieve)
    ↓
Condition Coverage
    ↓
Branch Coverage (sweet spot for most projects)
    ↓
Line Coverage (easiest to game)
```

### Coverage Best Practices

**Setting Coverage Goals:**
- **80% branch coverage**: Reasonable target for most projects
- **100% coverage for critical paths**: Payment processing, authentication
- **Lower coverage acceptable for**: Generated code, simple getters/setters
- **Exclude from coverage**: Configuration files, migrations, third-party code

**Coverage as a code review tool:**
- Identify untested code paths
- Find dead code
- Spot missing error handling
- Discover edge cases

**The dangers of coverage worship:**
```python
# High coverage, low value
def test_user_str():
    user = User(name="Alice")
    assert str(user)  # 100% coverage, 0% meaningful testing
```

### Continuous integration philosophy

**CI is not just automated testing:**
CI is about **integrating work frequently** to detect problems early. Testing is one component of a broader practice.

**Core CI Principles:**
- **Integrate frequently**: Multiple times per day, not weekly
- **Keep builds fast**: Under 10 minutes for feedback loop
- **Fix breaks immediately**: Broken build is highest priority
- **Make builds self-testing**: Automated verification
- **Everyone sees results**: Transparent build status

### CI pipeline design

**The modern CI pipeline stages:**
```
1. Code Commit
    ↓
2. Pre-commit hooks (linting, formatting)
    ↓
3. Build stage (compile, dependencies)
    ↓
4. Unit tests (milliseconds to seconds)
    ↓
5. Integration tests (seconds to minutes)
    ↓
6. Code quality checks (coverage, static analysis)
    ↓
7. Security scanning
    ↓
8. Performance tests (optional)
    ↓
9. Deploy to staging
    ↓
10. Smoke tests
    ↓
11. Deploy to production (CD)
```

**Pipeline optimization strategies:**
- **Fail fast**: run fastest tests first
- **Parallel execution**: independent stages run concurrently
- **Incremental testing**: only test changed code (risky but fast)
- **Test impact analysis**: run tests likely to fail first
- **Build caching**: cache dependencies, docker layers, artifacts

### Advanced CI pattrns

**The test pyramid in CI:**
```
Nightly: full regression suite (hours)
    ↓
Per PR: integration tests (10-30 min)
    ↓
Per commit: unit tests (1-5 min)
    ↓
Pre-commit: linting (seconds)
```

**Feature flags in CI:**
- Test new features behind flags
- Deploy inactive code safely
- Gradual rollouts with monitoring
- Quick rollback without deployment

**Branch protection strategies:**
- Require PR reviews
- Enforce status checks
- Require up-to-date branches
- Dismiss stale reviews
- Require conversation resolution

### CI anti-patterns

**The "Broken Windows" effect:**
- Ignoring flaky tests
- Accepting intermittent failures
- Commenting out failing tests
- Allowing coverage to decline


### Metrics that matter

**Beyond coverage:**
- **Test execution time**: how long until feedback?
- **Test flakiness rate**: how often do tests fail randomly?
- **Mean time to fix**: how quickly are breaks resolved?
- **Deployment frequency**: how often do we ship?
- **Change failure rate**: how often do changes cause issues?

**The CI health dashboard:**
```
Build success rate: 98% ✓
Average build time: 8m 32s ✓
Coverage trend: 82% ↑
Flaky test count: 3 ⚠
Last deploy: 2 hours ago
```

### Making CI/CD sustainable

**Developer experience matters:**
- Fast feedback loops
- Clear error messages
- Easy local reproduction
- Documented processes
- Automated fixes where possible

**The cost of poor CI:**
- Context switching
- Blocked pull requests
- Delayed releases
- Developer frustration
- Reduced confidence
