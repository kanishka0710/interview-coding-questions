# Bounded Object Pool for Lab Equipment Connections

## Context

Establishing a connection/session to lab test equipment (a cellular network
simulator, spectrum analyzer, etc., typically over VISA/GPIB/TCP) is expensive —
it can take real seconds to negotiate. Automated test campaigns run many test cases
in parallel across worker threads, and opening a fresh connection per test case
would be far too slow and could also exceed the equipment's own limit on
simultaneous sessions. Instead, a bounded pool of reusable connection-handle objects
is shared across threads: acquire one when you need it, return it when you're done,
and never create more than the equipment (or your license) allows.

## Problem

Implement `ObjectPool` in `object_pool.py`.

### Contract

- `ObjectPool(factory: Callable[[], T], max_size: int)` — `factory` creates a new
  handle on demand (in this repo's tests, a cheap stand-in object, but treat it as
  if it were expensive). No handles are created until first needed — the pool
  starts empty, not pre-filled.
- `acquire(timeout: float | None = None)` — a **context manager**. On `__enter__`,
  yields a handle: reuse an idle one if available, otherwise create a new one via
  `factory()` if the pool hasn't yet reached `max_size` total (checked out + idle)
  live handles, otherwise block until one is released (up to `timeout` seconds,
  raising `PoolTimeoutError` if it expires; `timeout=None` blocks indefinitely). On
  `__exit__`, the handle is returned to the idle pool automatically — **even if the
  `with` block raised an exception**.
- The total number of live handles (checked out + idle) must never exceed
  `max_size`.
- `close()` — tears down every currently-idle handle: if a handle object has a
  `close()` method, call it. Used to shut everything down between test suites.
  Checked-out handles aren't your concern here — assume callers have returned
  everything before calling `close()`.

Typical usage:

```python
pool = ObjectPool(factory=make_simulator_connection, max_size=4)

with pool.acquire(timeout=5) as conn:
    conn.send_command(...)
```

### Edge cases the tests check

- `acquire()` returns distinct handles up to `max_size` before any are returned.
- Requesting one more than `max_size` blocks, and succeeds once another thread
  releases its handle (tested with threads).
- Exceeding `max_size` with nothing ever released and a short `timeout` raises
  `PoolTimeoutError`.
- A handle returned to the pool is reused (identity check) rather than a fresh one
  being created, on the next `acquire()`.
- An exception raised inside the `with pool.acquire() as h:` block still returns
  `h` to the pool (it isn't leaked as permanently checked-out).
- `close()` calls `.close()` on every idle handle.

## Running

```
uv run pytest 12_memory_object_pool -v
```
