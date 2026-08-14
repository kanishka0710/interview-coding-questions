"""
Tests for ObjectPool. These are given -- you do not need to write tests
for this problem, just make them pass.
"""

import threading
import time

import pytest

from object_pool import ObjectPool, PoolTimeoutError


class FakeConnection:
    _next_id = 0

    def __init__(self):
        FakeConnection._next_id += 1
        self.id = FakeConnection._next_id
        self.closed = False

    def close(self):
        self.closed = True


@pytest.fixture(autouse=True)
def _reset_id_counter():
    FakeConnection._next_id = 0
    yield


def test_acquire_up_to_max_size_returns_distinct_handles():
    pool = ObjectPool(factory=FakeConnection, max_size=3)
    handles = []
    cms = [pool.acquire(timeout=1) for _ in range(3)]
    for cm in cms:
        handles.append(cm.__enter__())

    assert len({h.id for h in handles}) == 3

    for cm in cms:
        cm.__exit__(None, None, None)


def test_exceeding_max_size_blocks_then_succeeds_on_release():
    pool = ObjectPool(factory=FakeConnection, max_size=1)
    order = []

    cm1 = pool.acquire(timeout=2)
    h1 = cm1.__enter__()
    order.append(("acquired", h1.id))

    result = {}

    def waiter():
        with pool.acquire(timeout=2) as h2:
            result["id"] = h2.id
            order.append(("acquired", h2.id))

    t = threading.Thread(target=waiter)
    t.start()
    time.sleep(0.1)
    assert "id" not in result  # still blocked, pool exhausted

    cm1.__exit__(None, None, None)
    t.join(timeout=5)

    assert result["id"] == h1.id  # reused the released handle


def test_exhausted_pool_times_out():
    pool = ObjectPool(factory=FakeConnection, max_size=1)
    cm = pool.acquire(timeout=1)
    cm.__enter__()

    with pytest.raises(PoolTimeoutError):
        with pool.acquire(timeout=0.2):
            pass

    cm.__exit__(None, None, None)


def test_released_handle_is_reused_not_recreated():
    pool = ObjectPool(factory=FakeConnection, max_size=1)

    with pool.acquire(timeout=1) as h1:
        first_id = h1.id

    with pool.acquire(timeout=1) as h2:
        assert h2.id == first_id


def test_exception_in_with_block_still_returns_handle():
    pool = ObjectPool(factory=FakeConnection, max_size=1)

    with pytest.raises(RuntimeError):
        with pool.acquire(timeout=1) as h1:
            first_id = h1.id
            raise RuntimeError("boom")

    # pool must not be permanently exhausted by the exception
    with pool.acquire(timeout=0.5) as h2:
        assert h2.id == first_id


def test_close_closes_idle_handles():
    pool = ObjectPool(factory=FakeConnection, max_size=2)

    with pool.acquire(timeout=1) as h1:
        pass
    with pool.acquire(timeout=1) as h2:
        pass

    pool.close()

    assert h1.closed
    assert h2.closed
