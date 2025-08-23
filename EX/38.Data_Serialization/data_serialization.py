"""Examples of object serialization and configuration management.

This script demonstrates how to use pickle and shelve to persist Python
objects, and how to read/write configuration files using configparser and
tomllib (if available).
"""
import pickle
import shelve
import configparser
from pathlib import Path
import os

try:
    import tomllib  # Python 3.11+ for reading TOML
except ModuleNotFoundError:
    tomllib = None  # type: ignore


def demo_pickle() -> None:
    """Serialize and deserialize a Python object using pickle."""
    data = {"numbers": [1, 2, 3], "message": "Hello"}
    file_path = Path("data.pkl")
    with file_path.open("wb") as f:
        pickle.dump(data, f)
    with file_path.open("rb") as f:
        loaded = pickle.load(f)
    print("Pickle loaded:", loaded)
    file_path.unlink(missing_ok=True)


def demo_shelve() -> None:
    """Use shelve to store and retrieve key‑value data."""
    with shelve.open("mydatabase") as db:
        db["counter"] = list(range(5))
        db["config"] = {"debug": True, "log_level": "info"}
        print("Shelve keys:", list(db.keys()))
    # Reopen to read
    with shelve.open("mydatabase") as db:
        print("Counter from shelve:", db["counter"])
    # Remove the underlying files
    for suffix in ("", ".db", ".bak", ".dat", ".dir"):
        try:
            os.remove("mydatabase" + suffix)
        except FileNotFoundError:
            pass


def demo_configparser() -> None:
    """Write and read an INI configuration file."""
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"ServerAliveInterval": "45", "Compression": "yes"}
    config["bitbucket.org"] = {"User": "hg"}
    config["topsecret.server.com"] = {"Port": "50022", "ForwardX11": "no"}
    ini_path = Path("config.ini")
    with ini_path.open("w") as f:
        config.write(f)
    # Read back
    config2 = configparser.ConfigParser()
    config2.read(ini_path)
    print("Config sections:", config2.sections())
    ini_path.unlink(missing_ok=True)


def demo_toml_read() -> None:
    """Read a TOML file using tomllib if available."""
    if tomllib is None:
        print("tomllib is not available on this Python version.")
        return
    toml_path = Path("example.toml")
    toml_path.write_text("""\
[database]
server = "db.example.com"
ports = [ 8001, 8001, 8002 ]
enabled = true
""")
    with toml_path.open("rb") as f:
        data = tomllib.load(f)
    print("TOML data:", data)
    toml_path.unlink(missing_ok=True)


if __name__ == "__main__":
    demo_pickle()
    demo_shelve()
    demo_configparser()
    demo_toml_read()