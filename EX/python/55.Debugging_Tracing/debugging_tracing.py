"""Demonstrate Python debugging and traceback formatting.

This script contains a function that triggers an error.  When run
normally, it catches the exception and prints the traceback.  You can
insert a call to breakpoint() to inspect variables interactively.
"""

from __future__ import annotations

import traceback


def faulty_function(x: int, y: int) -> float:
    """Deliberately perform a bad division to trigger ZeroDivisionError."""
    return x / y  # raises ZeroDivisionError when y == 0


def main() -> None:
    values = [(10, 2), (5, 0), (3, 1)]
    for a, b in values:
        try:
            result = faulty_function(a, b)
        except ZeroDivisionError:
            # capture and print the traceback
            tb = traceback.format_exc()
            print(f"Error computing {a}/{b}\n{tb}")
        else:
            print(f"{a}/{b} = {result}")


if __name__ == "__main__":
    # You can uncomment the following line to start an interactive debugger
    # breakpoint()
    main()