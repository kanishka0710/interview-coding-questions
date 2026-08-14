"""
Scaffold for the token bucket rate limiter.

Implement TokenBucketRateLimiter below. See README.md in this folder for the
full problem statement and contract.

Remember to call self._time_fn() everywhere you'd normally call
time.monotonic() -- the tests inject a fake clock to test refill behavior
deterministically.
"""

from __future__ import annotations

import time
from typing import Callable


class TokenBucketRateLimiter:
    def __init__(
        self,
        rate: float,
        capacity: int,
        time_fn: Callable[[], float] = time.monotonic,
    ) -> None:
        if rate <= 0:
            raise ValueError("rate must be positive")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.rate = rate
        self.capacity = capacity
        self._time_fn = time_fn
        raise NotImplementedError

    def allow(self, tokens: int = 1) -> bool:
        """
        Non-blocking. Returns True and consumes `tokens` if available,
        otherwise returns False and consumes nothing. Thread-safe.
        """
        raise NotImplementedError

    def wait_for_token(self, tokens: int = 1, timeout: float | None = None) -> bool:
        """
        Blocks (sleeping, not busy-spinning) until `tokens` are available or
        `timeout` seconds elapse. Returns True if tokens were consumed,
        False if it timed out.
        """
        raise NotImplementedError
