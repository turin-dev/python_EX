"""Example of using configparser with environment overrides."""

from __future__ import annotations

import configparser
import os


def write_default_config(path: str) -> None:
    """Write a sample configuration file to the given path."""
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"Port": "8000", "Debug": "false"}
    config["database"] = {"User": "dbuser", "Password": "secret", "Host": "localhost"}
    with open(path, "w") as f:
        config.write(f)


def load_config(path: str) -> dict[str, str]:
    """Load configuration and apply environment overrides."""
    parser = configparser.ConfigParser()
    parser.read(path)
    cfg = dict(parser["DEFAULT"])
    # Apply environment variables, falling back to config values
    cfg["Port"] = os.getenv("APP_PORT", cfg.get("Port", "8000"))
    cfg["Debug"] = os.getenv("APP_DEBUG", cfg.get("Debug", "false"))
    return cfg


if __name__ == "__main__":
    ini_file = "example.ini"
    write_default_config(ini_file)
    print("Default configuration written to", ini_file)
    config = load_config(ini_file)
    print("Loaded configuration:", config)
    # Clean up
    os.remove(ini_file)