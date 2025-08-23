"""
Compare the performance of different ways to build a list of strings.

This script uses the timeit module to measure the execution time of
list comprehensions versus map functions.  It also demonstrates basic
profiling with cProfile when run as a script.
"""

import timeit
import cProfile
from functools import partial


def list_comp() -> list[str]:
    return [str(n) for n in range(1000)]


def list_map() -> list[str]:
    return list(map(str, range(1000)))


def measure() -> None:
    comp_time = timeit.timeit(list_comp, number=5000)
    map_time = timeit.timeit(list_map, number=5000)
    print(f"List comprehension: {comp_time:.4f}s")
    print(f"Map function:       {map_time:.4f}s")


if __name__ == "__main__":
    # Benchmark using timeit
    measure()
    # Profile the functions using cProfile
    print("\nProfiling list_comp...")
    cProfile.runctx("list_comp()", globals(), locals())
    print("\nProfiling list_map...")
    cProfile.runctx("list_map()", globals(), locals())