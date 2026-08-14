"""
Tests for TokenBucketRateLimiter. These are given -- you do not need to
write tests for this problem, just make them pass.
"""

import threading

from rate_limiter import TokenBucketRateLimiter


class FakeClock:
    """A manually-advanced clock, injected as time_fn for deterministic tests."""

    def __init__(self, start: float = 0.0):
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


def test_burst_up_to_capacity_then_denied():
    clock = FakeClock()
    limiter = TokenBucketRateLimiter(rate=1.0, capacity=5, time_fn=clock)

    for _ in range(5):
        assert limiter.allow() is True
    assert limiter.allow() is False


def test_refill_over_time():
    clock = FakeClock()
    limiter = TokenBucketRateLimiter(rate=2.0, capacity=5, time_fn=clock)

    for _ in range(5):
        assert limiter.allow() is True
    assert limiter.allow() is False

    clock.advance(1.0)  # +2 tokens
    assert limiter.allow() is True
    assert limiter.allow() is True
    assert limiter.allow() is False


def test_refill_does_not_exceed_capacity():
    clock = FakeClock()
    limiter = TokenBucketRateLimiter(rate=10.0, capacity=3, time_fn=clock)

    for _ in range(3):
        assert limiter.allow() is True

    clock.advance(100.0)  # way more than enough to overfill

    granted = 0
    for _ in range(10):
        if limiter.allow():
            granted += 1
    assert granted == 3


def test_allow_consumes_multiple_tokens_atomically():
    clock = FakeClock()
    limiter = TokenBucketRateLimiter(rate=1.0, capacity=5, time_fn=clock)

    assert limiter.allow(tokens=3) is True
    assert limiter.allow(tokens=3) is False  # only 2 left
    assert limiter.allow(tokens=2) is True


def test_wait_for_token_times_out():
    clock = FakeClock()
    limiter = TokenBucketRateLimiter(rate=1.0, capacity=1, time_fn=clock)
    assert limiter.allow() is True  # drain the bucket

    # Real timeout, real clock underneath wait_for_token's sleeping --
    # clock (fake, frozen) never advances, so this must time out.
    assert limiter.wait_for_token(timeout=0.3) is False


def test_thread_safety_never_oversells_burst():
    clock = FakeClock()
    limiter = TokenBucketRateLimiter(rate=0.0001, capacity=50, time_fn=clock)

    granted = []
    lock = threading.Lock()

    def worker():
        result = limiter.allow()
        if result:
            with lock:
                granted.append(1)

    threads = [threading.Thread(target=worker) for _ in range(500)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5)

    assert sum(granted) == 50
