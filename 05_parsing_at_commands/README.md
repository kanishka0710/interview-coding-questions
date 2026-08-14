# AT Command Response Parser

## Context

Talking to a cellular modem over its AT command interface is a staple of automated
modem/telephony testing — querying signal quality (`AT+CSQ`), network registration
status (`AT+CREG?`), PDP context config (`AT+CGDCONT?`), etc. Raw serial responses
are plain text with a fairly loose but conventional structure, and test scripts need
them turned into structured Python objects before they can make assertions.

A typical raw response (bytes as read off the serial port, `\r\n` line endings) looks
like:

```
AT+CSQ\r\r\n+CSQ: 15,99\r\n\r\nOK\r\n
```

Or with an error:

```
AT+CFUN=1\r\r\n+CME ERROR: 10\r\n
```

Or a bare status with no info lines:

```
AT\r\r\nOK\r\n
```

Or multiple info lines (e.g. listing PDP contexts):

```
AT+CGDCONT?\r\r\n+CGDCONT: 1,"IP","internet","0.0.0.0",0,0\r\n+CGDCONT: 2,"IP","ims","0.0.0.0",0,0\r\n\r\nOK\r\n
```

## Problem

Implement two functions in `at_command_parser.py`.

### `parse_at_response(raw: str) -> ATResponse`

Parses a full raw response into an `ATResponse` (dataclass, already defined in the
scaffold):

```python
@dataclass
class ATResponse:
    command: str | None        # the echoed command, e.g. "AT+CSQ", or None if absent
    info_lines: list[tuple[str, str]]   # [(prefix, value_str), ...], e.g. [("+CSQ", "15,99")]
    status: str                 # "OK", "ERROR", or "+CME ERROR: <n>" (verbatim)
    raw: str                    # the original input, unmodified
```

Rules:
- Lines are separated by `\r\n` (there may also be a stray leading `\r` right after
  the echoed command — see the first example above — strip blank lines).
- The first non-blank line, if it starts with `AT`, is the echoed command.
- Any line matching `+PREFIX: value` before the final status line is an info line —
  keep `value` as the raw string (don't try to interpret it here).
- The final non-blank line is the status: `OK`, `ERROR`, or a `+CME ERROR: ...` line.
- Raise `ValueError` if there's no recognizable status line at all (garbage input).

### `parse_csq(value: str) -> tuple[int, int]`

Parses a `+CSQ` info line's value string, e.g. `"15,99"`, into `(rssi, ber)` as ints.
Both `99` values are valid "not known / not detectable" sentinels per the AT command
spec — pass them through as-is (don't raise, don't special-case them into `None`,
just return the int). Raise `ValueError` for a malformed value (wrong number of
fields, non-numeric fields).

### Edge cases the tests check

- Bare `OK` / `ERROR` with no info lines.
- `+CME ERROR: <n>` responses.
- Multiple info lines in one response, in order.
- Leading/trailing whitespace and the stray `\r` after the echoed command.
- Garbage input with no status line raising `ValueError`.
- `parse_csq` on valid and malformed input.

## Running

```
uv run pytest 05_parsing_at_commands -v
```
