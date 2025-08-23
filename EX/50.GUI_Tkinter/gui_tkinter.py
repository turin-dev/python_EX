"""
Simple Tkinter GUI examples.
"""

import tkinter as tk
from tkinter import ttk


def hello_window() -> None:
    root = tk.Tk()
    root.title("Hello")
    label = tk.Label(root, text="Hello, Tkinter!")
    label.pack(padx=20, pady=20)
    root.mainloop()


def treeview_demo() -> None:
    root = tk.Tk()
    root.title("Treeview Demo")
    tree = ttk.Treeview(root, columns=("Name", "Age"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.insert("", tk.END, values=("Alice", 30))
    tree.insert("", tk.END, values=("Bob", 25))
    tree.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


def click_canvas() -> None:
    root = tk.Tk()
    root.title("Click Me")
    canvas = tk.Canvas(root, width=200, height=200, bg="white")

    def on_click(event: tk.Event) -> None:
        print(f"Clicked at {event.x}, {event.y}")
        # Draw a small circle where the click occurred
        r = 3
        canvas.create_oval(event.x - r, event.y - r, event.x + r, event.y + r, fill="black")

    canvas.bind("<Button-1>", on_click)
    canvas.pack()
    root.mainloop()


if __name__ == "__main__":
    # Show different demos based on user choice
    import sys

    demos = {
        "hello": hello_window,
        "tree": treeview_demo,
        "click": click_canvas,
    }
    choice = sys.argv[1] if len(sys.argv) > 1 else "hello"
    if choice in demos:
        demos[choice]()
    else:
        print("Available demos:", ", ".join(demos))