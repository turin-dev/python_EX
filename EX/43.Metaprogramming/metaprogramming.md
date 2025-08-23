# 43. Metaprogramming and special methods

Metaprogramming refers to writing code that manipulates code — either at
definition time (using class decorators or metaclasses) or at runtime.  Python
exposes hooks that allow classes to customise attribute access, arithmetic
operations and object creation.  These hooks are implemented as “special
methods” (often called dunder methods).

## Customising attribute access

The data model describes methods that intercept attribute lookup, assignment
and deletion.  Implementing `__getattr__(self, name)` allows a class to
compute attribute values on the fly when normal lookup fails【271779506080093†L1761-L1774】.
`__getattribute__(self, name)` is called unconditionally and must call the
base class implementation to avoid infinite recursion【271779506080093†L1786-L1795】.
Similarly, `__setattr__(self, name, value)` intercepts assignments and
`__delattr__(self, name)` intercepts deletions【271779506080093†L1806-L1823】.

Example: automatically returning the value of an internal dictionary when an
attribute name is not found.

```python
class AttrDict:
    def __init__(self, data: dict[str, int]) -> None:
        self._data = data

    def __getattr__(self, name: str) -> int:
        if name in self._data:
            return self._data[name]
        raise AttributeError(name)

    def __setattr__(self, name: str, value: int) -> None:
        if name == "_data":
            super().__setattr__(name, value)
        else:
            self._data[name] = value
```

## Operator overloading and numeric emulation

Special methods like `__add__`, `__sub__`, `__mul__` and friends allow classes
to emulate numeric types.  When you evaluate `x + y`, Python calls
`type(x).__add__(x, y)`; if that returns `NotImplemented`, it falls back to
reflected methods such as `__radd__`【271779506080093†L2634-L2666】.  There are
also in‑place methods like `__iadd__` for augmented assignment (`+=`)【271779506080093†L2715-L2724】.
Unimplemented operations should return `NotImplemented` so Python can try
reflected operations or raise an error.

Example: a 2D vector class that overloads `+` and `*` to add vectors and
multiply by scalars.

```python
class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__  # allow scalar * vector

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"
```

## Metaclasses

A metaclass is the “class of a class”.  Classes are instances of
metaclasses, just as objects are instances of classes.  You can customise
class creation by defining a metaclass that implements the `__new__` or
`__init__` methods.  Metaclasses are a powerful tool but rarely needed; they
are commonly used in ORMs and frameworks to register subclasses or modify
class attributes at definition time.

Example: automatically registering subclasses in a registry.

```python
class RegistryMeta(type):
    registry: dict[str, type] = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        RegistryMeta.registry[name] = cls


class Base(metaclass=RegistryMeta):
    pass


class User(Base):
    pass

print(RegistryMeta.registry)  # {'Base': <class Base>, 'User': <class User>}
```

## Summary

Python’s data model exposes hooks that allow your classes to behave like
built‑ins.  By implementing special methods you can intercept attribute access,
support operators and customise class creation.  Use these features sparingly
and document them well; subtle errors can lead to confusing behaviour.
