"""AST processing examples: parsing, visiting, and modifying code."""

from __future__ import annotations

import ast
from typing import Any


def dump_ast(source: str) -> None:
    """Parse Python source and print its abstract syntax tree."""
    tree = ast.parse(source)
    print(ast.dump(tree, indent=4))


class VariableCollector(ast.NodeVisitor):
    """Visitor that collects variable names from Name nodes."""
    def __init__(self) -> None:
        self.names: list[str] = []

    def visit_Name(self, node: ast.Name) -> Any:
        if isinstance(node.ctx, ast.Load):
            self.names.append(node.id)
        self.generic_visit(node)


class RenameVariables(ast.NodeTransformer):
    """Transformer that renames variables according to a mapping."""
    def __init__(self, mapping: dict[str, str]) -> None:
        self.mapping = mapping

    def visit_Name(self, node: ast.Name) -> Any:
        new_id = self.mapping.get(node.id, node.id)
        if new_id != node.id:
            return ast.copy_location(ast.Name(id=new_id, ctx=node.ctx), node)
        return node


def example() -> None:
    source = """
def add(x, y):
    result = x + y
    return result
"""
    print("Original AST:")
    dump_ast(source)
    tree = ast.parse(source)
    # Collect variable names
    collector = VariableCollector()
    collector.visit(tree)
    print("Variables used:", collector.names)
    # Rename x -> a, y -> b
    transformer = RenameVariables({"x": "a", "y": "b"})
    new_tree = transformer.visit(tree)
    compiled = compile(new_tree, filename="<ast>", mode="exec")
    namespace: dict[str, Any] = {}
    exec(compiled, namespace)
    print("Result of add(a, b):", namespace["add"](2, 3))


if __name__ == "__main__":
    example()