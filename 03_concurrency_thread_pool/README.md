# Custom Thread Pool With Per-Task Timeout

**This one asks you to write the tests yourself.** See "Your task" at the bottom.

## Context

An automated test campaign runs many independent RF test cases (attach, handover,
throughput, etc.) in parallel across a fixed number of worker threads. Occasionally a
test case hangs — e.g., the network simulator stops responding — and a hung task must
not be allowed to block the rest of the campaign forever. The caller needs to be able
to ask "did this task finish, and what did it return / raise / did it time out?"
without the whole pool grinding to a halt.

**Important Python constraint to design around:** you cannot forcibly kill a running
thread in Python. If a task hangs, its worker thread stays stuck running it. What you
*can* do is stop waiting on it from the caller's side and report it as timed out, so
the caller isn't blocked — even though the underlying thread may still be alive,
occupying that worker, until/unless the task function itself returns.

## Problem

Implement `SimpleThreadPool` in `thread_pool.py`.

**Do not use `concurrent.futures`** (that's the standard-library version of exactly
this exercise) **and do not use `queue.Queue`** — build the internal work queue on
`threading.Lock` / `threading.Condition` yourself, same as problem 1.

### Contract

- `SimpleThreadPool(num_workers: int)` — spins up `num_workers` worker threads
  immediately, each pulling tasks off an internal queue.
- `submit(fn, *args, timeout: float | None = None, **kwargs) -> str` — enqueues
  `fn(*args, **kwargs)` to run on a worker thread. Returns a `task_id` **immediately**
  (does not block waiting for the task to run). `timeout`, if given, is the max time
  *the task itself* is allowed to run before it's considered timed out (see below).
- `result(task_id, timeout: float | None = None) -> Any` — blocks until the task
  identified by `task_id` completes (or up to `timeout` seconds, a *separate* timeout
  from the one passed at `submit`, governing how long this call to `result()` itself
  should wait). Behavior:
  - Returns the task's return value if it completed normally.
  - Re-raises the task's exception if it raised one.
  - Raises `TaskTimeoutError` if the task's own `timeout` (from `submit`) elapsed
    before it finished.
  - Raises `TaskTimeoutError` (or a distinct exception of your choosing — document
    it) if `result()`'s own `timeout` elapses before the task's outcome is known.
  - Raises `KeyError` for an unknown `task_id`.
- `shutdown(wait: bool = True)` — stops accepting new `submit()` calls. If
  `wait=True`, blocks until all *already-submitted, non-timed-out* tasks finish
  before returning.

### Things to think about while designing this (and your tests)

- What happens if you call `result()` on the same `task_id` twice?
- What happens if you call `result()` *before* the task has started running yet?
- Ordering: with `num_workers=1` and several tasks submitted back to back, do they
  run in submission order?
- A task that raises an exception shouldn't crash its worker thread or take down the
  pool — the next task submitted to that worker should still run.
- What does `submit()` do if called after `shutdown()`?

## Your task

Unlike the other problems in this repo, **`test_thread_pool.py` is intentionally
mostly empty.** Write a pytest suite that would give you confidence this
implementation is correct — including the concurrency edge cases above. Think about
what an interviewer would actually want to see you probe, not just the happy path.

## Running

```
uv run pytest 03_concurrency_thread_pool -v
```
