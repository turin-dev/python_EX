"""Memory management and profiling examples using gc and tracemalloc."""

from __future__ import annotations

import gc
import tracemalloc


def show_gc_info() -> None:
    """Print information about the garbage collector."""
    print("GC enabled:", gc.isenabled())
    counts = gc.get_count()
    print("Objects in generations:", counts)
    print("Collection thresholds:", gc.get_threshold())
    unreachable = gc.collect()
    print("Unreachable objects collected:", unreachable)


def memory_profile_example() -> None:
    """Use tracemalloc to identify lines allocating the most memory."""
    def allocate_strings(n: int) -> list[str]:
        return [f"str_{i}" for i in range(n)]

    tracemalloc.start()
    # allocate a large number of strings
    allocate_strings(200_000)
    snapshot = tracemalloc.take_snapshot()
    # show top 3 lines responsible for allocations
    top_stats = snapshot.statistics("lineno")[:3]
    print("Top memory allocations:")
    for stat in top_stats:
        print(stat)
    tracemalloc.stop()


if __name__ == "__main__":
    print("Garbage collector info:")
    show_gc_info()
    print("\nMemory profiling:")
    memory_profile_example()