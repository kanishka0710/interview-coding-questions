"""
Scaffold for the cellular protocol log line parser.

Implement parse_log_line(), parse_log_file(), and count_events_by_layer()
below. See README.md in this folder for the full problem statement, format
examples, and contract.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable
import re


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
    # Get Timestamp - [2024-03-11 14:22:01.123]
    timestamp_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})", line)
    if timestamp_match:
        format_layout = "%Y-%m-%d %H:%M:%S.%f"
        timestamp = datetime.strptime(timestamp_match.group(), format_layout)
    else:
        return None

    # Get Layer
    layer_match = re.search(r"LAYER=(\w+)", line)
    if layer_match:
        layer = layer_match.group(1)
    else:
        return None

    # Get Event
    event_match = re.search(r"EVENT=(\w+)", line)
    if event_match:
        event_name = event_match.group(1)
    else:
        return None

    # Remainder Fields
    remaining_str = line[event_match.end():]
    pairs = re.findall(r'(\w+)=("[^"]*"|\S+)', remaining_str)
    data = dict(pairs)
    data = {k:v.strip('"') for k,v in data.items()}
    return LogEvent(timestamp=timestamp, layer=layer, event=event_name, fields=data)

def parse_log_file(lines: Iterable[str]) -> list[LogEvent]:
    """
    Parse a stream of log lines, skipping malformed ones, returning valid
    LogEvents in original order.
    """
    parsed = []
    for line in lines:
        parsed_line = parse_log_line(line)
        if parsed_line:
            parsed.append(parsed_line)
    return parsed


def count_events_by_layer(events: list[LogEvent]) -> dict[str, int]:
    """Return a {layer: count} mapping over the given events."""
    map = defaultdict(int)
    for event in events:
        map[event.layer] += 1
    return map
