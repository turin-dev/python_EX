"""Examples of manipulating binary data using bytes, bytearray, memoryview, struct and array."""

from __future__ import annotations

import struct
from array import array


def demo_bytes_and_bytearray() -> None:
    data = b"hello"
    print("Original bytes:", data)
    mutable = bytearray(data)
    mutable[0] = ord('H')
    print("Modified bytearray:", mutable)
    # convert back to bytes
    print("Back to bytes:", bytes(mutable))


def demo_memoryview() -> None:
    buf = bytearray(range(10))
    view = memoryview(buf)
    print("First five bytes via memoryview:", view[:5].tolist())
    # modify underlying buffer through view
    view[0:3] = b"abc"
    print("Modified buffer:", buf)


def demo_struct_and_array() -> None:
    # use struct to pack/unpack binary data
    packed = struct.pack('>hI', -2, 65535)
    print("Packed bytes:", packed)
    val1, val2 = struct.unpack('>hI', packed)
    print("Unpacked values:", val1, val2)
    # array of signed ints
    arr = array('i', [1, 2, 3, 4])
    arr.append(5)
    print("Array contents:", arr.tolist())


if __name__ == "__main__":
    demo_bytes_and_bytearray()
    print()
    demo_memoryview()
    print()
    demo_struct_and_array()