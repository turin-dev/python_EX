"""Examples of using concurrent.futures for asynchronous execution.

This script demonstrates how to run functions concurrently using
ThreadPoolExecutor and ProcessPoolExecutor.  It defines simple tasks and
runs them in parallel, printing the results as they complete.
"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


def slow_square(n: int) -> int:
    """Simulate a slow computation by sleeping and then squaring the input."""
    time.sleep(0.5)
    return n * n


def demo_thread_pool() -> None:
    """Run slow_square concurrently on a thread pool and print results."""
    numbers = list(range(5))
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(slow_square, n): n for n in numbers}
        for future in as_completed(futures):
            n = futures[future]
            print(f"Thread result for {n}: {future.result()}")


def demo_process_pool() -> None:
    """Run slow_square concurrently on a process pool and print results."""
    numbers = list(range(5))
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(slow_square, n): n for n in numbers}
        for future in as_completed(futures):
            n = futures[future]
            print(f"Process result for {n}: {future.result()}")


if __name__ == "__main__":
    print("Running thread pool demonstration:")
    demo_thread_pool()
    print("\nRunning process pool demonstration:")
    demo_process_pool()