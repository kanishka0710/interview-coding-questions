"""
Scaffold for a from-scratch thread pool with per-task timeouts.

Implement SimpleThreadPool below. See README.md in this folder for the full
problem statement and contract.

Do NOT use concurrent.futures or queue.Queue -- build the internal work
queue on threading.Lock / threading.Condition yourself.

Remember: you cannot forcibly kill a running Python thread. Design result()
and the timeout semantics around that constraint rather than fighting it.
"""

from __future__ import annotations

import threading
from typing import Any, Callable


class TaskTimeoutError(Exception):
    """Raised when a task exceeds its submit()-time timeout, or when a
    result() call's own wait timeout elapses first."""


class SimpleThreadPool:
    def __init__(self, num_workers: int) -> None:
        if num_workers <= 0:
            raise ValueError("num_workers must be positive")
        self.num_workers = num_workers
        raise NotImplementedError

    def submit(
        self,
        fn: Callable[..., Any],
        *args: Any,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Enqueue fn(*args, **kwargs) to run on a worker thread. Returns a
        task_id immediately without waiting for the task to run.

        `timeout`, if given, is the max time the task itself is allowed to
        run before result() reports it as timed out.
        """
        raise NotImplementedError

    def result(self, task_id: str, timeout: float | None = None) -> Any:
        """
        Block until the given task completes (or `timeout` seconds elapse
        waiting on this call). Returns the task's return value, re-raises
        the task's exception, or raises TaskTimeoutError. Raises KeyError
        for an unknown task_id.
        """
        raise NotImplementedError

    def shutdown(self, wait: bool = True) -> None:
        """
        Stop accepting new submit() calls. If wait=True, block until all
        already-submitted, non-timed-out tasks finish before returning.
        """
        raise NotImplementedError
