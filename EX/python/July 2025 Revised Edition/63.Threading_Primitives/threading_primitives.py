"""Examples of thread synchronization primitives: Lock, Condition, Event, Semaphore, Queue."""

from __future__ import annotations

import threading
import time
from queue import Queue


def lock_example() -> None:
    counter = 0
    lock = threading.Lock()

    def increment(n: int) -> None:
        nonlocal counter
        for _ in range(n):
            with lock:
                counter += 1

    threads = [threading.Thread(target=increment, args=(10_000,)) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    print("Counter value:", counter)


def condition_example() -> None:
    condition = threading.Condition()
    ready = False

    def waiter() -> None:
        nonlocal ready
        with condition:
            while not ready:
                condition.wait()
            print("Condition satisfied")

    def setter() -> None:
        nonlocal ready
        time.sleep(0.5)
        with condition:
            ready = True
            condition.notify()

    threading.Thread(target=waiter).start()
    threading.Thread(target=setter).start()


def semaphore_queue_example() -> None:
    sem = threading.Semaphore(2)
    q: Queue[int] = Queue()
    for i in range(5):
        q.put(i)

    def worker() -> None:
        while not q.empty():
            item = q.get()
            with sem:
                print(f"Working on {item}")
                time.sleep(0.1)
            q.task_done()

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()


if __name__ == "__main__":
    lock_example()
    condition_example()
    semaphore_queue_example()