"""
Tests for ReadWriteLock. These are given -- you do not need to write tests
for this problem, just make them pass.
"""

import threading
import time

from rw_lock import ReadWriteLock


def test_multiple_readers_can_overlap():
    rwlock = ReadWriteLock()
    concurrent_readers = 0
    peak = 0
    lock = threading.Lock()
    barrier = threading.Barrier(5)

    def reader():
        nonlocal concurrent_readers, peak
        with rwlock.read_lock():
            barrier.wait(timeout=2)  # force overlap
            with lock:
                concurrent_readers += 1
                peak = max(peak, concurrent_readers)
            time.sleep(0.05)
            with lock:
                concurrent_readers -= 1

    threads = [threading.Thread(target=reader) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5)

    assert peak == 5


def test_writer_excludes_readers():
    rwlock = ReadWriteLock()
    events = []
    events_lock = threading.Lock()

    def writer():
        with rwlock.write_lock():
            with events_lock:
                events.append("writer-start")
            time.sleep(0.2)
            with events_lock:
                events.append("writer-end")

    def reader():
        time.sleep(0.05)  # ensure writer goes first
        with rwlock.read_lock():
            with events_lock:
                events.append("reader")

    wt = threading.Thread(target=writer)
    rt = threading.Thread(target=reader)
    wt.start()
    rt.start()
    wt.join(timeout=5)
    rt.join(timeout=5)

    # reader must not appear between writer-start and writer-end
    start = events.index("writer-start")
    end = events.index("writer-end")
    reader_idx = events.index("reader")
    assert not (start < reader_idx < end)


def test_reader_excludes_writer():
    rwlock = ReadWriteLock()
    events = []
    events_lock = threading.Lock()

    def reader():
        with rwlock.read_lock():
            with events_lock:
                events.append("reader-start")
            time.sleep(0.2)
            with events_lock:
                events.append("reader-end")

    def writer():
        time.sleep(0.05)
        with rwlock.write_lock():
            with events_lock:
                events.append("writer")

    rt = threading.Thread(target=reader)
    wt = threading.Thread(target=writer)
    rt.start()
    wt.start()
    rt.join(timeout=5)
    wt.join(timeout=5)

    start = events.index("reader-start")
    end = events.index("reader-end")
    writer_idx = events.index("writer")
    assert not (start < writer_idx < end)


def test_waiting_writer_not_starved_by_continuous_readers():
    rwlock = ReadWriteLock()
    stop = threading.Event()
    writer_acquired = threading.Event()

    def reader_hammer():
        while not stop.is_set():
            with rwlock.read_lock():
                time.sleep(0.01)

    reader_threads = [threading.Thread(target=reader_hammer) for _ in range(4)]
    for t in reader_threads:
        t.start()

    time.sleep(0.05)  # let readers get going

    def writer():
        with rwlock.write_lock():
            writer_acquired.set()

    wt = threading.Thread(target=writer)
    wt.start()

    acquired_in_time = writer_acquired.wait(timeout=3)

    stop.set()
    wt.join(timeout=5)
    for t in reader_threads:
        t.join(timeout=5)

    assert acquired_in_time, "writer was starved by continuous readers"
