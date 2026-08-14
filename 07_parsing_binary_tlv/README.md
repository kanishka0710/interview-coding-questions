# Binary TLV Message Parser

**This one asks you to write the tests yourself.** See "Your task" at the bottom.

## Context

Lower layers of cellular protocol stacks frame messages as binary
Type-Length-Value (TLV) structures (this is a simplified stand-in for how real
NAS/RRC information elements are encoded). Test tooling that inspects an over-the-air
capture or a simulator's binary message dump needs to decode these frames to verify
message content — and needs to fail loudly and specifically on corrupt or truncated
captures rather than silently misparsing them.

## Wire format

A message is:

- **Header (4 bytes):**
  - `message_type` — 1 byte, unsigned (`uint8`)
  - `flags` — 1 byte, unsigned (`uint8`)
  - `total_length` — 2 bytes, unsigned, **big-endian** (`uint16`) — the length in
    bytes of everything that follows the header (i.e., all the TLV elements
    combined, not including the 4-byte header itself)
- **Zero or more TLV elements**, back to back, each:
  - `type` — 1 byte, unsigned (`uint8`)
  - `length` — 1 byte, unsigned (`uint8`)
  - `value` — exactly `length` raw bytes

Use the `struct` module for packing/unpacking (`>BBH` for the header, `>BB` for each
TLV's type/length).

## Problem

Implement in `tlv_parser.py`:

```python
@dataclass
class DecodedMessage:
    message_type: int
    flags: int
    tlvs: list[tuple[int, bytes]]   # [(type, value), ...] in wire order
```

### `encode_message(message_type: int, flags: int, tlvs: list[tuple[int, bytes]]) -> bytes`

Builds the full wire-format byte string described above. `total_length` in the
header must be computed, not passed in.

### `decode_message(data: bytes) -> DecodedMessage`

Parses `data` back into a `DecodedMessage`. Must raise `MalformedMessageError`
(defined in the scaffold) for any of:

- `data` shorter than 4 bytes (can't even read the header).
- Header's `total_length` doesn't match the number of bytes actually remaining
  after the header.
- A TLV's declared `length` would run past the end of the available bytes
  (truncated/corrupt TLV).

Round-tripping — `decode_message(encode_message(t, f, tlvs))` should reproduce
`t`, `f`, and `tlvs` exactly — is the core correctness property here.

## Your task

**`test_tlv_parser.py` is intentionally mostly empty.** Write a pytest suite for
`encode_message` / `decode_message`. At minimum, think about:

- Round-trip encode → decode for an empty TLV list, one TLV, and multiple TLVs.
- A TLV with a zero-length value.
- At least two distinct corruption scenarios that should raise
  `MalformedMessageError` (not just "any bad input raises something").
- Whatever else you'd want to see covered if you were reviewing this as a PR.

## Running

```
uv run pytest 07_parsing_binary_tlv -v
```
