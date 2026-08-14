# Bounded, Thread-Safe Sample Queue

## Context

During RF conformance/performance testing, a background thread continuously polls a
spectrum analyzer / signal analyzer and pushes power readings into a queue. Several
consumer threads drain it concurrently: a real-time monitor UI, a logger, and a
threshold-alarm checker. Memory is bounded (the box running the test rig doesn't have
infinite RAM for a multi-hour soak test), so the queue must apply backpressure: if
consumers fall behind, producers block rather than growing the queue unboundedly.

## Problem

Implement `BoundedSampleQueue` in `rf_sample_queue.py`.

**Do not use `queue.Queue` or `queue.SimpleQueue`** — that would make this a
one-liner and defeats the point. Build it on `threading.Lock` / `threading.Condition`
yourself. A plain `list` or `collections.deque` as the underlying storage is fine.

### Contract

- `BoundedSampleQueue(capacity: int)` — capacity must be a positive int.
- `put(item, timeout=None)` — inserts `item`, blocking while the queue is full.
  - `timeout=None` blocks indefinitely.
  - `timeout=<float>` waits up to that many seconds, then raises `QueueTimeout`.
  - Raises `RuntimeError` if the queue has been closed.
- `get(timeout=None)` — removes and returns the oldest item (FIFO), blocking while empty.
  - `timeout=None` blocks indefinitely, **unless** the queue is closed and empty, in
    which case it returns the `SENTINEL` object immediately instead of blocking forever.
  - `timeout=<float>` waits up to that many seconds, then raises `QueueTimeout`.
- `close()` — marks the queue closed and wakes up any blocked callers. Items already
  in the queue are still deliverable via `get()` after `close()` — only once the
  queue is *both* closed and empty does `get()` start returning `SENTINEL`.
- `size()`, `is_full()`, `is_empty()` — non-blocking snapshots.

### Edge cases the tests check

- FIFO ordering under a single producer/consumer.
- `put()` timing out when full with no consumer draining it.
- `get()` timing out when empty with no producer filling it.
- A blocked `put()` unblocking as soon as a consumer frees space.
- Multiple blocked `get()` callers all waking up and receiving `SENTINEL` once the
  queue is closed and drained.
- Multiple producers and multiple consumers running concurrently: every item
  produced is consumed exactly once (no loss, no duplication).

## Running

```
uv run pytest 01_concurrency_bounded_queue -v
```
