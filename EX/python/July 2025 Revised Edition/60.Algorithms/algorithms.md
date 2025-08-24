# Chapter 60 – Algorithms: Heaps and Binary Search

Python’s standard library includes modules for fundamental algorithms.  The `heapq` module implements a binary heap, a priority queue data structure that allows efficient insertion and retrieval of the smallest (or largest) element.  The `bisect` module provides functions for maintaining sorted lists and performing fast binary searches.  These modules, together with tools like `itertools` which offers memory‑efficient iterator building blocks【912455807076022†L51-L99】, enable high‑performance data processing.

## Using a heap as a priority queue

A heap is a binary tree where the smallest element is always at the root.  In Python, a heap is represented as a list, and `heapq` functions maintain the heap invariant.  Key functions:

* `heapq.heappush(heap, item)` – Push a new item onto the heap.
* `heapq.heappop(heap)` – Pop and return the smallest item.  Raises `IndexError` if the heap is empty.
* `heapq.heapify(list)` – Transform an existing list into a heap in O(n) time.
* `heapq.heappushpop(heap, item)` – Push then pop in a single call for efficiency.
* `heapq.nlargest(n, iterable)` and `heapq.nsmallest(n, iterable)` – Return the `n` largest or smallest elements.

Example:

```python
import heapq

data = [5, 3, 1, 4, 2]
heapq.heapify(data)
heapq.heappush(data, 0)
while data:
    print(heapq.heappop(data))  # prints values in ascending order
```

## Maintaining sorted lists with `bisect`

The `bisect` module provides `bisect_left` and `bisect_right` to insert items into a sorted list while maintaining order.  It also offers `insort_left` and `insort_right` convenience functions that perform the insertion.  Use bisect operations to implement binary search manually or to maintain sorted sequences efficiently.

```python
import bisect

scores = [10, 20, 30, 40]
bisect.insort(scores, 25)  # insert 25 while keeping the list sorted
print(scores)  # [10, 20, 25, 30, 40]

# find insertion position for 35
pos = bisect.bisect_left(scores, 35)
print("Insert 35 at index", pos)
```

## Summary

`heapq` and `bisect` are simple yet powerful tools for working with ordered data.  Use a heap to implement priority queues and efficiently find the smallest or largest elements.  Use bisect to maintain sorted lists and perform binary searches.  Combined with other iterator tools【912455807076022†L51-L99】, they form the foundation for many algorithms.