# Chapter 59 – Memory Management and Profiling

Understanding memory usage helps you write efficient programs and detect leaks.  Python manages memory automatically through reference counting and a cyclic garbage collector.  The `gc` module exposes functions to interact with the garbage collector; you can disable automatic collection, trigger a collection manually, and set debugging options【721861822603243†L49-L57】.  For fine‑grained memory tracking, the `tracemalloc` module records allocation traces and lets you inspect the current and peak memory usage of code blocks.

## Garbage collection

Besides reference counting, Python uses a generational garbage collector to detect and free cyclic references.  Use `gc.collect()` to force an immediate collection and `gc.get_count()` to see the number of objects tracked in each generation.  You can enable or disable automatic collection with `gc.enable()` and `gc.disable()` and adjust thresholds via `gc.get_threshold()` and `gc.set_threshold()`【721861822603243†L49-L57】.

```python
import gc

# Disable automatic GC
gc.disable()
print("GC enabled?", gc.isenabled())

# Force a collection and inspect statistics
unreachable = gc.collect()
print("Unreachable objects collected:", unreachable)
print("Objects in generations:", gc.get_count())
print("Thresholds:", gc.get_threshold())

# Re‑enable GC
gc.enable()
```

## Tracking memory with `tracemalloc`

`tracemalloc` records memory allocations so you can identify where objects are created.  Start tracking with `tracemalloc.start()`; call `take_snapshot()` to capture the current allocations and `compare_to()` to see differences between snapshots.  Use `snapshot.statistics('lineno')` to see which lines allocate the most memory.  This is helpful for profiling memory leaks.

```python
import tracemalloc

def allocate(n):
    # create many small objects
    return [str(i) for i in range(n)]

tracemalloc.start()
allocate(100_000)
snapshot = tracemalloc.take_snapshot()

top = snapshot.statistics('lineno')[:5]
for stat in top:
    print(stat)
tracemalloc.stop()
```

## Summary

Use the `gc` module to control the garbage collector and inspect object counts【721861822603243†L49-L57】.  For detailed memory profiling, use `tracemalloc` to track allocations and compare snapshots.  Understanding memory usage helps diagnose leaks and optimize performance.