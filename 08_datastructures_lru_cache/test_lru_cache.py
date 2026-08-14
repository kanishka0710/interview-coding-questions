"""
Tests for ThreadSafeLRUCache. These are given -- you do not need to write
tests for this problem, just make them pass.
"""

import random
import threading

import pytest

from lru_cache import ThreadSafeLRUCache


def test_basic_get_put():
    cache = ThreadSafeLRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    assert cache.get("b") == 2
    assert len(cache) == 2


def test_eviction_order_is_least_recently_used():
    cache = ThreadSafeLRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # should evict "a" (least recently used)
    assert "a" not in cache
    assert "b" in cache
    assert "c" in cache


def test_get_refreshes_recency():
    cache = ThreadSafeLRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")  # "a" is now most-recently-used
    cache.put("c", 3)  # should evict "b", not "a"
    assert "a" in cache
    assert "b" not in cache
    assert "c" in cache


def test_contains_does_not_refresh_recency():
    cache = ThreadSafeLRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert "a" in cache  # peek, should NOT count as use
    cache.put("c", 3)  # should still evict "a"
    assert "a" not in cache
    assert "b" in cache


def test_get_missing_key_raises_keyerror_without_default():
    cache = ThreadSafeLRUCache(capacity=2)
    with pytest.raises(KeyError):
        cache.get("missing")


def test_get_missing_key_returns_default():
    cache = ThreadSafeLRUCache(capacity=2)
    assert cache.get("missing", "fallback") == "fallback"


def test_put_updates_existing_key_without_growing():
    cache = ThreadSafeLRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 100)  # update, not a new entry
    assert len(cache) == 2
    assert cache.get("a") == 100


def test_concurrent_stress_no_corruption():
    capacity = 16
    cache = ThreadSafeLRUCache(capacity=capacity)
    keys = [f"key-{i}" for i in range(50)]
    stop_flag = {"stop": False}
    errors = []

    def worker():
        rng = random.Random()
        try:
            for _ in range(2000):
                key = rng.choice(keys)
                if rng.random() < 0.5:
                    cache.put(key, rng.random())
                else:
                    cache.get(key, None)
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=15)

    assert not errors
    assert len(cache) <= capacity
