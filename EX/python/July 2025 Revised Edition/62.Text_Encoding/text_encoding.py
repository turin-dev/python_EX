"""Text encoding and binary encoding examples."""

from __future__ import annotations

import base64


def demonstrate_encoding() -> None:
    text = "¡Hola, mundo!"
    utf8_bytes = text.encode("utf-8")
    latin1_bytes = text.encode("latin1", errors="replace")
    print("UTF-8 bytes:", utf8_bytes)
    print("Latin-1 bytes (with replacement):", latin1_bytes)
    print("Decoded back:", utf8_bytes.decode("utf-8"))


def demonstrate_base64() -> None:
    data = b"binary\x00data"
    encoded = base64.b64encode(data)
    print("Base64 encoded:", encoded)
    decoded = base64.b64decode(encoded)
    print("Decoded matches original:", decoded == data)


if __name__ == "__main__":
    demonstrate_encoding()
    print()
    demonstrate_base64()