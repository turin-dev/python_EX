"""Demonstrate in‑memory text and binary streams using io.StringIO and BytesIO."""

from __future__ import annotations

from io import StringIO, BytesIO


def demonstrate_stringio() -> None:
    buf = StringIO()
    buf.write("Line 1\n")
    buf.write("Line 2\n")
    contents = buf.getvalue()
    print("StringIO contents:\n", contents)
    buf.close()


def demonstrate_bytesio() -> None:
    buf = BytesIO()
    buf.write(b"\x01\x02\x03")
    buf.seek(0)
    data = buf.read()
    print("BytesIO data:", data)
    buf.close()


if __name__ == "__main__":
    demonstrate_stringio()
    demonstrate_bytesio()