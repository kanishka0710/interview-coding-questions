"""
Scaffold for the min-heap retry scheduler.

Implement RetryScheduler below. See README.md in this folder for the full
problem statement and contract, in particular the lazy-deletion
requirement for handling reschedules of an already-pending step_id.
"""

from __future__ import annotations

import heapq
import time
from typing import Callable


class RetryScheduler:
    def __init__(self, time_fn: Callable[[], float] = time.monotonic) -> None:
        self._time_fn = time_fn
        raise NotImplementedError

    def schedule(self, step_id: str, delay_seconds: float) -> None:
        """
        Schedule step_id to become due at time_fn() + delay_seconds. If
        step_id is already pending, this replaces its due time -- the old
        entry must become stale and never be returned by pop_due().
        """
        raise NotImplementedError

    def pop_due(self, now: float | None = None) -> str | None:
        """
        Pop and return the step_id with the earliest due time <= now
        (defaults to time_fn()), or None if nothing is due yet. Must skip
        stale entries left behind by schedule() overwrites.
        """
        raise NotImplementedError

    def peek_next_due_time(self) -> float | None:
        """Smallest due time among active entries, or None. Does not pop."""
        raise NotImplementedError

    def __len__(self) -> int:
        """Number of currently active (non-stale) scheduled entries."""
        raise NotImplementedError
