# Classic Concurrency Design Patterns & Work Coordination

> This area scales up from low-level primitives to architectural patterns used to orchestrate complex operations, manage thread lifecycles, and safely pass data between execution units. It also covers the paradigm shifts in how we conceptualize asynchronous control flow.

# What to cover

- Study the Producer-Consumer pattern and Thread Pools. Understand why unbounded queues are dangerous and how bounded queues provide backpressure.
-Fork-Join framework and work-stealing algorithms, where idle threads steal tasks from the queues of busy threads to maximize CPU utilization.
- Trace the evolution from Callbacks -> Futures/Promises -> Async/Await semantics.
- Modern Paradigms: explore the "function coloring" debate and the rise of Structured Concurrency. Look at Java's Project Loom (Virtual Threads) as a modern solution to the C10K problem without function coloring.
- Design a data processing pipeline (in Python or Java) utilizing a thread pool with a bounded, work-stealing queue. Skew the workload sizes and measure the throughput to demonstrate load balancing.
- Futures/promises -> async/await -> the debate

## Resources:

### Papers/ essays
- Blumofe & Leiserson, "Scheduling Multithreaded Computations by Work Stealing" - read §1–2 for the idea
- Nystrom, "What Color is Your Function?" - https://journal.stuffwithstuff.com/2015/02/01/what-color-is-your-function/
- Trio's documentation (trio.readthedocs.io) - the tutorial section is the best prose ever written on structured concurrency

### Talks
- Rob Pike, "Go Concurrency Patterns" (Google I/O 2012) - pipelines/fan-in/fan-out with channels; the pattern talk - youtube.com/watch?v=f6kdp27TYZs
- Roman Elizarov, "Structured concurrency" (Hydra 2019, YouTube).

Note: area 6 owns everything Python-version-specific (TaskGroups' API details, free threading) so you can mention asyncio.TaskGroup as structured concurrency's Python handing to them
