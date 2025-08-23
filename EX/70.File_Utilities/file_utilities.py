"""Demonstrate globbing, filename matching, file comparison and copying."""

from __future__ import annotations

import glob
import fnmatch
import filecmp
import shutil
import os


def create_sample_files() -> None:
    """Create sample files for demonstration."""
    with open("file1.txt", "w") as f:
        f.write("Hello\n")
    with open("file2.txt", "w") as f:
        f.write("Hello\n")
    with open("script.sh", "w") as f:
        f.write("#!/bin/sh\necho hi\n")


def demo_glob_and_fnmatch() -> None:
    print("Python files:", glob.glob("*.py"))
    names = os.listdir()
    print("*.txt files:", fnmatch.filter(names, "*.txt"))


def demo_filecmp_and_shutil() -> None:
    same = filecmp.cmp("file1.txt", "file2.txt", shallow=False)
    print("file1 and file2 same?", same)
    shutil.copy("file1.txt", "file1_copy.txt")
    print("Copied file1 to file1_copy.txt")


if __name__ == "__main__":
    create_sample_files()
    demo_glob_and_fnmatch()
    demo_filecmp_and_shutil()
    # cleanup
    for fname in ["file1.txt", "file2.txt", "file1_copy.txt", "script.sh"]:
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass