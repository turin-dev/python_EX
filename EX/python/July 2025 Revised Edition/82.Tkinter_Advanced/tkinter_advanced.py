"""Advanced Tkinter GUI demonstrating frames, events and canvas drawing."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def main() -> None:
    root = tk.Tk()
    root.title("Advanced Tkinter Demo")

    # top frame with a label and entry
    top_frame = ttk.Frame(root, padding=10)
    top_frame.pack(side=tk.TOP, fill=tk.X)
    ttk.Label(top_frame, text="Enter text:").pack(side=tk.LEFT)
    entry = ttk.Entry(top_frame)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # middle frame with a canvas
    middle_frame = ttk.Frame(root)
    middle_frame.pack(fill=tk.BOTH, expand=True)
    canvas = tk.Canvas(middle_frame, width=300, height=200, background="white")
    canvas.pack(fill=tk.BOTH, expand=True)

    def draw_circle(event) -> None:
        x, y = event.x, event.y
        canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue")

    canvas.bind("<Button-1>", draw_circle)

    # bottom frame with a listbox and button
    bottom_frame = ttk.Frame(root, padding=10)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
    listbox = tk.Listbox(bottom_frame, height=5)
    listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def add_item() -> None:
        text = entry.get()
        if text:
            listbox.insert(tk.END, text)
            entry.delete(0, tk.END)

    ttk.Button(bottom_frame, text="Add", command=add_item).pack(side=tk.LEFT)

    root.mainloop()


if __name__ == "__main__":
    main()