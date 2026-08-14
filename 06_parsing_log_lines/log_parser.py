"""
Scaffold for the cellular protocol log line parser.

Implement parse_log_line(), parse_log_file(), and count_events_by_layer()
below. See README.md in this folder for the full problem statement, format
examples, and contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable


@dataclass
class LogEvent:
    timestamp: datetime
    layer: str
    event: str
    fields: dict[str, str] = field(default_factory=dict)


def parse_log_line(line: str) -> LogEvent | None:
    """
    Parse one log line into a LogEvent, or return None if the line is
    malformed in any way (do not raise).
    """
    raise NotImplementedError


def parse_log_file(lines: Iterable[str]) -> list[LogEvent]:
    """
    Parse a stream of log lines, skipping malformed ones, returning valid
    LogEvents in original order.
    """
    raise NotImplementedError


def count_events_by_layer(events: list[LogEvent]) -> dict[str, int]:
    """Return a {layer: count} mapping over the given events."""
    raise NotImplementedError
