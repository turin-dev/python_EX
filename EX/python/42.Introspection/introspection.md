# 42. Reflection and Introspection

Introspection means examining Python objects at runtime.  The `inspect`
module provides functions for getting information about live objects such as
modules, classes, methods, functions and frames.  As the documentation
states, `inspect` can be used to examine classes, retrieve the source code of
a method, extract and format the argument list for a function or get
information for displaying a detailed traceback【319197758890060†L65-L72】.  It
offers services for type checking, retrieving source code, inspecting
callables and examining the interpreter stack【319197758890060†L65-L74】.

## Key functions

- `inspect.getmembers(obj, predicate=None)`: return a list of (name, value)
  pairs of the members of an object.  Use predicates like
  `inspect.isfunction` to filter results【319197758890060†L76-L83】.
- `inspect.signature(callable)`: return a `Signature` object that describes
  the call signature of a callable.  You can inspect parameters and defaults.
- `inspect.getsource(object)`: return the text of the source code for the
  object if available.
- `inspect.isclass`, `inspect.ismethod`, `inspect.isfunction`: return
  booleans indicating the type of object.
- `inspect.stack()`: get the current call stack frames.  Useful for
  debugging and logging.

## Example: Inspecting a function

```python
import inspect

def greet(name: str, greeting: str = "Hello") -> str:
    """Return a greeting."""
    return f"{greeting}, {name}!"

# Print signature and defaults
sig = inspect.signature(greet)
print("Signature:", sig)
for name, param in sig.parameters.items():
    print(name, param.kind, param.default)

# Get source code
print("Source:\n", inspect.getsource(greet))

# Check if an object is a function
print(inspect.isfunction(greet))  # True
```

## Introspecting classes and modules

You can use `inspect.getmembers()` with `predicate=inspect.isfunction` to list
functions defined in a module or methods of a class.  For example:

```python
import inspect
import math

# List all functions in the math module
functions = inspect.getmembers(math, inspect.isbuiltin)
for name, func in functions:
    print(name, func)
```

## Summary

The `inspect` module makes it easy to explore objects, their attributes and
call signatures at runtime.  It underpins tools like IDEs, debuggers and
interactive help systems【319197758890060†L65-L74】.
