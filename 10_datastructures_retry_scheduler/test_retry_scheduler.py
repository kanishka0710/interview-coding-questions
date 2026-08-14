"""
Write your own pytest suite for RetryScheduler here.

See the README in this folder for the full contract. Bring your own fake
clock (see problem 2, 02_concurrency_rate_limiter/test_rate_limiter.py, for
the pattern -- a small callable class with an .advance() method, injected
as time_fn).

Things worth designing tests around (not exhaustive -- add more of your
own):

  - Basic schedule() + pop_due(): nothing due before its time, due exactly
    at/after its time.
  - Rescheduling the same step_id before it's due -- pop_due() must never
    emit it twice, and must use the *new* due time, not the old one.
  - len() staying accurate through several reschedules of the same
    step_id(s).
  - Multiple distinct step_ids due at the same time -- each poppable
    exactly once.
  - peek_next_due_time() reflecting the earliest *active* entry, not a
    stale one left behind by a reschedule.
  - pop_due() returning None repeatedly when nothing is due, then
    returning correctly once something becomes due.

This file is deliberately not wired up with any tests yet -- that's the
point of this exercise.
"""

from retry_scheduler import RetryScheduler  # noqa: F401
