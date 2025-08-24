# 50. Graphical user interfaces with Tkinter

Python ships with Tk/Tcl bindings accessible via the `tkinter` package.  Tk
provides a robust, cross‑platform windowing toolkit that is bundled with
Python on most systems.  The documentation notes that Tk/Tcl has long been
an integral part of Python and that `tkinter` wraps the Tk widgets as
Python classes【387040448624851†L44-L56】.  You do not need to write Tcl code
directly because `tkinter` exposes object‑oriented APIs.  Although the
default look and feel has historically been dated, Tk 8.5 introduced the
themed `ttk` widgets which greatly improve appearance【387040448624851†L55-L60】.

## Hello world window

The simplest GUI program creates a window and displays a label:

```python
import tkinter as tk

root = tk.Tk()
root.title("Hello")
label = tk.Label(root, text="Hello, Tkinter!")
label.pack(padx=20, pady=20)
root.mainloop()
```

`Tk()` creates the main application window.  Widgets are placed in the
window by calling geometry managers (`pack`, `grid` or `place`).  Call
`mainloop()` to start the event loop.

## Layout managers

Tkinter provides three layout managers: `pack` (simple stack), `grid`
(table‑like) and `place` (absolute positioning).  Use `grid` to arrange
widgets in rows and columns.

## Tk themed widgets (ttk)

The `tkinter.ttk` module provides themed widgets like `Combobox`,
`Notebook` and `Treeview` that offer a more modern appearance and
additional functionality.  Import `ttk` from `tkinter` and use themed
widgets in place of their classic equivalents.

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
tree = ttk.Treeview(root, columns=("Name", "Age"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.insert("", tk.END, values=("Alice", 30))
tree.insert("", tk.END, values=("Bob", 25))
tree.pack(fill=tk.BOTH, expand=True)
root.mainloop()
```

## Event binding

Use the `bind()` method to handle events like clicks or key presses:

```python
def on_click(event):
    print(f"Clicked at {event.x}, {event.y}")

canvas = tk.Canvas(root, width=200, height=200)
canvas.bind("<Button-1>", on_click)
canvas.pack()
```

## Summary

`tkinter` makes it easy to build simple desktop GUIs without external
dependencies.  For more complex applications consider exploring other GUI
frameworks like PyQt, wxPython or Kivy, but `tkinter` is an excellent
starting point and is available out‑of‑the‑box【387040448624851†L44-L56】.
