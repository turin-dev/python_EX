"""Retrieve information about the Python runtime and underlying system."""

from __future__ import annotations

import os
import sys
import platform


def show_sys_info() -> None:
    print("Python version:", sys.version)
    print("Platform:", sys.platform)
    print("Max int:", sys.maxsize)
    print("Module search path count:", len(sys.path))


def show_platform_info() -> None:
    print("System:", platform.system())
    print("Release:", platform.release())
    print("Machine:", platform.machine())
    print("Python implementation:", platform.python_implementation())


def show_os_info() -> None:
    print("os.name:", os.name)
    if hasattr(os, "uname"):
        print("os.uname:", os.uname())
    print("HOME:", os.getenv("HOME"))


if __name__ == "__main__":
    show_sys_info()
    show_platform_info()
    show_os_info()