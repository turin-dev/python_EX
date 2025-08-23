"""
Demonstrate advanced iterator techniques: `yield from` and itertools tools.
"""

from __future__ import annotations

import itertools
from typing import Iterable, Iterator, TypeVar

T = TypeVar("T")


def flatten(nested: Iterable[Iterable[T] | T]) -> Iterator[T]:
    """Flatten arbitrarily nested lists/tuples into a flat iterator."""
    for item in nested:
        if isinstance(item, (list, tuple)):
            # Delegate to a subgenerator
            yield from flatten(item)  # type: ignore[arg-type]
        else:
            yield item  # type: ignore[misc]


def demo_itertools() -> None:
    letters = ['A', 'B', 'C']
    print("Permutations of 2 letters:", list(itertools.permutations(letters, 2)))
    print("Combinations of 2 letters:", list(itertools.combinations(letters, 2)))
    print("Cartesian product of [1,2] and letters:", list(itertools.product([1, 2], letters)))
    # Demonstrate groupby
    data = [1, 1, 2, 2, 2, 3, 1]
    for key, group in itertools.groupby(data):
        print(key, list(group))
    # Infinite iterator examples (stop after a few values)
    from itertools import count, cycle, repeat, islice
    print("Count:", list(itertools.islice(count(10, 2), 5)))  # [10, 12, 14, 16, 18]
    print("Cycle:", list(itertools.islice(cycle('AB'), 6)))   # ['A','B','A','B','A','B']
    print("Repeat:", list(itertools.islice(repeat('X'), 3)))   # ['X','X','X']


def main() -> None:
    # Flatten nested structures
    nested = [1, [2, 3], (4, [5, 6])]
    print(list(flatten(nested)))
    # Demonstrate itertools utilities
    demo_itertools()


if __name__ == "__main__":
    main()