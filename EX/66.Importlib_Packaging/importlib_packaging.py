"""Demonstrate dynamic imports and querying package metadata."""

from __future__ import annotations

import importlib
from importlib import metadata


def run_dynamic_import() -> None:
    """Dynamically import a module and call a function."""
    module_name = "math"
    func_name = "factorial"
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    print(f"{module_name}.{func_name}(5) =", func(5))


def show_package_info(package: str) -> None:
    """Print version and summary of an installed distribution."""
    try:
        ver = metadata.version(package)
        meta = metadata.metadata(package)
        print(f"{package} version: {ver}")
        print(f"Summary: {meta.get('Summary')}")
    except metadata.PackageNotFoundError:
        print(f"Package {package!r} is not installed")


if __name__ == "__main__":
    run_dynamic_import()
    show_package_info("pip")