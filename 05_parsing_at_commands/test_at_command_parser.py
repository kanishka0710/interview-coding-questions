"""
Tests for the AT command response parser. These are given -- you do not
need to write tests for this problem, just make them pass.
"""

import pytest

from at_command_parser import ATResponse, parse_at_response, parse_csq


def test_bare_ok_no_info_lines():
    raw = "AT\r\r\nOK\r\n"
    resp = parse_at_response(raw)
    assert resp.command == "AT"
    assert resp.info_lines == []
    assert resp.status == "OK"
    assert resp.raw == raw


def test_csq_query_with_single_info_line():
    raw = "AT+CSQ\r\r\n+CSQ: 15,99\r\n\r\nOK\r\n"
    resp = parse_at_response(raw)
    assert resp.command == "AT+CSQ"
    assert resp.info_lines == [("+CSQ", "15,99")]
    assert resp.status == "OK"


def test_cme_error_response():
    raw = "AT+CFUN=1\r\r\n+CME ERROR: 10\r\n"
    resp = parse_at_response(raw)
    assert resp.command == "AT+CFUN=1"
    assert resp.info_lines == []
    assert resp.status == "+CME ERROR: 10"


def test_plain_error():
    raw = "AT+FOO\r\r\nERROR\r\n"
    resp = parse_at_response(raw)
    assert resp.status == "ERROR"


def test_multiple_info_lines_preserve_order():
    raw = (
        "AT+CGDCONT?\r\r\n"
        '+CGDCONT: 1,"IP","internet","0.0.0.0",0,0\r\n'
        '+CGDCONT: 2,"IP","ims","0.0.0.0",0,0\r\n'
        "\r\nOK\r\n"
    )
    resp = parse_at_response(raw)
    assert resp.command == "AT+CGDCONT?"
    assert resp.info_lines == [
        ("+CGDCONT", '1,"IP","internet","0.0.0.0",0,0'),
        ("+CGDCONT", '2,"IP","ims","0.0.0.0",0,0'),
    ]
    assert resp.status == "OK"


def test_no_echoed_command():
    raw = "+CSQ: 20,5\r\nOK\r\n"
    resp = parse_at_response(raw)
    assert resp.command is None
    assert resp.info_lines == [("+CSQ", "20,5")]
    assert resp.status == "OK"


def test_garbage_input_raises():
    with pytest.raises(ValueError):
        parse_at_response("this is not an AT response at all")


def test_empty_input_raises():
    with pytest.raises(ValueError):
        parse_at_response("")


@pytest.mark.parametrize(
    "value,expected",
    [
        ("15,99", (15, 99)),
        ("0,0", (0, 0)),
        ("99,99", (99, 99)),
        ("31,0", (31, 0)),
    ],
)
def test_parse_csq_valid(value, expected):
    assert parse_csq(value) == expected


@pytest.mark.parametrize("value", ["15", "15,20,30", "fifteen,99", "", "15,"])
def test_parse_csq_malformed_raises(value):
    with pytest.raises(ValueError):
        parse_csq(value)
