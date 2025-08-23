"""
Demonstrate programmatic imports using importlib.
"""

import importlib
import importlib.metadata


def dynamic_import(module_name: str) -> object:
    """Dynamically import a module by name and return it."""
    return importlib.import_module(module_name)


def show_package_version(package: str) -> str:
    """Return the version metadata for an installed package."""
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def main() -> None:
    # Import math and use it
    math_mod = dynamic_import('math')
    print("sqrt(16) =", math_mod.sqrt(16))
    # Attempt to get version of a standard library package
    print("math version:", show_package_version('math'))
    # Import a submodule of json
    encoder = importlib.import_module('.encoder', 'json')
    print("JSON Encoder class:", encoder.JSONEncoder)


if __name__ == "__main__":
    main()