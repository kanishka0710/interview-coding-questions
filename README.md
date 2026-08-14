# Wireless SWE Interview Prep

A bank of Python practice problems modeled on the kind of things that come up when
interviewing for wireless/cellular test-software roles (functional & performance
testing of telephony/cellular/satellite stacks, automation, lab equipment control).
Themes covered: **concurrency**, **parsing**, **data structures (incl. thread-safe
ones)**, and **memory management**.

Every problem folder is self-contained:

- `README.md` — problem description, background context, contract, examples, edge cases.
- `*.py` scaffold — the file you actually code in. Stubs raise `NotImplementedError`.
- `test_*.py` — a pytest suite. **For most problems the tests are already written** —
  just make them pass. A few problems are marked **"write your own tests"** — for
  those, the test file is a near-empty stub and designing the test suite *is* the
  exercise (this comes up in real interviews).

No solutions are included anywhere in this repo — it's meant to be practiced against,
not read.

## Setup

```
uv sync
```

## Running tests

Run everything:

```
uv run pytest
```

Run a single problem:

```
uv run pytest 01_concurrency_bounded_queue -v
```

## Problems

| # | Folder | Topic | Tests |
|---|--------|-------|-------|
| 1 | `01_concurrency_bounded_queue` | Concurrency — producer/consumer, condition variables | given |
| 2 | `02_concurrency_rate_limiter` | Concurrency — token bucket, injectable clock | given |
| 3 | `03_concurrency_thread_pool` | Concurrency — build a thread pool from scratch, per-task timeout | **you write tests** |
| 4 | `04_concurrency_rw_lock` | Concurrency — reader/writer lock, writer starvation | given |
| 5 | `05_parsing_at_commands` | Parsing — modem AT command responses | given |
| 6 | `06_parsing_log_lines` | Parsing — cellular protocol log lines, malformed input | given |
| 7 | `07_parsing_binary_tlv` | Parsing — binary TLV framing with `struct` | **you write tests** |
| 8 | `08_datastructures_lru_cache` | Data structures — thread-safe LRU cache | given |
| 9 | `09_datastructures_ring_buffer` | Data structures — fixed-size circular buffer | given |
| 10 | `10_datastructures_retry_scheduler` | Data structures — min-heap backoff scheduler, lazy deletion | **you write tests** |
| 11 | `11_memory_weakref_pubsub` | Memory management — weak references, avoiding leaks | given |
| 12 | `12_memory_object_pool` | Memory management — bounded pool, context managers | given |

Suggested order: read the README for a folder first, then open the scaffold and
start coding. Don't peek at other folders' scaffolds for "the trick" — each is
meant to stand alone the way a 45-minute interview problem would.
