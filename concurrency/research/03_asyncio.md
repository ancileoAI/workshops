# Asynchronous I/O, Event Loops, and OS Subsystems

> This area focuses on how software handles thousands of simultaneous I/O operations efficiently. Try to demysty the "magic" of async programming by exploring the underlying OS multiplexing primitives and contrasting them with thread-per-connection models.

## Four layers, bottom-up:

- I/O models - blocking, non-blocking, I/O multiplexing, signal-driven, and asynchronous I/O (the classic five-model taxonomy from Stevens' UNIX Network Programming). The crucial distinction: non-blocking/multiplexed = "tell me when I can read" (readiness) vs asynchronous = "read this and tell me when it's done" (completion).
- OS multiplexing primitives - select/poll (portable, O(n), the C10K bottleneck), epoll (Linux), kqueue (BSD/macOS), IOCP (Windows, completion-based), and the new kid io_uring (Linux, completion-based, the first time Linux got a true Proactor-style interface).
- Design patterns - Reactor (readiness: epoll/kqueue world - nginx, Redis, asyncio, Node/libuv on Unix) vs Proactor (completion: IOCP, io_uring, Boost.Asio). Plus the event loop's anatomy: ready callbacks, I/O poll with timeout, timers.
- Multitasking style - cooperative (the loop runs callbacks/coroutines that must yield) vs preemptive (area 1's threads). Why "one slow callback blocks everyone" is the fundamental contract of this world.

## What to cover

- The five I/O models & why "non-blocking ≠ async"
- The primitives - select: fd_set bitmap, FD_SETSIZE=1024 limit, O(n) scan each call
- Patterns & the loop itself - reactor: demultiplexer (epoll) + handlers; the loop, proactor: initiate ops, handle completions.
- Where real systems sit: redis


## Resources
Papers / essays

- Dan Kegel, "The C10K problem" - mandatory.
- "The Architecture of Open Source Applications" (aosabook.org, free): the nginx chapter (by Andrew Alexeev) - how an event-driven server is actually structured.
- Jens Axboe, "Efficient IO with io_uring" - the design doc, very readable - https://kernel.dk/io_uring.pdf

Tutorials / blogs

- Eli Bendersky's "Concurrent Servers" series (eli.thegreenplace.net, parts 1–6) - builds from sequential -> threads -> select -> epoll -> libuv in C.
- "Lord of the io_uring" (unixism.net/loti) - the community's favorite io_uring tutorial.
- libuv's "Design overview" docs (docs.libuv.org) + "An Introduction to libuv" (nikhilm.github.io/uvbook) - how one library unifies epoll/kqueue/IOCP; the diagram of libuv's loop iteration is slide-ready.
- Julia Evans - "Async IO on Linux: select, poll, and epoll" and related posts/zines - short, friendly, great for the junior half of the audience.
- Redis source: ae.c - read it with the annotated guides available online; presenting "here is a real production event loop, it fits on a slide" lands extremely well.
- Philip Roberts, "What the heck is the event loop anyway?" (JSConf EU 2014, YouTube) - the most-watched event-loop talk ever; JS-flavored but the mental model transfers, good warm-up viewing.

Python-specific

- selectors module docs (the stdlib abstraction over select/epoll/kqueue) + asyncio "low-level API" docs (loop internals).
- "A Web Crawler With asyncio Coroutines" by A. Jesse Jiryu Davis & Guido van Rossum - the 500 Lines or Less chapter (aosabook.org, free) where asyncio's author builds an event loop + coroutines from select and generators. The single most relevant text to your practical - https://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html
- David Beazley, "Build Your Own Async" (PyCon India 2019, YouTube) - live-codes an event loop with callbacks, then generators - https://www.youtube.com/watch?v=Y4Gt3Xjd7G8
