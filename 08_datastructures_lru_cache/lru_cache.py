"""
Scaffold for the thread-safe LRU cache.

Implement ThreadSafeLRUCache below. See README.md in this folder for the
full problem statement and contract.

Using collections.OrderedDict as your underlying storage is fine -- this
exercise is about correct LRU + thread-safety semantics, not reinventing a
linked list.
"""

from __future__ import annotations

import threading
from typing import Any

_MISSING = object()


class ThreadSafeLRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        raise NotImplementedError

    def get(self, key: Any, default: Any = _MISSING) -> Any:
        """
        Return the value for key, refreshing its recency. If key is
        absent, return `default` if given, else raise KeyError.
        """
        raise NotImplementedError

    def put(self, key: Any, value: Any) -> None:
        """
        Insert or update key, refreshing its recency. Evicts the
        least-recently-used entry if this insertion pushes the cache over
        capacity.
        """
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __contains__(self, key: Any) -> bool:
        """Membership check. Must NOT affect recency."""
        raise NotImplementedError
