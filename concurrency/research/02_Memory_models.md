# Memory Models, Locks, and Lock-Free Primitives

> This topic explores the mechanisms required to ensure data safety when multiple execution contexts access shared memory. It transitions from traditional blocking mechanisms (locks) to modern hardware-supported lock-free structures.

---

## Two intertwined threads

1. Memory consistency models - the contract between programmer, compiler, and CPU about the order in which memory operations become visible across threads. Sequential consistency as the intuitive ideal; the weakly-ordered reality of real hardware (x86's TSO vs ARM's much weaker model); and the language-level models (C/C++11, Java's JMM) that let us write portable concurrent code.
2. Synchronization machinery - blocking primitives (mutexes, semaphores, spinlocks, and how a real mutex is built on futex), their failure modes (deadlock, livelock, priority inversion), and the lock-free world built directly on atomicss.

4. Resources

Herlihy & Shavit (+ Luchangco & Spear in 2nd ed.), "The Art of Multiprocessor Programming" - the academic canon: linearizability, consensus numbers, spin locks, lock-free structures. Read chapters selectively (1–3, 7, 10–11); it's dense.
Mara Bos, "Rust Atomics and Locks" (2023) - free to read online at marabos.nl/atomics. The community's favorite modern entry point: builds spinlocks, mutexes, condition variables, channels and an Arc from raw atomics, explaining memory ordering with unusual clarity. Even if your team never writes Rust, chapters 1–4 are the best memory-ordering tutorial in print.
Anthony Williams, "C++ Concurrency in Action" (2nd ed., 2019) - chapter 5 is the standard reference on the C++ memory model; chapter 7 walks through lock-free design honestly (including how hard it is).
Paul McKenney, "Is Parallel Programming Hard, And, If So, What Can You Do About It?" (perfbook) - free PDF (kernel.org → people/paulmck/perfbook). Written by the RCU author/Linux kernel veteran. Chapters on counting, locking, and memory ordering are superb; the hardware appendix complements Area 1.

Papers (short and readable)

- Lamport 1979 (sequential consistency) - 2 pages.
- Adve & Gharachorloo, "Shared Memory Consistency Models: A Tutorial" (IEEE Computer, 1996) - classic survey
- Michael & Scott 1996 (queues).
- LMAX Disruptor technical paper (2011) - short, industrial, includes the false-sharing/cache-line story (bridges to area 1).
- "The 'Double-Checked Locking is Broken' Declaration" (Pugh et al.) - coordinate with area 4, which demos the bug; you explain why via the memory model.

Talks

- Herb Sutter, "atomic Weapons" (C++ and Beyond 2012, 2 parts) - Long, but the first hour gives you most of your research: https://www.youtube.com/watch?v=A8eCGOqgvH4
- Fedor Pikus, "C++ atomics, from basic to advanced" and "Spinlocks" talks - https://www.youtube.com/watch?v=ZQFzMfHIxng

Blogs / community gems

- preshing.com (Jeff Preshing) - memory-model explainer: "An Introduction to Lock-Free Programming," "Acquire and Release Semantics," "Memory Barriers Are Like Source Control."
- Dmitry Vyukov - Go race detector author; the definitive practical pages on lock-free queues, including SPSC designs. Practical part's blueprint - https://sites.google.com/site/1024cores/home/lock-free-algorithms/first-things-first?authuser=0
- Drepper, "Futexes Are Tricky" - how Linux mutexes really work.
