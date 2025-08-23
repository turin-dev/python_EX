"""
Demonstration of using the inspect module for introspection.

This script defines a simple class and introspects its attributes and
methods.  It also shows how to examine a function’s signature and obtain
source code.
"""

import inspect
from typing import Any


class Person:
    """Simple class for introspection examples."""

    species = "Homo sapiens"

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Hello, I'm {self.name} and I'm {self.age} years old."


def show_signature(func: Any) -> None:
    """Print the function signature and default values."""
    sig = inspect.signature(func)
    print(f"Signature for {func.__name__}: {sig}")
    for name, param in sig.parameters.items():
        print(f"  {name}: kind={param.kind}, default={param.default}")


def list_members(obj: Any) -> None:
    """List functions and attributes of an object."""
    members = inspect.getmembers(obj)
    print(f"Members of {obj}:")
    for name, value in members:
        print(f"  {name}: {type(value)}")


def show_source(func: Any) -> None:
    """Print the source code for a function if available."""
    try:
        source = inspect.getsource(func)
        print(source)
    except OSError:
        print("Source not available")


def main() -> None:
    person = Person("Alice", 30)
    # Introspect the Person class and instance
    list_members(Person)
    list_members(person)
    # Show signature of the greet method
    show_signature(Person.greet)
    # Display source code of the greet method
    show_source(Person.greet)


if __name__ == "__main__":
    main()