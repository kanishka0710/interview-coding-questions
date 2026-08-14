"""
Write your own pytest suite for SimpleThreadPool here.

See the README in this folder for the full contract. A few things worth
designing tests around (not exhaustive -- add more of your own):

  - Happy path: submit a simple function, result() returns its value.
  - A task that raises -- result() should re-raise it.
  - A task that runs past its submit()-time `timeout` -- result() should
    raise TaskTimeoutError.
  - Calling result() with a short timeout on a task that hasn't finished
    yet vs. one that has already finished.
  - Unknown task_id -- result() should raise KeyError.
  - With num_workers=1, do multiple submitted tasks run in submission
    order?
  - A raising task shouldn't take down its worker -- the next task
    submitted should still run.
  - submit() after shutdown() -- what should happen?
  - shutdown(wait=True) actually waits for in-flight tasks.

This file is deliberately not wired up with any tests yet -- that's the
point of this exercise.
"""

from thread_pool import SimpleThreadPool, TaskTimeoutError  # noqa: F401
