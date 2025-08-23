"""Performance measurement using timeit, cProfile and pstats."""

from __future__ import annotations

import timeit
import cProfile
import pstats


def benchmark_sort(n: int = 1000) -> float:
    code = "sorted(range(%d), reverse=True)" % n
    return timeit.timeit(code, number=1000)


def profile_fibonacci(n: int) -> None:
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def fib(k: int) -> int:
        return k if k < 2 else fib(k - 1) + fib(k - 2)

    profiler = cProfile.Profile()
    profiler.enable()
    fib(n)
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative').print_stats(5)


if __name__ == "__main__":
    duration = benchmark_sort(1000)
    print(f"Sorting benchmark took {duration:.4f} seconds")
    print("Profiling fibonacci(20):")
    profile_fibonacci(20)