# Chapter 61 – Working with Binary Data

Python supports several types and modules for manipulating raw bytes.  The built‑in `bytes` type represents immutable sequences of bytes, while `bytearray` offers a mutable variant.  The `memoryview` type provides a safe way to access the memory of binary objects without copying.  You can also use the `array` module for efficient numeric arrays and the `struct` module to pack and unpack binary data into Python values.  The documentation notes that many operating system functions accept either `str` or `bytes` paths and data【549557713116431†L88-L90】, making it important to understand these types.

## Byte sequences

* **`bytes`** – Immutable sequence of 8‑bit integers (0–255).  You create bytes literals with a `b` prefix or by encoding strings.  Common methods include `.hex()`, `.decode()` and slicing.
* **`bytearray`** – Mutable version of bytes supporting in‑place modifications, `.append()`, `.extend()` and `.pop()` operations.
* **`memoryview`** – A view object that exposes a buffer protocol interface to an underlying bytes-like object without copying.  Use it to slice large binary data efficiently.

```python
data = b"\x48\x65\x6c\x6c\x6f"  # bytes literal
print(data.hex())        # '48656c6c6f'
mutable = bytearray(data)
mutable[0] = 0x77  # change first byte to 'w'
view = memoryview(mutable)
print(view[0:3].tobytes())  # b'wEl'
```

## Structured binary data

When communicating with binary protocols or reading binary files, you often need to convert between Python values and packed byte sequences.  The `struct` module performs this conversion using format strings that specify the layout.  For example, `struct.pack('>I', 42)` packs an unsigned 32‑bit big‑endian integer into four bytes, and `struct.unpack('<h', b'\x34\x12')` returns a little‑endian signed short.

The `array` module provides compact array types (e.g., `'h'` for signed short, `'I'` for unsigned int) that store homogeneous numeric data more efficiently than lists.

```python
import struct
from array import array

# pack and unpack using struct
p = struct.pack('>I', 65535)  # big‑endian unsigned int
print(p)  # b'\x00\x00\xff\xff'
value, = struct.unpack('>I', p)
print(value)  # 65535

# array of 16‑bit integers
a = array('h', [1000, -2000, 3000])
print(a)
a[1] = 0  # modify in place
print(a)
```

## Summary

Use `bytes` for immutable binary data and `bytearray` when you need mutability.  Memory views allow slicing and manipulation without copying.  The `struct` module converts between Python values and C‑style binary representations, while the `array` module stores homogeneous numeric data efficiently.  These types are essential for working with binary protocols and file formats【549557713116431†L88-L90】.