"""
Scaffold for the binary TLV message encoder/decoder.

Implement encode_message() and decode_message() below. See README.md in
this folder for the wire format and full contract.

Use the struct module: '>BBH' for the 4-byte header (message_type, flags,
total_length), '>BB' for each TLV's (type, length) prefix.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field


class MalformedMessageError(Exception):
    """Raised when decode_message() is given truncated or corrupt bytes."""


@dataclass
class DecodedMessage:
    message_type: int
    flags: int
    tlvs: list[tuple[int, bytes]] = field(default_factory=list)


def encode_message(message_type: int, flags: int, tlvs: list[tuple[int, bytes]]) -> bytes:
    """
    Build the wire-format bytes for a message: 4-byte header followed by
    the TLV elements. total_length in the header is computed from the
    encoded TLVs, not passed in.
    """
    raise NotImplementedError


def decode_message(data: bytes) -> DecodedMessage:
    """
    Parse wire-format bytes into a DecodedMessage. Raises
    MalformedMessageError for a too-short header, a total_length that
    doesn't match the remaining bytes, or a TLV whose declared length runs
    past the end of the available data.
    """
    raise NotImplementedError
