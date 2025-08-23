# 45. Measuring performance and profiling

When comparing alternative implementations you should use tools that account
for microbenchmarks and interpreter overhead.  The `timeit` module provides a
simple way to time small code snippets.  The documentation notes that it
offers both a command‑line and callable interface and avoids common traps
when measuring execution time【19128105459207†L59-L63】.  It automatically selects
the appropriate high‑resolution timer for your platform and repeats the code
many times to obtain reliable results.

## Using the command‑line interface

You can invoke `timeit` as a module from the command line to compare
expressions:

```sh
python -m timeit "'-'.join(str(n) for n in range(100))"
python -m timeit "'-'.join([str(n) for n in range(100)])"
python -m timeit "'-'.join(map(str, range(100)))"
```

The output reports the best of several runs and the average time per loop【19128105459207†L65-L87】.

## Python interface

From Python code call `timeit.timeit(stmt, setup, number)` to measure the
execution time of `stmt` executed `number` times.  You can also pass a
callable instead of a string.  Use `timeit.repeat()` to run multiple
timings and return a list of results【19128105459207†L104-L119】.

```python
import timeit

def list_comp():
    return [str(n) for n in range(100)]

def list_map():
    return list(map(str, range(100)))

print(timeit.timeit(list_comp, number=10000))
print(timeit.timeit(list_map, number=10000))
```

## Profiling larger programs

For larger functions and whole programs use the `cProfile` module.  Run
`python -m cProfile myscript.py` to see time spent in each function.  The
`pstats` module can sort and format the results.  Profilers help identify
bottlenecks for optimisation.

## Summary

Use `timeit` for fine‑grained measurements and `cProfile` for coarse‑grained
profiling.  Avoid using `time.perf_counter()` directly when benchmarking as
`timeit` handles many details like disabling the garbage collector and
repeating the code sufficiently【19128105459207†L59-L63】.
