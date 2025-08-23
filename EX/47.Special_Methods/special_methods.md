# 47. Special methods and operator overloading

Python classes can implement “magic” methods to integrate with language
features.  These methods are identified by double underscores at the
beginning and end of the name (e.g., `__len__`, `__getitem__`).  The data
model specifies special methods for numeric operations, container emulation
and conversions.  Defining these methods allows your objects to behave like
built‑in types.  The documentation notes that methods like
`__add__`, `__sub__`, `__mul__` and others are called to implement
arithmetic operations and that Python calls `type(x).__add__(x, y)` to
evaluate `x + y`【271779506080093†L2634-L2666】.  Reflected and in‑place variants
(`__radd__`, `__iadd__`, etc.) support swapped operands and augmented
assignment【271779506080093†L2667-L2724】.

## Container protocol methods

To make an object behave like a sequence you can implement:

- `__len__(self)`: return the number of elements.
- `__getitem__(self, index)`: return the element at a given index.
- `__setitem__(self, index, value)`: assign a value at an index (for mutable
  sequences).
- `__iter__(self)`: return an iterator over elements.  Alternatively define
  `__getitem__` with integer indices starting at 0 and Python will iterate
  until an `IndexError` is raised.

Example: a simple range‑like object.

```python
class MyRange:
    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.start = start
        self.stop = stop
        self.step = step

    def __len__(self) -> int:
        return max(0, (self.stop - self.start + self.step - 1) // self.step)

    def __getitem__(self, index: int) -> int:
        value = self.start + index * self.step
        if (self.step > 0 and value >= self.stop) or (self.step < 0 and value <= self.stop):
            raise IndexError
        return value

    def __iter__(self):
        i = 0
        while True:
            try:
                yield self[i]
                i += 1
            except IndexError:
                return
```

## Conversion and representation

Implement `__str__` for a human‑readable representation and `__repr__` for a
developer‑oriented string that could recreate the object.  Define
`__int__`, `__float__` or `__bool__` to allow your object to be used in
contexts expecting those types.

## Comparisons

`__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__` implement equality and
ordering.  Python falls back to reflected comparison methods when appropriate.
The `functools.total_ordering` decorator can fill in missing methods based on
one or two.

## Summary

Special methods are the glue between your classes and Python’s syntax.  By
defining them thoughtfully you can make custom objects intuitive and
compatible with the language’s built‑in features【271779506080093†L2634-L2666】.
