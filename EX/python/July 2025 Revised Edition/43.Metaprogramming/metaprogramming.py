"""
Examples illustrating metaprogramming in Python: attribute access,
operator overloading and a simple metaclass.
"""

from __future__ import annotations


class AttrDict:
    """Expose keys of an internal dictionary as attributes."""

    def __init__(self, data: dict[str, int]) -> None:
        super().__setattr__("_data", data)

    def __getattr__(self, name: str) -> int:
        if name in self._data:
            return self._data[name]
        raise AttributeError(name)

    def __setattr__(self, name: str, value: int) -> None:
        if name == "_data":
            super().__setattr__(name, value)
        else:
            self._data[name] = value


class Vector:
    """2D vector supporting addition and scalar multiplication."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Vector) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __mul__(self, scalar: float) -> Vector:
        return Vector(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"


class RegistryMeta(type):
    """Metaclass that registers subclasses in a registry."""
    registry: dict[str, type] = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        RegistryMeta.registry[name] = cls


class Base(metaclass=RegistryMeta):
    pass


class User(Base):
    pass


def main() -> None:
    # Demonstrate AttrDict
    ad = AttrDict({"a": 1, "b": 2})
    print(ad.a)  # 1
    ad.c = 3
    print(ad._data)  # {'a': 1, 'b': 2, 'c': 3}

    # Demonstrate Vector operations
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print(v1 + v2)  # Vector(4, 6)
    print(3 * v1)   # Vector(3, 6)

    # Show metaclass registry
    print(RegistryMeta.registry)


if __name__ == "__main__":
    main()