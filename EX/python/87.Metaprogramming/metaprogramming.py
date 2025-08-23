"""Examples of descriptors and metaclasses in Python."""

from __future__ import annotations


# Descriptor example
class PositiveNumber:
    def __init__(self) -> None:
        self._name = None

    def __set_name__(self, owner, name) -> None:
        self._name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Value must be non‑negative")
        setattr(instance, self._name, value)


class Account:
    balance = PositiveNumber()
    def __init__(self, balance: float) -> None:
        self.balance = balance


# Metaclass example
class AutoReprMeta(type):
    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        # add a __repr__ method if not defined
        if '__repr__' not in namespace:
            def __repr__(self) -> str:
                attrs = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items())
                return f"{name}({attrs})"
            cls.__repr__ = __repr__  # type: ignore
        return cls


class Person(metaclass=AutoReprMeta):
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


if __name__ == "__main__":
    acc = Account(100.0)
    print("Initial balance:", acc.balance)
    try:
        acc.balance = -10  # should raise ValueError
    except ValueError as e:
        print("Caught error:", e)
    # metaclass auto repr
    p = Person("Jane", 30)
    print("Person representation:", p)