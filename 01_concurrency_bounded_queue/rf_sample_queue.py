"""
Scaffold for the bounded, thread-safe sample queue.

Implement BoundedSampleQueue below. See README.md in this folder for the
full problem statement and the exact contract your implementation must
satisfy (timeout behavior, close() semantics, etc).

Do NOT use queue.Queue or queue.SimpleQueue as a shortcut -- build this on
threading.Lock / threading.Condition yourself. A plain list or
collections.deque as the underlying storage is fine.
"""

from __future__ import annotations

import threading
import time
from typing import Any


class QueueTimeout(Exception):
    """Raised by put()/get() when the requested timeout elapses."""


# Sentinel returned by get() when the queue has been closed and drained.
SENTINEL = object()


class BoundedSampleQueue:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)
        self.buffer = []
        self.closed = False

    def put(self, item: Any, timeout: float | None = None) -> None:
        """
        Insert item, blocking while the queue is full.

        - Blocks indefinitely if timeout is None.
        - Waits up to `timeout` seconds if timeout is a float, then raises
          QueueTimeout if no space became available.
        - Raises RuntimeError if the queue has been closed.
        """
        with self.not_full:
            deadline = None if timeout is None else time.monotonic() + timeout
            while len(self.buffer) >= self.capacity and not self.closed:
                if deadline is None:
                    self.not_full.wait()
                else:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0 or not self.not_full.wait(remaining):
                        raise QueueTimeout

            if self.closed:
                raise RuntimeError("queue is closed")

            self.buffer.append(item)
            self.not_empty.notify()

    def get(self, timeout: float | None = None) -> Any:
        """
        Remove and return the oldest item (FIFO), blocking while empty.

        - Blocks indefinitely if timeout is None, *unless* the queue is
          closed, in which case it returns SENTINEL immediately once
          drained instead of blocking forever.
        - Waits up to `timeout` seconds if timeout is a float, then raises
          QueueTimeout if no item became available.
        """
        with self.not_empty:
            deadline = None if timeout is None else time.monotonic() + timeout
            while len(self.buffer) == 0 and not self.closed:
                if deadline is None:
                    self.not_empty.wait()
                else:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0 or not self.not_empty.wait(remaining):
                        raise QueueTimeout
            
            if len(self.buffer) == 0:
                return SENTINEL
            item = self.buffer.pop(0)
            self.not_full.notify()
            return item
        

    def close(self) -> None:
        """Mark the queue closed and wake up any blocked callers."""
        self.closed = True
        with self.lock:
            self.not_empty.notify_all()
            self.not_full.notify_all()

    def size(self) -> int:
        return len(self.buffer)

    def is_full(self) -> bool:
        return len(self.buffer) == self.capacity

    def is_empty(self) -> bool:
        return len(self.buffer) == 0
