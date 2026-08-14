# Weak-Reference Event Bus (Avoiding Subscriber Leaks)

## Context

Test equipment driver classes (signal generator, spectrum analyzer, cellular network
simulator) publish events — `"measurement_ready"`, `"link_down"`, etc. — to
subscriber callbacks, which are very often *bound methods* of a test-case object
(`self.on_measurement`). A regression run executes thousands of test cases in a
single process. If the event bus's subscription table holds **strong** references to
those callbacks, every test-case object that ever subscribed stays alive for the
lifetime of the process — even long after its test finished — because the bus is
still holding a reference into it. Over thousands of test cases, that's a real
memory leak.

The fix is to have the event bus hold only **weak** references to subscribers, so a
finished test-case object (and its bound methods) can be garbage-collected normally
without anyone having to remember to call `unsubscribe()`.

## Problem

Implement `EventBus` in `weakref_pubsub.py`.

### Contract

- `EventBus()`
- `subscribe(event_name: str, callback: Callable) -> None` — stores a **weak**
  reference to `callback`. `callback` may be a plain function, a lambda kept alive
  by the caller, or a bound method. **Bound methods need special handling**: the
  bound-method object itself (`obj.method`) is created fresh on each attribute
  access and immediately eligible for collection, so a plain `weakref.ref` on it
  won't behave the way you want — look at `weakref.WeakMethod`.
- `publish(event_name: str, *args, **kwargs) -> int` — calls every still-alive
  subscriber for `event_name` with `(*args, **kwargs)`, and returns the count of
  callbacks actually invoked. Subscribers whose weak reference has died must be
  silently skipped **and purged** from internal storage (not just skipped on this
  call and left to accumulate forever).
- `unsubscribe(event_name: str, callback: Callable) -> None` — explicit removal, for
  the case where a caller does want to opt out early. Should be a no-op (not raise)
  if `callback` wasn't subscribed.
- `subscriber_count(event_name: str) -> int` — returns the number of currently
  live, non-purged subscriptions for `event_name`. This exists so tests (and you)
  can verify dead references actually get cleaned out of internal storage, not just
  skipped at publish time.

### Edge cases the tests check

- A plain function subscriber receives published events.
- A bound method subscriber receives published events.
- After the object owning a subscribed bound method is deleted and garbage
  collected, `publish()` no longer calls it, and `subscriber_count()` drops
  accordingly (i.e., the dead entry was actually purged, not just skipped).
- Multiple subscribers to the same event: one dying doesn't stop the others from
  being called.
- `unsubscribe()` on a callback that was never subscribed doesn't raise.

## Running

```
uv run pytest 11_memory_weakref_pubsub -v
```
