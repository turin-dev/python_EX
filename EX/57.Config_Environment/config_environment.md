# Chapter 57 – Configuration Files and Environment Variables

Programs often need configurable settings.  Python’s `configparser` module provides a basic configuration language similar to Windows INI files, allowing end users to customise behaviour through text files【257164874177851†L67-L70】.  Additionally, environment variables can override defaults at runtime.

## Parsing configuration files

`configparser.ConfigParser` reads and writes configuration files with sections and key‑value pairs.  A quick start example from the documentation shows how to create a configuration, add sections and options, write it to disk, and read it back【257164874177851†L96-L131】.  When reading, you can access sections like dictionaries and retrieve options with optional fallback values【257164874177851†L138-L166】.

```python
import configparser

config = configparser.ConfigParser()
config["DEFAULT"] = {"ServerAliveInterval": "45", "Compression": "yes"}
config["bitbucket.org"] = {"User": "hg"}
config["topsecret.server.com"] = {"Host Port": "50022", "ForwardX11": "no"}

with open("settings.ini", "w") as f:
    config.write(f)

# Reading the configuration
parser = configparser.ConfigParser()
parser.read("settings.ini")
port = parser["topsecret.server.com"].getint("Host Port")
print("Host port:", port)
```

## Environment variables override

Use `os.environ` to inspect and set environment variables.  Accessing a variable that is not set returns `KeyError` or `None` depending on method; use `os.getenv("VAR", default)` to provide a fallback.  Environment variables often override configuration file values to allow easy customisation without editing files.

Example:

```python
import os
import configparser

# Load defaults from configuration file
parser = configparser.ConfigParser()
parser.read("settings.ini")

# Override with environment variable if present
port = int(os.getenv("APP_PORT", parser["DEFAULT"].get("Port", "8080")))
print("Using port:", port)
```

## Summary

Use `configparser` to parse simple INI‑style configuration files; sections and options behave like nested dictionaries【257164874177851†L96-L166】.  Allow environment variables to override or augment configuration values for flexible deployment.  Combining configuration files with environment overrides yields a robust configuration strategy.