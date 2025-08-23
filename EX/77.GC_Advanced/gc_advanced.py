"""Advanced garbage collection control example."""

from __future__ import annotations

import gc


def tweak_gc_thresholds() -> None:
    original = gc.get_threshold()
    print("Original thresholds:", original)
    # increase thresholds to reduce collection frequency
    new_thresholds = tuple(t * 2 for t in original)
    gc.set_threshold(*new_thresholds)
    print("New thresholds:", gc.get_threshold())
    # restore original
    gc.set_threshold(*original)


def enable_debugging() -> None:
    gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_UNCOLLECTABLE)
    print("Triggering a collection with debugging on…")
    unreachable = gc.collect()
    print("Unreachable objects:", unreachable)
    gc.set_debug(0)


if __name__ == "__main__":
    tweak_gc_thresholds()
    enable_debugging()