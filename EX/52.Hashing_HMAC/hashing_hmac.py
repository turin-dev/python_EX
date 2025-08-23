"""Demonstration of hashing and HMAC in Python.

This script shows how to compute message digests using hashlib and
authenticate messages using the hmac module.
"""

from __future__ import annotations

import hashlib
import hmac


def compute_hash(data: bytes, algorithm: str = "sha256") -> str:
    """Return the hexadecimal digest of data using the chosen algorithm."""
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(data)
    return hash_obj.hexdigest()


def compute_hmac(key: bytes, data: bytes, algorithm: str = "sha256") -> str:
    """Return the hexadecimal HMAC of the data using the secret key."""
    mac = hmac.new(key, data, getattr(hashlib, algorithm))
    return mac.hexdigest()


def verify_hmac(key: bytes, data: bytes, mac_hex: str, algorithm: str = "sha256") -> bool:
    """Verify that the provided HMAC matches the data and key."""
    expected = compute_hmac(key, data, algorithm)
    # Use compare_digest for constant‑time comparison
    return hmac.compare_digest(mac_hex, expected)


if __name__ == "__main__":
    message = b"Verify the integrity of this message"
    secret = b"secret‑token"

    print("Hash digests:")
    for algo in ("sha256", "sha512", "blake2b"):
        print(f"{algo}: {compute_hash(message, algo)}")

    # Compute and verify HMAC
    print("\nComputing HMAC...")
    mac = compute_hmac(secret, message, "sha256")
    print(f"HMAC: {mac}")
    # Verification
    is_valid = verify_hmac(secret, message, mac, "sha256")
    print(f"Verification succeeded: {is_valid}")