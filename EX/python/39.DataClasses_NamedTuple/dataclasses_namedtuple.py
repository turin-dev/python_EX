"""Demonstrations of dataclasses and namedtuple for structured data.

This script compares dataclasses to namedtuple and shows how to use them.
"""
from dataclasses import dataclass, field
from typing import List
from collections import namedtuple


@dataclass(order=True)
class Student:
    """Data class representing a student with ordering based on grade."""

    sort_index: float = field(init=False, repr=False)
    name: str
    grade: float
    courses: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Use negative grade for descending sort order
        self.sort_index = -self.grade


def demo_dataclass() -> None:
    """Create and sort dataclass instances."""
    students = [
        Student(name="Alice", grade=85.5, courses=["math", "history"]),
        Student(name="Bob", grade=92.0),
        Student(name="Charlie", grade=78.0, courses=["science"]),
    ]
    # dataclass with order=True allows sorting
    for student in sorted(students):
        print(student)


def demo_namedtuple() -> None:
    """Use a namedtuple for lightweight immutable records."""
    Point = namedtuple("Point", ["x", "y", "z"])
    p1 = Point(1, 2, 3)
    p2 = Point(4, 5, 6)
    print(f"p1: {p1}, x coordinate: {p1.x}")
    # Namedtuples are immutable; attempting to assign raises AttributeError
    try:
        p1.x = 10  # type: ignore[assignment]
    except AttributeError as e:
        print("Expected error:", e)


if __name__ == "__main__":
    print("Dataclass demonstration:")
    demo_dataclass()
    print("\nNamedtuple demonstration:")
    demo_namedtuple()