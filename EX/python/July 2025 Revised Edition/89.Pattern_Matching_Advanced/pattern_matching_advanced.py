"""Advanced pattern matching examples using match/case."""

from __future__ import annotations


def classify_value(x: int | float) -> str:
    match x:
        case 0 | 1:
            return "unit"
        case n if n < 0:
            return "negative"
        case n if n > 100:
            return "large"
        case _:
            return "other"


def match_sequence(seq: list[int]) -> str:
    match seq:
        case []:
            return "empty"
        case [x]:
            return f"single {x}"
        case [x, y]:
            return f"pair {x}, {y}"
        case [1, *rest]:
            return f"starts with 1; rest={rest}"
        case _:
            return "many"


class Point:
    __match_args__ = ("x", "y")
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


def describe_point(p: Point) -> str:
    match p:
        case Point(x, y) if x == y:
            return "diagonal"
        case Point(x, y):
            return f"point({x},{y})"


if __name__ == "__main__":
    print(classify_value(0), classify_value(-5), classify_value(150))
    print(match_sequence([]))
    print(match_sequence([42]))
    print(match_sequence([1, 2, 3]))
    p1 = Point(3, 3)
    p2 = Point(2, 5)
    print(describe_point(p1))
    print(describe_point(p2))