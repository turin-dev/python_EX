# 49. Modules, packages and programmatic import

Python organises code into **modules** (files containing definitions) and
**packages** (directories containing an `__init__.py` file).  Modules can
import other modules using the `import` statement.  Internally, the import
mechanism is implemented by the `importlib` package.  The `importlib`
documentation states that its purpose is three‑fold: to provide a portable
implementation of the `import` statement; expose components so users can
create custom importers; and offer utility functions for working with
packages【491628540515688†L69-L84】.  It recommends using
`importlib.import_module()` instead of directly calling `__import__()`
【491628540515688†L161-L176】.

## Creating a package

To create a package, place an `__init__.py` file in a directory.  Any
modules inside the directory can be imported using dotted notation.  For
example, with the following structure:

```
my_pkg/
    __init__.py
    utilities.py
    data/
        __init__.py
        loader.py
```

You can import `utilities` with `import my_pkg.utilities` and `loader` with
`from my_pkg.data import loader`.  The top‑level `__init__.py` can define
what names are exported when `import my_pkg` is used by setting
`__all__ = ['utilities', 'data']`.

## Programmatic imports

Use `importlib.import_module(name, package=None)` to import a module when
the name is determined at runtime.  The `name` parameter may be absolute or
relative; when using relative names you must supply the package argument
【491628540515688†L169-L176】.  For example:

```python
import importlib

mod = importlib.import_module('math')
print(mod.sqrt(9))

# Import a submodule
json_encoder = importlib.import_module('.encoder', 'json')
```

## Metadata and resources

Use `importlib.metadata` to access package metadata (such as the version
number) and `importlib.resources` to read data files bundled with
packages【491628540515688†L86-L90】.

## Packaging and distribution

For real projects you should provide a `pyproject.toml` file describing how
to build your package.  Tools like `setuptools`, `flit` and `poetry` use
this file.  Publishing packages to the Python Package Index (PyPI) allows
others to `pip install` them.

## Summary

Understanding how Python finds and loads modules will help you organise
applications and reuse code effectively.  The `importlib` module exposes
the import mechanism in Python and offers utility functions for dynamic
imports and accessing package metadata【491628540515688†L69-L84】.
