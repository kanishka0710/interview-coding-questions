# Cellular Protocol Log Line Parser

## Context

Lower-layer protocol stacks (RRC/NAS-like) emit diagnostic log lines during test
execution. Test tooling parses these into structured events to reconstruct a
timeline and make pass/fail assertions (e.g., "did an RRCConnectionSetup event occur
within 2 seconds of the attach request?"). The log source is a live capture and is
occasionally flaky — a batch parser needs to tolerate malformed or truncated lines
without crashing the whole run, while still surfacing how many lines it had to skip.

Example log lines:

```
[2024-03-11 14:22:01.123] LAYER=RRC EVENT=RRCConnectionSetup cell_id=12345 rat=LTE
[2024-03-11 14:22:01.456] LAYER=NAS EVENT=AttachRequest imsi=001010123456789 reason="initial registration"
[2024-03-11 14:22:03.001] LAYER=RRC EVENT=RRCConnectionRelease cell_id=12345 cause=normal
```

Malformed examples that must be tolerated (skipped, not raised):

```
LAYER=RRC EVENT=RRCConnectionSetup cell_id=12345
[not-a-timestamp] LAYER=RRC EVENT=X
[2024-03-11 14:22:01.123] EVENT=X cell_id=12345
[2024-03-11 14:22:01.123] LAYER=RRC cell_id=12345
```

## Problem

Implement three functions in `log_parser.py`.

### `parse_log_line(line: str) -> LogEvent | None`

Parses one line into a `LogEvent` (dataclass, already defined in the scaffold):

```python
@dataclass
class LogEvent:
    timestamp: datetime          # parsed from "YYYY-MM-DD HH:MM:SS.mmm"
    layer: str                   # value of LAYER=
    event: str                   # value of EVENT=
    fields: dict[str, str]       # every other key=value pair (LAYER/EVENT excluded)
```

Rules:
- A valid line starts with `[<timestamp>]` followed by whitespace-separated
  `KEY=VALUE` tokens. `LAYER=` and `EVENT=` are required; everything else goes into
  `fields`.
- Values may optionally be double-quoted to contain spaces, e.g. `reason="no
  service"` — the quotes are stripped from the stored value, and the spaces inside
  are preserved as part of that one field's value (don't split on whitespace that's
  inside quotes).
- On **any** malformation (missing timestamp brackets, unparsable timestamp, missing
  `LAYER=` or `EVENT=`), return `None`. **Do not raise.**

### `parse_log_file(lines: Iterable[str]) -> list[LogEvent]`

Parses a full stream of lines, skipping (not raising on) malformed ones, and returns
the valid `LogEvent`s in the original order.

### `count_events_by_layer(events: list[LogEvent]) -> dict[str, int]`

Returns a `{layer: count}` mapping over a list of `LogEvent`s.

### Edge cases the tests check

- Well-formed lines with and without extra fields.
- Quoted values containing spaces.
- Each of the malformed variants above returning `None`.
- A mixed file of valid and invalid lines: valid ones extracted in order, invalid
  ones silently skipped.
- `count_events_by_layer` on an empty list and on a mixed-layer list.

## Running

```
uv run pytest 06_parsing_log_lines -v
```
