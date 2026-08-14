"""
Scaffold for the weak-reference event bus.

Implement EventBus below. See README.md in this folder for the full
problem statement and contract.

Hint: plain weakref.ref does not work correctly for bound methods (the
bound-method object is ephemeral). Look at weakref.WeakMethod for those,
and fall back to weakref.ref for plain functions/callables.
"""

from __future__ import annotations

import weakref
from typing import Callable


class EventBus:
    def __init__(self) -> None:
        raise NotImplementedError

    def subscribe(self, event_name: str, callback: Callable) -> None:
        """Store a weak reference to callback for event_name."""
        raise NotImplementedError

    def publish(self, event_name: str, *args, **kwargs) -> int:
        """
        Call every still-alive subscriber for event_name with
        (*args, **kwargs). Returns the count of callbacks invoked. Dead
        references must be purged from internal storage, not just skipped.
        """
        raise NotImplementedError

    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        """Remove callback from event_name's subscribers. No-op if absent."""
        raise NotImplementedError

    def subscriber_count(self, event_name: str) -> int:
        """Number of currently live, non-purged subscriptions for event_name."""
        raise NotImplementedError
