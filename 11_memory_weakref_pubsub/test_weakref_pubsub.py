"""
Tests for EventBus. These are given -- you do not need to write tests for
this problem, just make them pass.
"""

import gc

from weakref_pubsub import EventBus


def test_plain_function_subscriber_is_called():
    bus = EventBus()
    received = []

    def handler(value):
        received.append(value)

    bus.subscribe("measurement_ready", handler)
    count = bus.publish("measurement_ready", 42)

    assert received == [42]
    assert count == 1


class _Recorder:
    def __init__(self):
        self.received = []

    def on_event(self, value):
        self.received.append(value)


def test_bound_method_subscriber_is_called():
    bus = EventBus()
    recorder = _Recorder()

    bus.subscribe("link_down", recorder.on_event)
    count = bus.publish("link_down", "reason=timeout")

    assert recorder.received == ["reason=timeout"]
    assert count == 1


def test_dead_bound_method_subscriber_is_purged_not_called():
    bus = EventBus()
    recorder = _Recorder()
    bus.subscribe("link_down", recorder.on_event)
    assert bus.subscriber_count("link_down") == 1

    del recorder
    gc.collect()

    count = bus.publish("link_down", "reason=timeout")
    assert count == 0
    assert bus.subscriber_count("link_down") == 0


def test_one_dead_subscriber_does_not_block_others():
    bus = EventBus()
    live_received = []

    class Owner:
        def __init__(self):
            self.received = []

        def on_event(self, value):
            self.received.append(value)

    dying = Owner()
    bus.subscribe("event", dying.on_event)

    def live_handler(value):
        live_received.append(value)

    bus.subscribe("event", live_handler)

    del dying
    gc.collect()

    count = bus.publish("event", "x")
    assert count == 1
    assert live_received == ["x"]


def test_unsubscribe_removes_callback():
    bus = EventBus()
    received = []

    def handler(value):
        received.append(value)

    bus.subscribe("event", handler)
    bus.unsubscribe("event", handler)

    count = bus.publish("event", "x")
    assert count == 0
    assert received == []


def test_unsubscribe_unknown_callback_does_not_raise():
    bus = EventBus()

    def handler(value):
        pass

    bus.unsubscribe("event", handler)  # never subscribed -- should not raise


def test_subscriber_count_unknown_event_is_zero():
    bus = EventBus()
    assert bus.subscriber_count("nonexistent") == 0
