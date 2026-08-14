"""
Scaffold for a fair reader/writer lock.

Implement ReadWriteLock below. See README.md in this folder for the full
problem statement and contract, including the writer-starvation
requirement.
"""

from __future__ import annotations

import contextlib
import threading
from typing import Iterator


class ReadWriteLock:
    def __init__(self) -> None:
        raise NotImplementedError

    @contextlib.contextmanager
    def read_lock(self) -> Iterator[None]:
        """
        Context manager. Multiple readers may hold this concurrently, but
        not while a writer holds write_lock(). Must not starve waiting
        writers under a continuous stream of new readers.
        """
        raise NotImplementedError
        yield  # pragma: no cover

    @contextlib.contextmanager
    def write_lock(self) -> Iterator[None]:
        """
        Context manager. Exclusive with both readers and other writers.
        """
        raise NotImplementedError
        yield  # pragma: no cover
