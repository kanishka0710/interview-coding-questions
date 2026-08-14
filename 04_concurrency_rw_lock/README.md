# Reader/Writer Lock

## Context

A shared in-memory calibration table (e.g., cable-loss correction values per
frequency, keyed by band) is read constantly by many parallel test-case threads
during a test campaign, and occasionally updated in bulk by a calibration-refresh
thread. A plain `threading.Lock` would serialize all the readers against each other
even though concurrent reads are perfectly safe — only reads-vs-writes and
writes-vs-writes need to be exclusive.

## Problem

Implement `ReadWriteLock` in `rw_lock.py`, exposing two context managers.

### Contract

- `ReadWriteLock()`
- `read_lock()` — context manager. Any number of readers may hold the read lock
  concurrently, as long as no writer currently holds the write lock.
- `write_lock()` — context manager. Exclusive: while held, no reader and no other
  writer may be inside their respective critical section.
- **Writer starvation:** a steady stream of new readers arriving one after another
  should not be able to starve out a writer that's waiting. Once a writer is
  waiting, new readers arriving after it should queue behind it (already-in-progress
  readers are allowed to finish). This is the crux of the exercise — a naive
  readers-preferred implementation is easy; a fair one takes more care.

Typical usage:

```python
rwlock = ReadWriteLock()

with rwlock.read_lock():
    value = calibration_table.get(freq)

with rwlock.write_lock():
    calibration_table.update(new_values)
```

### Edge cases the tests check

- Multiple readers can hold the lock at the same time (verified by tracking peak
  concurrent readers).
- A writer holding the lock excludes all readers.
- A reader holding the lock excludes writers.
- Under a continuous stream of new readers, a waiting writer still acquires the
  lock within a bounded amount of time (not literal starvation).

## Running

```
uv run pytest 04_concurrency_rw_lock -v
```
