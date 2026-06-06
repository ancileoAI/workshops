# Foundations: Concurrency vs Parallelism, Processes, Threads, the OS & the CPU

> Build the mental model everyone else's talk depends on - what concurrency is, how the OS gives it to us, and why the physical shape of the CPU (cores, caches, cache lines) decides whether parallel code is fast or unexpectedly slow.

---

## Why this area exists

Every other topic in this session (locks, async, the GIL, work-stealing) is a response to facts established here:

- **"The Free Lunch Is Over"** (2005) is the canonical statement of this turning point and a perfect opening slide.
- Concurrency and parallelism are different things. Rob Pike's talk "Concurrency Is Not Parallelism" made this distinction mainstream.
- Understanding what a context switch costs and what a thread actually is (a stack + register state + kernel scheduling entity) makes it clearer later on to understand.

## What to cover

### Concepts and vocabulary (the map)
- Concurrency vs parallelism; task vs thread vs process.
- Process anatomy: address space, file descriptors, threads inside it. Thread anatomy: stack, registers, thread-local storage.
- Kernel threads vs user-space ("green") threads vs hybrid (M:N) models (short just to plant the seed for the async talk).
- Preemptive vs cooperative multitasking (again, a hook for area 3).
- CPU-bound vs I/O-bound workloads - most practical classification a backend engineer makes.

### The OS layer
- How Linux creates threads: `fork()` vs `clone()` flags; why on Linux a thread is just a process sharing an address space (the task_struct view).
- The scheduler: timeslices, run queues, voluntary vs involuntary context switches.
- Cost of a context switch: direct cost (register save/restore, kernel crossing) vs indirect cost (cache and TLB pollution - usually dominant). 

### Scaling laws
- Amdahl's Law (1967): speedup is capped by the serial fraction. Derive it on one slide; show the brutal curve (95% parallel code maxes out at 20× no matter how many cores).
- **Gustafson's Law** (1988) as the rebuttal: scale the *problem*, not just the machine.
- Universal Scalability Law (Gunther) as an optional extra - it adds the *coherence penalty* term, which is exactly what your false-sharing demo measures in the wild.

### CPU architecture where it matters for parallelism
- Memory hierarchy with real numbers: register < L1 (~1 ns) < L2 < L3 < RAM (~100 ns). (can use the interactive table from resources)
- Cache lines (64 B), cache coherency, and the MESI protocol at the "states and arrows" level, enough to explain why one core writing a line invalidates it in every other core's cache.
- True sharing vs false sharing
- Hardware threads / SMT (hyper-threading): why 8 "CPUs" may be 4 cores;
- Out-of-order execution and store buffers -= as a teaser handing off to the Memory Models talk (area 2): "the CPU reorders your memory operations; here's whose problem that becomes."

## Practical examples
- Context-switch cost: two threads ping-ponging on a pipe vs a function call loop; or just show `vmstat`/`pidstat -w` counting switches.
- Amdahl in practice: parallelize a loop where 10% is serial and plot speedup vs thread count (matplotlib).

## Key questions
1. What's the difference between concurrency and parallelism - with one concrete backend example of each?
2. What does a thread cost (memory, creation, context switch), and where do those costs come from?
3. Why does Amdahl's law put a ceiling on speedup, and what does Gustafson change?
4. What is a cache line, and why does the CPU move memory in cache-line units?
5. Demo: why did two threads writing to "different" variables get slower - and what fixed it?
6. Handoff: if cores have private caches, who guarantees they agree on memory contents, and what happens when the compiler/CPU reorders writes? (-> area 2.)

## Resources

### Papers & essays
- Drepper, What Every Programmer Should Know About Memory (2007) - read Parts 1–3 and 6 (https://people.freebsd.org/~lstewart/articles/cpumemory.pdf). The cornerstone for your practical demo.
- Sutter, The Free Lunch Is Over (2005) - http://www.gotw.ca/publications/concurrency-ddj.htm
- Sutter, Eliminate False Sharing (Dr. Dobb's, 2009) - a how-to for your demo.

### Talks (community-praised)
- **Scott Meyers, "CPU Caches and Why You Care"** (code::dive 2014) - the most-recommended caches talk ever; contains a false-sharing demo you can adapt. https://www.youtube.com/watch?v=WDIkqP4JbkE
- **Rob Pike, "Concurrency Is Not Parallelism"** (Heroku Waza 2012) - https://go.dev/blog/waza-talk
- Mike Acton, "Data-Oriented Design and C++" (CppCon 2014) - cache-consciousness as a design philosophy; optional but inspiring.
- Matt Godbolt, "What Has My Compiler Done for Me Lately?" (CppCon 2017) - for comfort reading assembly in Compiler Explorer.

### Other
- Amdahl's law - https://en.wikipedia.org/wiki/Amdahl%27s_law
- Interactive table form "Latency Numbers Every Programmer Should Know" - https://colin-scott.github.io/personal_website/research/interactive_latency.html.


## Historical cornerstones (what shaped this field)

| Year | Milestone | Why it matters |
|---|---|---|
| 1965 | Dijkstra, *Cooperating Sequential Processes* | Birth of concurrent programming as a discipline |
| 1967 | Amdahl's paper on the validity of single-processor approaches | The scaling ceiling, still quoted daily |
| ~1970s–80s | Unix process model; later POSIX threads (pthreads, standardized 1995) | The API model every language still wraps |
| 1988 | Gustafson, *Reevaluating Amdahl's Law* | The optimistic counterpoint; HPC's foundation |
| 2002–2005 | Power wall hits; Intel cancels Tejas; multicore becomes the roadmap | Why concurrency became everyone's problem |
| 2005 | Sutter, *The Free Lunch Is Over* (Dr. Dobb's) | The wake-up call essay |
| 2007 | Drepper, *What Every Programmer Should Know About Memory* | The definitive (114-page!) treatment of caches, lines, NUMA |
| 2012 | Pike, *Concurrency Is Not Parallelism* | Fixed the vocabulary for a generation |
