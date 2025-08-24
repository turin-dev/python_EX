"""Examples using math and statistics modules.

This script demonstrates functions from the `math` and `statistics` modules.
"""
import math
from statistics import mean, median, pstdev, pvariance, quantiles


def demo_math_functions() -> None:
    """Print various mathematical computations."""
    print("Pi:", math.pi)
    print("Euler's number e:", math.e)
    print("GCD of 48 and 180:", math.gcd(48, 180))
    print("LCM of 12 and 15:", math.lcm(12, 15))
    print("sqrt(2):", math.sqrt(2))
    print("log10(1000):", math.log10(1000))
    print("sin(π/2):", math.sin(math.pi / 2))


def demo_statistics_functions() -> None:
    """Compute basic statistics for a sample dataset."""
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    print("Data:", data)
    print("Mean:", mean(data))
    print("Median:", median(data))
    print("Population variance:", pvariance(data))
    print("Population standard deviation:", pstdev(data))
    print("Quartiles:", quantiles(data, n=4))


if __name__ == "__main__":
    demo_math_functions()
    demo_statistics_functions()