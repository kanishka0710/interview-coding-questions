"""
Scaffold for the bounded object pool.

Implement ObjectPool below. See README.md in this folder for the full
problem statement and contract.
"""

from __future__ import annotations

import contextlib
import threading
from typing import Callable, Iterator, TypeVar

T = TypeVar("T")


class PoolTimeoutError(Exception):
    """Raised by acquire() when no handle becomes available in time."""


class ObjectPool:
    def __init__(self, factory: Callable[[], T], max_size: int) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self._factory = factory
        self.max_size = max_size
        raise NotImplementedError

    @contextlib.contextmanager
    def acquire(self, timeout: float | None = None) -> Iterator[T]:
        """
        Context manager. Yields a handle: reuse an idle one if available,
        else create via factory() if under max_size, else block (up to
        timeout, raising PoolTimeoutError on expiry). Returns the handle
        to the idle pool on exit, even if the with-block raised.
        """
        raise NotImplementedError
        yield  # pragma: no cover

    def close(self) -> None:
        """Tear down every currently-idle handle (call .close() if present)."""
        raise NotImplementedError
