"""Examples for working with files and directories using pathlib.

This script demonstrates creating, reading and iterating over paths using
`pathlib.Path`. Run this file to see various operations in action.
"""
from pathlib import Path


def list_python_files(base: Path) -> None:
    """Print all Python files under a directory recursively."""
    for py_file in base.rglob("*.py"):
        print(py_file)


def create_and_write_file() -> None:
    """Create a directory and write/read a text file."""
    data_dir = Path("example_data")
    data_dir.mkdir(exist_ok=True)
    file_path = data_dir / "hello.txt"
    file_path.write_text("Hello, pathlib!\n")
    print("Wrote file", file_path)
    content = file_path.read_text()
    print("Content read:", content.strip())


def demonstrate_path_properties(path: Path) -> None:
    """Display various properties of a path."""
    print("Full path:", path.resolve())
    print("Name:", path.name)
    print("Stem:", path.stem)
    print("Suffix:", path.suffix)
    print("Is file?", path.is_file())
    print("Is directory?", path.is_dir())


if __name__ == "__main__":
    base = Path('.')
    print("Listing Python files in current directory tree:")
    list_python_files(base)
    print("\nCreating and reading a text file:")
    create_and_write_file()
    # Demonstrate properties on this script itself
    demonstrate_path_properties(Path(__file__))