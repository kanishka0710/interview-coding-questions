"""
Tests for RingBuffer. These are given -- you do not need to write tests
for this problem, just make them pass.
"""

import pytest

from ring_buffer import RingBuffer


def test_empty_buffer():
    buf = RingBuffer(capacity=3)
    assert len(buf) == 0
    assert buf.to_list() == []
    with pytest.raises(IndexError):
        buf[0]


def test_append_below_capacity():
    buf = RingBuffer(capacity=5)
    buf.append("a")
    buf.append("b")
    assert len(buf) == 2
    assert buf.to_list() == ["a", "b"]
    assert buf[0] == "a"
    assert buf[1] == "b"
    assert buf[-1] == "b"
    assert buf[-2] == "a"


def test_append_beyond_capacity_drops_oldest():
    buf = RingBuffer(capacity=3)
    for x in ["a", "b", "c", "d"]:
        buf.append(x)
    assert len(buf) == 3
    assert buf.to_list() == ["b", "c", "d"]


def test_multiple_wraparounds_preserve_order():
    buf = RingBuffer(capacity=4)
    for i in range(37):  # well beyond capacity, wraps many times
        buf.append(i)
    assert len(buf) == 4
    assert buf.to_list() == [33, 34, 35, 36]
    assert buf[0] == 33
    assert buf[-1] == 36


def test_capacity_attribute():
    buf = RingBuffer(capacity=7)
    assert buf.capacity == 7


def test_index_error_out_of_range():
    buf = RingBuffer(capacity=3)
    buf.append("a")
    buf.append("b")
    with pytest.raises(IndexError):
        buf[2]
    with pytest.raises(IndexError):
        buf[-3]


def test_to_list_is_independent_copy():
    buf = RingBuffer(capacity=3)
    buf.append("a")
    buf.append("b")
    snapshot = buf.to_list()
    snapshot.append("mutated")
    assert buf.to_list() == ["a", "b"]


def test_invalid_capacity_raises():
    with pytest.raises(ValueError):
        RingBuffer(capacity=0)
    with pytest.raises(ValueError):
        RingBuffer(capacity=-1)
