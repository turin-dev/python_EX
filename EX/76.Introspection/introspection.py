"""Examples of using the inspect module for introspection."""

from __future__ import annotations

import inspect
import math


def sample_function(a: int, b: int = 42) -> int:
    """Return the sum of a and b."""
    return a + b


def show_function_info(func) -> None:
    sig = inspect.signature(func)
    print("Signature:", sig)
    print("Docstring:", inspect.getdoc(func))
    print("Source:\n", inspect.getsource(func))


def list_math_builtins() -> None:
    builtins = [name for name, obj in inspect.getmembers(math, inspect.isbuiltin)]
    print("Built‑ins in math:", builtins)


if __name__ == "__main__":
    show_function_info(sample_function)
    list_math_builtins()