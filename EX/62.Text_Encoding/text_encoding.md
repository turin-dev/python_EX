# Chapter 62 – Text Encoding and Codecs

Computers store text as sequences of bytes.  Encoding schemes map characters to integer codes, while decoders transform byte sequences back into text.  Python uses Unicode strings internally and provides powerful tools for encoding and decoding, including the `codecs` module and the `base64` module for binary‑to‑text encoding.  It’s important to understand the difference between text (str) and bytes; many file and OS APIs accept either type【549557713116431†L88-L90】.

## Encoding and decoding strings

To convert a string to bytes, call `encode()` with the desired encoding; to convert bytes back to a string, call `decode()`.  Common encodings include UTF‑8, UTF‑16 and Latin‑1.  The built‑in open function will encode and decode automatically when reading or writing text files.

```python
text = "Café"
b = text.encode("utf‑8")
print(b)           # b'Caf\xc3\xa9'
recovered = b.decode("utf‑8")
print(recovered)  # 'Café'
```

The `codecs` module provides generic encode/decode functions and registry access for all supported encodings.  For streaming, it offers incremental encoders and decoders.

## Base64 and other binary‑to‑text encodings

The `base64` module converts binary data to ASCII strings using Base64, Base32 or Base85 encodings.  This is useful for transmitting binary content over text‑based protocols such as email or HTTP.

```python
import base64

data = b"\x00\xf0\xaa\x55"
b64 = base64.b64encode(data)
print(b64)               # b'APCqVQ=='
decoded = base64.b64decode(b64)
print(decoded == data)  # True
```

## Handling errors

When decoding, invalid byte sequences raise `UnicodeDecodeError`.  You can pass an `errors` parameter like `'replace'` or `'ignore'` to handle malformed data gracefully.  Similarly, encoding may raise `UnicodeEncodeError` if a character cannot be represented in the chosen encoding.

## Summary

Understanding Unicode and encodings ensures your programs handle text and binary data correctly.  Use `str.encode()` and `bytes.decode()` to convert between text and bytes, `codecs` for lower‑level encoding operations, and `base64` or related modules to represent binary data as ASCII【549557713116431†L88-L90】.