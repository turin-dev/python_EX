"""Command‑line argument parsing examples using argparse."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Example argument parser")
    parser.add_argument("filename", help="Input file")
    parser.add_argument("--count", type=int, default=1, help="Number of repetitions")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for i in range(args.count):
        if args.verbose:
            print(f"Verbose iteration {i+1}: processing {args.filename}")
        else:
            print(f"Processing {args.filename}")


if __name__ == "__main__":
    main()