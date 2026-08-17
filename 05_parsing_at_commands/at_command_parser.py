"""
Scaffold for the AT command response parser.

Implement parse_at_response() and parse_csq() below. See README.md in this
folder for the full problem statement, format examples, and contract.
"""

from __future__ import annotations

import re

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
    response = ATResponse(command=None)
    response.raw = raw

    lines = [line.strip() for line in raw.split('\r\n')]
    lines = [line for line in lines if line != '']

    idx = 0
    if lines and lines[0].startswith('AT'):
        response.command = lines[0]
        idx = 1

    status = None
    for line in lines[idx:]:
        if line == 'OK':
            status = 'OK'
        elif line == 'ERROR':
            status = 'ERROR'
        elif line.startswith('+CME ERROR:'):
            status = line
        else:
            m = re.match(r'\+(\w+):\s?(.*)', line)
            if m:
                response.info_lines.append(('+' + m.group(1), m.group(2)))

    if status is None:
        raise ValueError(f"no recognizable status line in {raw!r}")
    response.status = status

    return response
    


def parse_csq(value: str) -> tuple[int, int]:
    """
    Parse a +CSQ info line's value string (e.g. "15,99") into (rssi, ber)
    ints. 99 is a valid "unknown" sentinel for either field -- pass it
    through unchanged. Raises ValueError on malformed input.
    """
    value = value.replace(' ', '')
    lines = [line.strip() for line in value.split(',')]
    if len(lines) != 2:
        raise ValueError
    
    value1 = lines[0]
    value2 = lines[1]

    if value1.isnumeric():
        value1 = int(value1)
    else:
        raise ValueError
    if value2.isnumeric():
        value2 = int(value2)
    else:
        raise ValueError
    return (value1, value2)
