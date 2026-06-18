# Race Conditions, Synchronization Primitives & Concurrency Bugs

> A practical exploration of what goes wrong when concurrent code interacts unpredictably. This area focuses on identifying, reproducing, and fixing classic concurrency bugs, as well as utilizing "modern" tooling to catch these errors before production.

## What to cover

Think of if like this: concurrency bugs follow a small number of recurring patterns. Here are the patterns, here is each one failing live, here is the disciplined fix, and here are the tools that catch them before going prod does.

- Categorize the bugs - understand the difference between "data races" (unsynchronized access to shared memory) and logical "race conditions" (e.g. check-then-act or atomicity violations).
- Study famous patterns of failure: deadlocks (circular waits), livelocks, starvation, and lock ordering inversions.
- practical implementation: - write deliberately broken code: e.g., a bank-transfer method that deadlocks, or a lost-update counter.

## Resources
Papers and articles

- "The Double-Checked Locking is Broken" Declaration* by Bill Pugh, Doug Lea, et al. (explaining why a seemingly clever optimization failed due to memory model reordering) - https://www.cs.umd.edu/~pugh/java/memoryModel/DoubleCheckedLocking.html
- ThreadSanitizer (TSan) documentation by Google/LLVM. - https://clang.llvm.org/docs/ThreadSanitizer.html
- "Learning from Mistakes: A Comprehensive Study on Real World Concurrency Bug Characteristics" - https://www.cs.columbia.edu/~junfeng/09fa-e6998/papers/concurrency-bugs.pdf
- go test -race docs - design note explains dynamic race detection well - https://go.dev/doc/articles/race_detector
- How To Corrupt An SQLite Database File - https://www.sqlite.org/howtocorrupt.html
