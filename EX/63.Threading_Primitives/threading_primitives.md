# Chapter 63 – Thread Synchronization Primitives

Python’s `threading` module provides tools for running code concurrently in threads.  While threads run in the same process and share memory, they must be coordinated to prevent race conditions.  The `threading` module offers a variety of synchronization primitives—locks, reentrant locks, conditions, semaphores and events—to coordinate access to shared resources.  The documentation notes that the GIL prevents multiple threads from executing Python bytecode simultaneously, so threading is most useful for I/O‑bound tasks【570737854010064†L77-L150】.

## Locks and reentrant locks

* **`Lock`** – A basic mutual exclusion lock.  Acquire it before accessing shared state and release it when done.  Attempting to acquire a locked `Lock` blocks until it becomes available.
* **`RLock`** – A reentrant lock that can be acquired multiple times by the same thread without deadlocking.  Useful for recursive functions.

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print("Final counter:", counter)
```

## Conditions and events

A `Condition` variable allows one or more threads to wait until notified.  Use it with a lock to coordinate producers and consumers.  An `Event` represents a boolean flag that threads can wait on and set; when set, all waiting threads unblock.

```python
import threading

condition = threading.Condition()
ready = False

def worker():
    with condition:
        while not ready:
            condition.wait()
        print("Worker proceeding")

def notifier():
    global ready
    with condition:
        ready = True
        condition.notify_all()

threading.Thread(target=worker).start()
threading.Thread(target=notifier).start()
```

## Semaphores and queues

Semaphores limit the number of concurrent accesses to a resource.  Use `BoundedSemaphore` for a semaphore with a maximum value.  The `queue` module provides thread‑safe FIFO, LIFO and priority queues for communicating between threads.

```python
import threading
from queue import Queue

sem = threading.Semaphore(2)  # allow at most 2 workers concurrently
work_queue: Queue[int] = Queue()

def do_work(item: int) -> None:
    with sem:
        print("Processing", item)

for i in range(5):
    work_queue.put(i)

threads = [threading.Thread(target=do_work, args=(work_queue.get(),)) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()
```

## Summary

Use locks to protect shared state, conditions and events for complex coordination, semaphores to limit concurrency, and `queue.Queue` for thread‑safe communication between producer and consumer threads.  Keep in mind that due to the GIL, Python threads are best suited to I/O‑bound tasks【570737854010064†L77-L150】.