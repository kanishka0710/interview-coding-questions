"""
Scaffold for the AT command response parser.

Implement parse_at_response() and parse_csq() below. See README.md in this
folder for the full problem statement, format examples, and contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ATResponse:
    command: str | None
    info_lines: list[tuple[str, str]] = field(default_factory=list)
    status: str = ""
    raw: str = ""


def parse_at_response(raw: str) -> ATResponse:
    """
    Parse a raw AT command response (as read off a serial port, '\\r\\n'
    line endings) into an ATResponse. Raises ValueError if no recognizable
    status line (OK / ERROR / +CME ERROR: ...) is found.
    """
    raise NotImplementedError


def parse_csq(value: str) -> tuple[int, int]:
    """
    Parse a +CSQ info line's value string (e.g. "15,99") into (rssi, ber)
    ints. 99 is a valid "unknown" sentinel for either field -- pass it
    through unchanged. Raises ValueError on malformed input.
    """
    raise NotImplementedError
