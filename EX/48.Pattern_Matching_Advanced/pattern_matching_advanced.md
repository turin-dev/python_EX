# 48. Advanced pattern matching

Python 3.10 introduced structural pattern matching via the `match` statement.
PEP 636 provides a tutorial explaining how patterns work.  A match statement
takes a subject expression and compares it against successive patterns.  It
both checks the structure of the subject and can bind names to parts of
matched values【372741329340159†L101-L116】.  Pattern matching is similar to a
`switch` statement but more powerful: patterns can destructure sequences,
mapping types and even user‑defined classes.

## Matching sequences

You can match lists or tuples with a fixed number of elements.  The pattern
`[action, obj]` matches a sequence with exactly two elements and binds
`action` and `obj`【372741329340159†L101-L116】.  Use wildcards (`_`) to ignore
values and the star operator (`*rest`) to capture an arbitrary tail.

```python
def process(command: str) -> None:
    match command.split():
        case ["quit"]:
            print("Goodbye!")
        case ["go", direction]:
            print(f"Going {direction}")
        case [action, obj]:
            print(f"{action}ing {obj}")
        case _:
            print("Unknown command")
```

## OR patterns and literal patterns

Patterns can combine alternatives with `|` (OR patterns) or match literal
values.  For example:

```python
def classify(x: int) -> str:
    match x:
        case 0 | 1:
            return "small"
        case 2 | 3 | 5 | 7:
            return "prime"
        case _:
            return "other"
```

## Capturing subpatterns and guards

You can capture parts of a pattern with the `as` keyword or bind names inside
patterns.  Guards allow adding conditions after a pattern:

```python
match data:
    case [x, y] if x < y:
        print(f"Increasing pair: {x}, {y}")
    case [x, y]:
        print(f"Pair out of order: {x}, {y}")
```

## Matching mappings and classes

Patterns can match dictionaries by keys or user‑defined classes by matching
attributes or positional parameters.  To enable class pattern matching define
`__match_args__` on the class specifying the attributes that correspond to
positional patterns.

```python
class Point:
    __match_args__ = ("x", "y")
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


def where(p: Point) -> str:
    match p:
        case Point(0, 0):
            return "origin"
        case Point(x, y) if x == y:
            return "diagonal"
        case Point(x, y):
            return f"{x}, {y}"
        case _:
            return "unknown"
```

## Summary

Structural pattern matching enables declarative extraction of data from complex
structures.  Use match–case to simplify long chains of `if…elif` statements,
and refer to PEP 636 for a comprehensive tutorial【372741329340159†L101-L116】.
