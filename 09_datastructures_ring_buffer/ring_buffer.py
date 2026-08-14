"""
Scaffold for the fixed-size ring buffer.

Implement RingBuffer below. See README.md in this folder for the full
problem statement and contract. Not required to be thread-safe -- this is
single-producer/single-consumer scope. Focus on correct circular index
arithmetic.
"""

from __future__ import annotations

from typing import Any


class RingBuffer:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        raise NotImplementedError

    def append(self, item: Any) -> None:
        """
        O(1). Add item as the newest element, silently overwriting the
        oldest element if already at capacity.
        """
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def to_list(self) -> list[Any]:
        """Return an independent list snapshot, oldest to newest."""
        raise NotImplementedError

    def __getitem__(self, index: int) -> Any:
        """
        Index over currently-held elements: 0 = oldest, len-1 = newest,
        negative indices count from the newest end. Raises IndexError for
        out-of-range indices.
        """
        raise NotImplementedError
