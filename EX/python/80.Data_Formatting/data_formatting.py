"""Examples of string formatting, pretty printing and text wrapping."""

from __future__ import annotations

import textwrap
from pprint import pprint


def show_formatting() -> None:
    name = "Charlie"
    score = 88.929
    print(f"{name:>10s} scored {score:.2f}")
    template = "{name:<10s} scored {score:05.1f}"
    print(template.format(name=name, score=score))


def show_pprint() -> None:
    data = {
        "fruits": ["apple", "banana", "cherry"],
        "prices": {"apple": 0.99, "banana": 0.59, "cherry": 2.50},
        "in_stock": True,
    }
    pprint(data)


def show_textwrap() -> None:
    text = ("Python's standard library is very extensive, offering a wide range of facilities "
            "as indicated by the long list of modules distributed with the language.")
    print(textwrap.fill(text, width=50))


if __name__ == "__main__":
    show_formatting()
    print()
    show_pprint()
    print()
    show_textwrap()