"""Script to inspect package metadata using importlib.metadata."""

from __future__ import annotations

from importlib import metadata


def show_metadata(package: str) -> None:
    try:
        meta = metadata.metadata(package)
    except metadata.PackageNotFoundError:
        print(f"Package {package} is not installed")
        return
    print(f"{package} version:", meta.get("Version"))
    print("Summary:", meta.get("Summary"))
    print("Requires-Python:", meta.get("Requires-Python"))


if __name__ == "__main__":
    show_metadata("pip")