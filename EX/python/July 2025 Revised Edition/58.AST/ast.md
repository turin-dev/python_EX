# Chapter 58 – Processing Python Code with AST

The `ast` module allows Python programs to process abstract syntax trees.  An AST represents the syntactic structure of code as a tree of objects, making it possible to analyse or transform Python code programmatically.  You can obtain an AST by parsing source code or using the `compile()` function with the `ast.PyCF_ONLY_AST` flag【218391270827229†L74-L84】.  ASTs can be compiled back into code objects for execution.

## Creating and walking an AST

To parse Python source into an AST, use `ast.parse(source, filename='<unknown>', mode='exec')`.  The resulting tree consists of node classes like `Module`, `FunctionDef`, `Name`, and `Constant`.  You can traverse the tree using `ast.walk()` or `ast.iter_child_nodes()`, or write a custom visitor by subclassing `ast.NodeVisitor`.

```python
import ast

source = """
def greet(name):
    return f"Hello, {name}!"
"""

tree = ast.parse(source)
print(ast.dump(tree, indent=4))

# Count function definitions
class FuncCounter(ast.NodeVisitor):
    def __init__(self):
        self.count = 0
    def visit_FunctionDef(self, node):
        self.count += 1
        self.generic_visit(node)

counter = FuncCounter()
counter.visit(tree)
print("Number of functions:", counter.count)
```

## Modifying code

You can transform code by creating a subclass of `ast.NodeTransformer` and returning modified nodes.  After transformation, compile the AST back into a code object with `compile(ast_tree, filename, mode)` and execute it with `exec()`【218391270827229†L74-L84】.

Example: rename all variables named `x` to `y`:

```python
class RenameX(ast.NodeTransformer):
    def visit_Name(self, node):
        if node.id == "x":
            return ast.copy_location(ast.Name(id="y", ctx=node.ctx), node)
        return node

tree2 = RenameX().visit(tree)
code = compile(tree2, filename="<ast>", mode="exec")
exec(code, {})  # executes the modified code
```

## Summary

The `ast` module provides access to Python’s abstract syntax grammar.  Use `ast.parse()` or `compile(..., flags=ast.PyCF_ONLY_AST)` to obtain an AST, traverse or transform it with visitor classes, and compile the modified tree back into executable code【218391270827229†L74-L84】.