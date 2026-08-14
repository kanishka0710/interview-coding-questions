# Token Bucket Rate Limiter

## Context

The AT-command channel to a cellular modem (or the command channel to a cellular
network simulator) can't be flooded — sending commands too fast can desync the
modem's response parser or overrun the simulator's control-plane queue. Automated
test campaigns need to throttle command dispatch to a configured rate while still
allowing short bursts (e.g., a quick sequence of setup commands at the start of a
test case).

## Problem

Implement `TokenBucketRateLimiter` in `rate_limiter.py`.

### Contract

- `TokenBucketRateLimiter(rate: float, capacity: int, time_fn: Callable[[], float] = time.monotonic)`
  - `rate` — tokens added per second.
  - `capacity` — maximum tokens the bucket can hold (also the max burst size).
  - `time_fn` — **you must call this instead of `time.monotonic()` directly**
    everywhere you need the current time. This is what makes the class testable
    without real sleeps — the tests inject a fake clock.
  - The bucket starts full (at `capacity`).
- `allow(tokens: int = 1) -> bool` — non-blocking. If `tokens` are available,
  consumes them and returns `True`. Otherwise consumes nothing and returns `False`.
  Must be safe to call from multiple threads concurrently — you must not be able to
  "oversell" tokens (e.g., two threads both getting `True` for a call that only one
  of them should have won).
- `wait_for_token(tokens: int = 1, timeout: float | None = None) -> bool` — blocks
  (sleeping in short increments, not busy-spinning) until `tokens` become available,
  then consumes them and returns `True`. If `timeout` elapses first, returns `False`
  without consuming partial tokens.

### Edge cases the tests check

- Burst behavior: a fresh bucket allows up to `capacity` immediate calls, then denies.
- Refill behavior over (simulated) time, using a fake clock the tests control.
- Thread-safety: many threads calling `allow()` simultaneously never grants more than
  `capacity` tokens at once.

## Running

```
uv run pytest 02_concurrency_rate_limiter -v
```
