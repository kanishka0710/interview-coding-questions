# Fixed-Size Ring Buffer

## Context

A spectrum analyzer streams RF power samples at a high rate during a long soak test.
Rather than accumulating an ever-growing list (unbounded memory growth over a
multi-hour run), a fixed-capacity circular buffer holds only the most recent N
samples for rolling-window stats and display, silently overwriting the oldest sample
once full.

This one is single-producer / single-consumer scope — **it does not need to be
thread-safe**. The focus is getting the circular index arithmetic right.

## Problem

Implement `RingBuffer` in `ring_buffer.py`.

### Contract

- `RingBuffer(capacity: int)` — capacity must be a positive int.
- `append(item)` — O(1). Adds `item` as the newest element. If the buffer is already
  at `capacity`, the oldest element is silently overwritten/dropped.
- `__len__` — number of elements currently stored (`0 <= len <= capacity`).
- `capacity` — property/attribute returning the fixed capacity.
- `to_list()` — returns a plain `list` of the currently-held elements in order from
  oldest to newest. This is a snapshot — mutating the returned list must not affect
  the buffer.
- `__getitem__(index)` — indexes like a normal Python sequence over the *currently
  held* elements: `buf[0]` is the oldest, `buf[len(buf) - 1]` is the newest,
  negative indices count from the newest end (`buf[-1]` is the newest). Raises
  `IndexError` for an out-of-range index, including any index into an empty buffer.

### Edge cases the tests check

- Appending fewer items than capacity: `len()`, `to_list()`, and indexing all
  reflect only what's actually been added (no phantom `None`/zero-filled slots).
- Appending more items than capacity: oldest items are dropped, order is preserved,
  `len()` stays capped at `capacity`.
- Wrapping around the internal storage multiple times (append well beyond capacity)
  still produces correct order.
- Positive and negative indexing, including boundary indices.
- `IndexError` on an empty buffer and on out-of-range indices.
- `to_list()` returns an independent copy.

## Running

```
uv run pytest 09_datastructures_ring_buffer -v
```
