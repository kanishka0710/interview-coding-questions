# Thread-Safe LRU Cache

## Context

During a long automated sweep, a measurement-ingest thread continuously records
readings (e.g., RSRP) per cell/frequency, while several assertion-checking threads
concurrently ask "what was the last measurement we saw for cell X?" Keeping every
measurement ever seen in memory isn't practical for a multi-hour soak test, but
re-scanning a giant log for every lookup is too slow — so a bounded, thread-safe
LRU (least-recently-used) cache sits in between.

## Problem

Implement `ThreadSafeLRUCache` in `lru_cache.py`.

You do **not** need to hand-roll a doubly linked list — using `collections.OrderedDict`
(with `move_to_end`) as your underlying storage is fine and expected. The focus of
this exercise is correct LRU semantics plus correct thread-safety, not reinventing a
linked list.

### Contract

- `ThreadSafeLRUCache(capacity: int)` — capacity must be a positive int.
- `get(key, default=_MISSING)` — returns the value for `key`. If `key` isn't
  present: returns `default` if one was given, otherwise raises `KeyError`. A
  successful `get()` counts as "recently used" — it must refresh the key's
  position.
- `put(key, value)` — inserts or updates `key`. Also counts as "recently used".
  If inserting a new key pushes the cache over `capacity`, evict the least-recently-
  used entry (recency defined by both `get` and `put` activity).
- `__len__` — current number of entries.
- `__contains__` — membership check. **Does not** count as "recently used" (peeking
  shouldn't promote an entry — only `get`/`put` should).
- Must be safe under concurrent `get`/`put` calls from multiple threads.

### Edge cases the tests check

- Eviction order matches actual LRU semantics (not just insertion order).
- A `get()` on an existing key refreshes its recency, changing what gets evicted
  next.
- `__contains__` does not affect recency.
- `get()` on a missing key: default behavior and explicit-default behavior.
- Updating an existing key's value via `put()` doesn't change `capacity` accounting
  and does refresh recency.
- A concurrent stress test: many threads doing random `get`/`put` calls; afterward,
  the cache is still internally consistent (`len(cache) <= capacity` always held,
  no crash, no corruption).

## Running

```
uv run pytest 08_datastructures_lru_cache -v
```
