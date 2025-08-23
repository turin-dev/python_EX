"""Advanced functional programming examples using itertools and functools."""

from __future__ import annotations

import itertools
from functools import singledispatch, partial, total_ordering


def demo_combinatorics() -> None:
    data = ["a", "b", "c"]
    print("Permutations of 2:", list(itertools.permutations(data, 2)))
    print("Combinations of 2:", list(itertools.combinations(data, 2)))
    print("Product of [1,2] and ['x','y']:", list(itertools.product([1, 2], ['x', 'y'])))


@singledispatch
def to_string(obj) -> str:
    raise NotImplementedError


@to_string.register
def _(obj: int) -> str:
    return f"int:{obj}"


@to_string.register
def _(obj: list) -> str:
    return f"list:{','.join(map(str, obj))}"


@total_ordering
class Item:
    def __init__(self, weight: int, value: int) -> None:
        self.weight = weight
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return (self.value / self.weight) == (other.value / other.weight)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return (self.value / self.weight) < (other.value / other.weight)


def demo_partial() -> None:
    def power(base: int, exp: int) -> int:
        return base ** exp
    square = partial(power, exp=2)
    print("Square of 5:", square(5))


def demo_generic() -> None:
    print(to_string(10))
    print(to_string([1, 2, 3]))


if __name__ == "__main__":
    demo_combinatorics()
    demo_generic()
    items = [Item(2, 10), Item(3, 12), Item(1, 5)]
    print("Items sorted by value density:")
    for item in sorted(items):
        print(item.weight, item.value)
    demo_partial()