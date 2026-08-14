"""
Tests for the cellular protocol log line parser. These are given -- you do
not need to write tests for this problem, just make them pass.
"""

from datetime import datetime

import pytest

from log_parser import count_events_by_layer, parse_log_file, parse_log_line


def test_valid_line_basic_fields():
    line = "[2024-03-11 14:22:01.123] LAYER=RRC EVENT=RRCConnectionSetup cell_id=12345 rat=LTE"
    ev = parse_log_line(line)
    assert ev is not None
    assert ev.timestamp == datetime(2024, 3, 11, 14, 22, 1, 123000)
    assert ev.layer == "RRC"
    assert ev.event == "RRCConnectionSetup"
    assert ev.fields == {"cell_id": "12345", "rat": "LTE"}


def test_valid_line_no_extra_fields():
    line = "[2024-03-11 14:22:03.001] LAYER=RRC EVENT=RRCConnectionRelease"
    ev = parse_log_line(line)
    assert ev is not None
    assert ev.fields == {}


def test_quoted_value_with_spaces_preserved():
    line = (
        '[2024-03-11 14:22:01.456] LAYER=NAS EVENT=AttachRequest '
        'imsi=001010123456789 reason="initial registration"'
    )
    ev = parse_log_line(line)
    assert ev is not None
    assert ev.fields["reason"] == "initial registration"
    assert ev.fields["imsi"] == "001010123456789"


@pytest.mark.parametrize(
    "line",
    [
        "LAYER=RRC EVENT=RRCConnectionSetup cell_id=12345",
        "[not-a-timestamp] LAYER=RRC EVENT=X",
        "[2024-03-11 14:22:01.123] EVENT=X cell_id=12345",
        "[2024-03-11 14:22:01.123] LAYER=RRC cell_id=12345",
        "",
        "   ",
        "[2024-03-11 14:22:01.123]",
    ],
)
def test_malformed_lines_return_none(line):
    assert parse_log_line(line) is None


def test_parse_log_file_skips_malformed_preserves_order():
    lines = [
        "[2024-03-11 14:22:01.123] LAYER=RRC EVENT=RRCConnectionSetup cell_id=1",
        "this line is garbage",
        "[2024-03-11 14:22:01.456] LAYER=NAS EVENT=AttachRequest imsi=1",
        "[missing brackets LAYER=RRC EVENT=X",
        "[2024-03-11 14:22:03.001] LAYER=RRC EVENT=RRCConnectionRelease cell_id=1",
    ]
    events = parse_log_file(lines)
    assert [e.event for e in events] == [
        "RRCConnectionSetup",
        "AttachRequest",
        "RRCConnectionRelease",
    ]


def test_count_events_by_layer():
    lines = [
        "[2024-03-11 14:22:01.123] LAYER=RRC EVENT=A",
        "[2024-03-11 14:22:01.200] LAYER=RRC EVENT=B",
        "[2024-03-11 14:22:01.456] LAYER=NAS EVENT=C",
    ]
    events = parse_log_file(lines)
    assert count_events_by_layer(events) == {"RRC": 2, "NAS": 1}


def test_count_events_by_layer_empty():
    assert count_events_by_layer([]) == {}
