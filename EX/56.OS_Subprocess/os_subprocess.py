"""Demonstrate using the os and subprocess modules."""

from __future__ import annotations

import os
import subprocess


def demo_os_operations() -> None:
    """Show some basic os module operations."""
    print("Working directory:", os.getcwd())
    print("CPU count:", os.cpu_count())
    # Environment variable access
    home = os.getenv("HOME", default="not set")
    print("HOME environment variable:", home)
    # Create and remove a temporary directory
    tmp_dir = "tmp_demo"
    os.makedirs(tmp_dir, exist_ok=True)
    print("Created directory", tmp_dir)
    os.rmdir(tmp_dir)
    print("Removed directory", tmp_dir)


def demo_subprocess() -> None:
    """Run an external command using subprocess.run()."""
    result = subprocess.run(["echo", "Hello via subprocess"], capture_output=True, text=True)
    print("Subprocess return code:", result.returncode)
    print("Output:", result.stdout.strip())


if __name__ == "__main__":
    demo_os_operations()
    print()
    demo_subprocess()