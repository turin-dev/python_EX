"""
Examples of advanced structural pattern matching introduced in Python 3.10.
"""

from __future__ import annotations

from dataclasses import dataclass


def process_command(command: str) -> None:
    match command.split():
        case ["quit"]:
            print("Goodbye!")
        case ["go", direction]:
            print(f"Going {direction}")
        case [action, obj]:
            print(f"{action}ing {obj}")
        case _:
            print("Unknown command")


def classify_number(x: int) -> str:
    match x:
        case 0 | 1:
            return "small"
        case 2 | 3 | 5 | 7:
            return "prime"
        case _:
            return "other"


@dataclass
class Point:
    x: int
    y: int
    __match_args__ = ("x", "y")


def describe_point(p: Point) -> str:
    match p:
        case Point(0, 0):
            return "origin"
        case Point(x, y) if x == y:
            return "diagonal"
        case Point(x, y):
            return f"{x}, {y}"
        case _:
            return "unknown"


def main() -> None:
    for cmd in ["quit", "go north", "eat apple", "hello"]:
        process_command(cmd)
    for n in range(6):
        print(n, classify_number(n))
    for p in [Point(0, 0), Point(1, 1), Point(2, 3)]:
        print(p, "->", describe_point(p))


if __name__ == "__main__":
    main()