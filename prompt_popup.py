#!/usr/bin/env python3

import sys
import time
import tkinter as tk
from tkinter import simpledialog


def center_window(win: tk.Toplevel) -> None:
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = max((sw - w) // 2, 0)
    y = max((sh - h) // 2, 0)
    win.geometry(f"{w}x{h}+{x}+{y}")


def main() -> int:
    # Initialize a hidden root for dialogs
    root = tk.Tk()
    root.withdraw()

    try:
        # GUI input dialog
        text = simpledialog.askstring("Input", "Enter text to display:", parent=root)
    except Exception as e:
        print(f"Failed to show input dialog: {e}")
        return 1

    if text is None:
        print("Canceled. No text entered.")
        return 0

    if not str(text).strip():
        print("Empty input. Nothing to display.")
        return 0

    # Create a separate popup window with black background
    win = tk.Toplevel(root)
    win.title("Prompt")
    win.configure(bg="black")
    win.attributes("-topmost", True)
    win.resizable(False, False)

    # Esc closes early
    win.bind("<Escape>", lambda e: win.destroy())

    # Display label with white text on black background
    lbl = tk.Label(
        win,
        text=str(text),
        font=("Consolas", 18),
        fg="white",
        bg="black",
        wraplength=800,
        justify="center",
        padx=24,
        pady=16,
    )
    lbl.pack()

    # Layout stabilization and centering
    center_window(win)

    # Auto-close after 5 seconds
    win.after(5000, win.destroy)

    # Start the modal-like loop for the popup, then cleanly exit
    try:
        win.grab_set()  # Make it behave like a modal prompt
    except Exception:
        pass

    try:
        root.mainloop()
    finally:
        try:
            root.destroy()
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
