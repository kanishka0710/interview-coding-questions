# Retry Scheduler (Min-Heap Backoff)

**This one asks you to write the tests yourself.** See "Your task" at the bottom.

## Context

Automated test campaigns retry flaky steps — e.g., "attach to network" occasionally
fails because of transient RF chamber interference — using exponential backoff.
With many test steps potentially in flight and pending retry at once, the runner
needs an efficient way to always know which failed step is next "due" for a retry
attempt, ordered by scheduled time, without polling every pending item on every
tick. A min-heap keyed by due-time is the natural fit — the interesting part is
handling **rescheduling** correctly, since a naive heap doesn't support efficient
"update the priority of an existing entry" and instead needs lazy deletion.

## Problem

Implement `RetryScheduler` in `retry_scheduler.py`, backed by `heapq`.

### Contract

- `RetryScheduler(time_fn: Callable[[], float] = time.monotonic)` — `time_fn` is
  called wherever you need "now"; tests inject a fake clock for determinism (see
  problem 2 for the same pattern).
- `schedule(step_id: str, delay_seconds: float) -> None` — schedules `step_id` to
  become "due" at `time_fn() + delay_seconds`. If `step_id` was already scheduled
  (pending, not yet popped), this call **replaces** its pending entry — the old due
  time no longer applies. The heap does not support cheap in-place priority updates,
  so you'll need a lazy-deletion strategy: e.g. track the current authoritative due
  time per `step_id` separately, push a new heap entry, and treat any popped entry
  that doesn't match the authoritative due time as stale and skip it.
- `pop_due(now: float | None = None) -> str | None` — pops and returns the
  `step_id` with the earliest due time that is `<= now` (defaults to `time_fn()`).
  Returns `None` if no scheduled step is due yet. Must correctly skip stale heap
  entries left behind by `schedule()` overwrites rather than ever returning a
  `step_id` for an outdated/superseded due time.
- `peek_next_due_time() -> float | None` — the smallest due time among currently
  active (non-stale) entries, or `None` if nothing is scheduled. Does not pop.
- `__len__` — number of currently active (non-stale) scheduled entries — i.e., stale
  heap entries left behind by a reschedule must not be double-counted.

### Things to think about while designing this (and your tests)

- What happens if you call `schedule()` twice for the same `step_id` before either
  due time arrives — does `pop_due()` ever emit it twice, or emit it at the old
  time?
- `len()` after several reschedules of the same handful of `step_id`s — is it
  counting active entries or raw heap size?
- Multiple different `step_id`s due at the same time — no particular order is
  required between them, but each must be poppable exactly once.
- `pop_due()` called repeatedly when nothing is due yet vs. when several things are
  due at once.

## Your task

**`test_retry_scheduler.py` is intentionally mostly empty.** Write a pytest suite
using an injected fake clock (same pattern as problem 2) covering, at minimum, the
scenarios above.

## Running

```
uv run pytest 10_datastructures_retry_scheduler -v
```
