# Chapter 56 – Interacting with the Operating System

The `os` module provides a portable interface to many operating system services.  It exposes functions for environment variables, process management, filesystem operations, and low‑level system calls.  The documentation emphasises that `os` aims to be cross‑platform and recommends using built‑in `open()` or `pathlib` for file I/O and path manipulation【549557713116431†L69-L76】.  Many functions accept either `str` or `bytes` paths【549557713116431†L88-L90】.

## Environment and path utilities

* **Environment variables** – Access and modify the process environment via `os.environ`, a mutable mapping.  Use `os.getenv()` to retrieve values with a default.
* **Process information** – `os.getpid()` returns the current process ID, and `os.cpu_count()` reports the number of CPUs.
* **Filesystem operations** – `os.listdir()` lists directory contents; `os.mkdir()` creates directories; `os.remove()` and `os.rmdir()` delete files and directories; `os.rename()` renames files; `os.path` functions (or `pathlib`) handle path joining, splitting, and normalization.

Example:

```python
import os

print("Current directory:", os.getcwd())
os.makedirs("subdir", exist_ok=True)
with open(os.path.join("subdir", "file.txt"), "w") as f:
    f.write("Hello, os!")
print("Files:", os.listdir("subdir"))
os.remove(os.path.join("subdir", "file.txt"))
os.rmdir("subdir")
```

## Running external commands with `subprocess`

The `subprocess` module lets you spawn new processes, connect to their input/output streams, and obtain return codes.  It is intended to replace older functions like `os.system()` and provides more control over process execution【793962385525121†L76-L83】.  The high‑level `subprocess.run()` function runs a command described by a list or string, waits for it to complete, and returns a `CompletedProcess` object containing the exit code and captured output【793962385525121†L103-L110】.

```python
import subprocess

result = subprocess.run(["echo", "Hello from subprocess"], capture_output=True, text=True)
print("Return code:", result.returncode)
print("Stdout:", result.stdout.strip())
```

You can provide `stdin`, `stdout`, `stderr`, `timeout` and `env` arguments to control the child process.  When capturing output, set `text=True` to return strings instead of bytes.  For advanced use cases, use `Popen` to manage long‑running processes and communicate interactively.

## Summary

Use the `os` module to interact with the filesystem and process environment in a portable way【549557713116431†L69-L76】.  When executing external commands, prefer the `subprocess` module and its `run()` function for ease of use and greater control【793962385525121†L76-L110】.