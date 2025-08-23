"""Examples using the decimal and fractions modules for exact arithmetic."""

from __future__ import annotations

from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction


def demonstrate_decimal() -> None:
    """Show various decimal operations with adjustable precision and rounding."""
    getcontext().prec = 6  # set precision to 6 significant digits
    getcontext().rounding = ROUND_HALF_UP
    a = Decimal("1.2345")
    b = Decimal("6.7890")
    print(f"{a} + {b} = {a + b}")
    print(f"{a} / {b} = {a / b}")
    # demonstrate rounding behaviour
    print(f"Round 1/7: {Decimal(1) / Decimal(7)}")


def demonstrate_fractions() -> None:
    """Show arithmetic with fractions and conversions."""
    f1 = Fraction(3, 4)
    f2 = Fraction(5, 6)
    print(f"{f1} + {f2} = {f1 + f2}")
    print(f"{f1} * {f2} = {f1 * f2}")
    # from strings and floats
    f_str = Fraction("0.125")
    f_float = Fraction(0.125)
    print(f"Fraction('0.125') = {f_str}")
    print(f"Fraction(0.125) = {f_float}")
    # normalization demonstration
    f = Fraction(50, 100)
    print(f"Simplified 50/100 = {f}")


if __name__ == "__main__":
    print("Decimal examples:")
    demonstrate_decimal()
    print("\nFraction examples:")
    demonstrate_fractions()