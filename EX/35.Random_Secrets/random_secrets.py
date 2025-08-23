"""Demonstrations of the random and secrets modules.

This script shows how to generate pseudo‑random numbers for simulations using
`random` and how to generate cryptographically secure tokens using `secrets`.
"""
import random
import secrets
import string


def demo_random_numbers() -> None:
    """Generate a few pseudo‑random values using the random module."""
    print("Random float [0, 1):", random.random())
    print("Random integer 1–6:", random.randint(1, 6))
    fruits = ["apple", "banana", "cherry"]
    print("Random choice:", random.choice(fruits))
    lst = list(range(5))
    random.shuffle(lst)
    print("Shuffled list:", lst)


def demo_random_distribution() -> None:
    """Simulate a Gaussian distribution and display summary statistics."""
    data = [random.gauss(mu=0, sigma=1) for _ in range(1000)]
    # Compute rough mean and variance
    mean = sum(data) / len(data)
    var = sum((x - mean) ** 2 for x in data) / len(data)
    print(f"Gaussian sample: mean ≈ {mean:.3f}, variance ≈ {var:.3f}")


def demo_secrets_tokens() -> None:
    """Generate secure tokens and random numbers using the secrets module."""
    print("16‑byte hex token:", secrets.token_hex(16))
    # Generate a secure random password using letters and digits
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(12))
    print("Generated password:", password)
    print("Random integer < 100:", secrets.randbelow(100))


if __name__ == "__main__":
    demo_random_numbers()
    demo_random_distribution()
    demo_secrets_tokens()