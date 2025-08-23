# 46. Advanced iterators and generator techniques

Python’s iterator protocol makes it easy to create custom iterable objects.
Generators (functions that use `yield`) let you write lazy iterators without
building an entire class.  The `itertools` module extends these primitives
with fast, memory‑efficient building blocks that can be combined to process
streaming data.  The documentation describes `itertools` as an “iterator
algebra” that is memory efficient【912455807076022†L51-L99】.

## Delegating to subgenerators with `yield from`

The `yield from <iterable>` syntax, introduced in PEP 380, lets a generator
delegate part of its operations to a subgenerator or any iterable.  It
automatically forwards values sent to the delegating generator and returns the
subgenerator’s return value.  This simplifies generator composition.

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

print(list(flatten([1, [2, 3], (4, 5)])))  # [1, 2, 3, 4, 5]
```

## Useful tools from `itertools`

- **Combinatorics:** `itertools.permutations(iterable, r)`,
  `combinations(iterable, r)` and `product(*iterables)` generate permutations,
  combinations and Cartesian products.
- **Slicing and duplication:** `islice(iterable, stop)` slices an iterator;
  `tee(iterable, n)` creates multiple independent iterators from one.
- **Grouping:** `groupby(iterable, key)` groups consecutive elements with the
  same key.
- **Infinite iterators:** `count(start, step)` produces evenly spaced numbers;
  `cycle(iterable)` repeats an iterable indefinitely; `repeat(elem, n)` yields
  `elem` n times or forever.
- **Accumulation:** `accumulate(iterable, func)` yields running totals or other
  binary reductions.

## Asynchronous generators and `yield from` equivalents

In asynchronous code `async def` defines a coroutine.  You can use
`async for` to iterate over asynchronous iterators and `async with` for
asynchronous context managers.  Asynchronous generators use `async def` with
`yield` and may delegate to sub‑generators with `yield from` replaced by
`yield from` in synchronous contexts; in asynchronous contexts use `async for`.

## Example: Using `itertools` combinatorics

```python
import itertools

letters = ['A', 'B', 'C']
print(list(itertools.permutations(letters, 2)))  # [('A', 'B'), ('A', 'C'), ...]
print(list(itertools.combinations(letters, 2)))  # [('A', 'B'), ('A', 'C'), ('B', 'C')]
print(list(itertools.product([1, 2], letters)))   # [(1, 'A'), (1, 'B'), ...]
```

## Summary

Advanced iterators and generator patterns make it possible to create powerful
data pipelines and composable iteration logic.  The functions in the
`itertools` module are implemented in C for speed and minimise memory usage
because they generate values on demand【912455807076022†L51-L99】.
