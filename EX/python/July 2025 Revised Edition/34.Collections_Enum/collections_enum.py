"""Example usage of collections and enum from the Python standard library.

This script demonstrates several useful container types from the `collections`
module and how to define and use enumerations with the `enum` module.

Collections provide more specialized data structures than built‑in lists and
dictionaries. Enumerations let you define symbolic names bound to unique values.
"""
from collections import namedtuple, deque, Counter, OrderedDict, defaultdict, ChainMap
from enum import Enum, auto


def demo_namedtuple() -> None:
    """Show how namedtuple allows attribute access on tuple elements."""
    Point = namedtuple("Point", ["x", "y"])
    p = Point(2, 3)
    print(f"Point: x={p.x}, y={p.y}, as tuple={tuple(p)}")


def demo_deque() -> None:
    """Show deque operations from both ends."""
    dq = deque([1, 2, 3])
    dq.append(4)
    dq.appendleft(0)
    print(f"Deque after appends: {list(dq)}")
    dq.pop()
    dq.popleft()
    print(f"Deque after pops: {list(dq)}")


def demo_counter() -> None:
    """Count character occurrences using Counter."""
    text = "collections and enums"
    counts = Counter(text.replace(" ", ""))
    print("Most common letters:", counts.most_common(3))


def demo_defaultdict() -> None:
    """Group words by their first letter using defaultdict."""
    words = ["apple", "banana", "avocado", "blueberry", "cherry"]
    by_initial: defaultdict[str, list[str]] = defaultdict(list)
    for word in words:
        by_initial[word[0]].append(word)
    print("Grouped words:", dict(by_initial))


def demo_ordered_dict() -> None:
    """Demonstrate OrderedDict retains insertion order and can move items."""
    od = OrderedDict()
    od["first"] = 1
    od["second"] = 2
    od["third"] = 3
    print("Original order:", list(od.keys()))
    # Move a key to the end
    od.move_to_end("second")
    print("After move_to_end:", list(od.keys()))


def demo_chainmap() -> None:
    """Combine multiple dictionaries into a single view using ChainMap."""
    defaults = {"color": "red", "user": "guest"}
    user_settings = {"user": "admin"}
    cmdline = {"color": "blue"}
    combined = ChainMap(cmdline, user_settings, defaults)
    # Lookups search each mapping in order
    print("Combined color:", combined["color"])  # 'blue'
    print("Combined user:", combined["user"])   # 'admin'


class Color(Enum):
    """An enumeration of basic colors."""

    RED = auto()
    GREEN = auto()
    BLUE = auto()


def demo_enum() -> None:
    """Demonstrate enumeration usage."""
    print("Color members:", list(Color))
    print("The value of Color.RED is", Color.RED.value)
    # Comparisons use identity, not raw values
    if Color.RED is Color.RED:
        print("Colors are identical")
    # Iteration yields members in definition order
    for color in Color:
        print(f"Color {color.name} = {color.value}")


if __name__ == "__main__":
    demo_namedtuple()
    demo_deque()
    demo_counter()
    demo_defaultdict()
    demo_ordered_dict()
    demo_chainmap()
    demo_enum()