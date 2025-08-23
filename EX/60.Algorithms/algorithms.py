"""Demonstrate heaps and binary search using heapq and bisect."""

from __future__ import annotations

import bisect
import heapq


def demo_heapq() -> None:
    """Show how to use heapq to implement a priority queue."""
    tasks = []  # the heap
    # push items as (priority, task) tuples
    heapq.heappush(tasks, (2, "write code"))
    heapq.heappush(tasks, (1, "release product"))
    heapq.heappush(tasks, (3, "sleep"))
    print("Priority queue order:")
    while tasks:
        priority, task = heapq.heappop(tasks)
        print(priority, task)


def demo_bisect() -> None:
    """Show how to maintain a sorted list using bisect and insort."""
    sorted_list = [10, 20, 30, 50]
    bisect.insort(sorted_list, 40)
    bisect.insort(sorted_list, 25)
    print("Sorted list after insertions:", sorted_list)
    # use bisect to find index where a value should be inserted
    for value in (15, 35, 60):
        idx = bisect.bisect_left(sorted_list, value)
        print(f"{value} should be inserted at index {idx}")


if __name__ == "__main__":
    demo_heapq()
    print()
    demo_bisect()