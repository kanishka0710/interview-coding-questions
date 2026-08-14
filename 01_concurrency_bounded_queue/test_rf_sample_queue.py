"""
Tests for BoundedSampleQueue. These are given -- you do not need to write
tests for this problem, just make them pass.
"""

import threading
import time
from collections import Counter

import pytest

from rf_sample_queue import SENTINEL, BoundedSampleQueue, QueueTimeout


def test_basic_fifo_order():
    q = BoundedSampleQueue(capacity=3)
    q.put(1)
    q.put(2)
    q.put(3)
    assert q.get() == 1
    assert q.get() == 2
    assert q.get() == 3


def test_size_and_predicates():
    q = BoundedSampleQueue(capacity=2)
    assert q.is_empty()
    assert not q.is_full()
    q.put("a")
    assert q.size() == 1
    q.put("b")
    assert q.is_full()
    assert q.size() == 2


def test_put_times_out_when_full_and_no_consumer():
    q = BoundedSampleQueue(capacity=1)
    q.put("x")
    with pytest.raises(QueueTimeout):
        q.put("y", timeout=0.2)


def test_get_times_out_when_empty():
    q = BoundedSampleQueue(capacity=1)
    with pytest.raises(QueueTimeout):
        q.get(timeout=0.2)


def test_put_unblocks_once_space_freed():
    q = BoundedSampleQueue(capacity=1)
    q.put("first")
    results = []

    def producer():
        q.put("second", timeout=2)
        results.append("put-ok")

    t = threading.Thread(target=producer)
    t.start()
    time.sleep(0.1)
    assert q.get() == "first"
    t.join(timeout=2)
    assert results == ["put-ok"]
    assert q.get() == "second"


def test_close_wakes_blocked_getter_when_drained():
    q = BoundedSampleQueue(capacity=1)
    result = {}

    def consumer():
        result["value"] = q.get(timeout=2)

    t = threading.Thread(target=consumer)
    t.start()
    time.sleep(0.1)
    q.close()
    t.join(timeout=2)
    assert result.get("value") is SENTINEL


def test_multi_producer_multi_consumer_no_loss_or_duplication():
    q = BoundedSampleQueue(capacity=8)
    num_producers = 4
    items_per_producer = 200
    consumed = []
    consumed_lock = threading.Lock()

    def producer(pid):
        for i in range(items_per_producer):
            q.put((pid, i), timeout=5)

    def consumer():
        while True:
            item = q.get(timeout=5)
            if item is SENTINEL:
                return
            with consumed_lock:
                consumed.append(item)

    producers = [threading.Thread(target=producer, args=(pid,)) for pid in range(num_producers)]
    consumers = [threading.Thread(target=consumer) for _ in range(4)]

    for t in consumers:
        t.start()
    for t in producers:
        t.start()
    for t in producers:
        t.join(timeout=10)

    q.close()

    for t in consumers:
        t.join(timeout=10)

    expected = Counter((pid, i) for pid in range(num_producers) for i in range(items_per_producer))
    assert Counter(consumed) == expected
