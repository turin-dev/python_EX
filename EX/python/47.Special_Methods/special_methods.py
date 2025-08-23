"""
Demonstrate special methods for container emulation and arithmetic.
"""

from __future__ import annotations


class MyRange:
    """A custom range that supports len(), indexing and iteration."""

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.start = start
        self.stop = stop
        self.step = step

    def __len__(self) -> int:
        if self.step > 0:
            return max(0, (self.stop - self.start + self.step - 1) // self.step)
        else:
            return max(0, (self.start - self.stop - self.step - 1) // -self.step)

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

    def __repr__(self) -> str:
        return f"MyRange({self.start}, {self.stop}, {self.step})"


class Money:
    """A simple numeric type that supports addition and multiplication."""

    def __init__(self, amount: float) -> None:
        self.amount = float(amount)

    def __add__(self, other: "Money | float") -> "Money":
        if isinstance(other, Money):
            return Money(self.amount + other.amount)
        elif isinstance(other, (int, float)):
            return Money(self.amount + other)
        return NotImplemented

    __radd__ = __add__

    def __mul__(self, factor: float) -> "Money":
        return Money(self.amount * factor)

    __rmul__ = __mul__

    def __str__(self) -> str:
        return f"${self.amount:.2f}"

    def __repr__(self) -> str:
        return f"Money({self.amount})"


def main() -> None:
    mr = MyRange(0, 10, 2)
    print(list(mr))      # [0, 2, 4, 6, 8]
    print(len(mr))       # 5
    print(mr[2])         # 4
    # Money operations
    balance = Money(10)
    balance += Money(5)
    print(balance)       # $15.00
    # Add float to Money
    print(balance + 2.5) # $17.50
    print(3 * balance)   # $45.00


if __name__ == "__main__":
    main()