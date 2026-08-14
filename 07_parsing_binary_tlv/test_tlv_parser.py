"""
Write your own pytest suite for encode_message() / decode_message() here.

See the README in this folder for the wire format and full contract.
Things worth designing tests around (not exhaustive -- add more of your
own):

  - Round-trip encode -> decode: empty TLV list, one TLV, multiple TLVs.
  - A TLV with a zero-length value.
  - At least two distinct corruption scenarios that should raise
    MalformedMessageError:
      * data shorter than the 4-byte header
      * total_length in the header not matching the actual remaining bytes
      * a TLV's declared length running past the end of the data
  - Whatever else you'd want to see covered if reviewing this as a PR.

This file is deliberately not wired up with any tests yet -- that's the
point of this exercise.
"""

from tlv_parser import (  # noqa: F401
    DecodedMessage,
    MalformedMessageError,
    decode_message,
    encode_message,
)
