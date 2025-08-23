"""Advanced data class features demonstration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(order=True, frozen=True, slots=True)
class Student:
    sort_index: float = field(init=False, repr=False, compare=True)
    name: str
    grades: List[int] = field(default_factory=list, repr=False, compare=False)

    def __post_init__(self) -> None:
        # compute grade average for sorting
        object.__setattr__(self, 'sort_index', sum(self.grades) / len(self.grades) if self.grades else 0.0)


def main() -> None:
    s1 = Student(name="Alice", grades=[90, 85, 92])
    s2 = Student(name="Bob", grades=[88, 91, 80])
    s3 = Student(name="Charlie", grades=[95, 100, 98])
    students = [s1, s2, s3]
    # sorted using sort_index because of order=True and compare=True on sort_index
    for s in sorted(students):
        print(f"{s.name}: average {s.sort_index:.1f}")


if __name__ == "__main__":
    main()