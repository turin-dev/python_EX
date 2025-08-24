"""
Demonstrate manual control of CPython's garbage collector.
"""

import gc


class Node:
    def __init__(self) -> None:
        self.other: "Node | None" = None


def create_cycle() -> None:
    """Create a simple reference cycle between two nodes."""
    a = Node()
    b = Node()
    a.other = b
    b.other = a


def main() -> None:
    # Ensure the collector is enabled
    gc.enable()
    print("Collector enabled?", gc.isenabled())
    create_cycle()
    # Force a full collection
    unreachable_before = gc.collect()
    print("Unreachable objects before disabling collector:", unreachable_before)
    # Disable collector and create another cycle
    gc.disable()
    create_cycle()
    print("Collector enabled?", gc.isenabled())
    # When disabled, gc.collect will still collect but automatic collection stops
    unreachable_after = gc.collect()
    print("Unreachable objects with collector disabled:", unreachable_after)
    # Reenable collector
    gc.enable()
    print("Reenabled collector")


if __name__ == "__main__":
    main()