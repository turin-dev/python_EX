# 44. Garbage collection and memory management

Python primarily uses reference counting to manage memory.  When an
object’s reference count drops to zero it is immediately freed.  However,
reference cycles (where two objects reference each other) can prevent
reference counts from reaching zero.  To reclaim cyclical garbage, CPython
includes an optional generational garbage collector.

The `gc` module provides an interface to this collector.  It can disable
automatic collection, adjust collection thresholds and return statistics.
According to the documentation, the module lets you “disable the collector,
tune the collection frequency, and set debugging options”【721861822603243†L49-L57】.
You can also inspect unreachable objects that cannot be freed【721861822603243†L49-L57】.

## Key functions

- `gc.enable()` and `gc.disable()` control whether the collector runs
  automatically【721861822603243†L49-L67】.
- `gc.isenabled()` returns `True` if the collector is active【721861822603243†L69-L71】.
- `gc.collect(generation=0|1|2)` runs a garbage collection pass and returns the
  number of collected and uncollectable objects【721861822603243†L73-L79】.
- `gc.get_stats()` returns statistics about collections and uncollectable
  objects【721861822603243†L108-L119】.
- `gc.set_debug(flags)` enables debugging messages; use `gc.DEBUG_LEAK` to find
  objects that are not freed【721861822603243†L54-L57】.

## Example: Detecting reference cycles

```python
import gc

class Node:
    def __init__(self) -> None:
        self.other = None


def create_cycle() -> None:
    a = Node()
    b = Node()
    a.other = b
    b.other = a

create_cycle()

# Force a collection and report before/after counts
print("GC enabled?", gc.isenabled())
print("Collecting…", gc.collect())
print("Garbage:", gc.garbage)
```

In the example above a cycle of two `Node` objects is created.  The garbage
collector detects the cycle and frees the objects when `gc.collect()` is
called.  If you disable the collector with `gc.disable()`, cycles will
persist until you re‑enable the collector or call `gc.collect()` manually.

## Tuning the collector

The collector categorises objects into three generations (0, 1 and 2).  Each
generation has a threshold that determines when collection runs【721861822603243†L124-L139】.
Call `gc.get_threshold()` and `gc.set_threshold(threshold0, threshold1,
threshold2)` to view or change these values.  A lower threshold results in
more frequent collections.

## Summary

Understanding how Python reclaims memory helps you write efficient
programs.  The `gc` module exposes functions to control and observe the
garbage collector, making it easier to debug memory leaks and tune collection
behaviour【721861822603243†L49-L57】.
