from tkinter import Tk
from ctypes import windll
from src.gui import App
windll.shcore.SetProcessDpiAwareness(1)


def center_window(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    root = Tk()
    root.title("Анализатор заболоченности")
    root.configure(background="#eaeaea")
    height = 1024
    width = 768
    root.minsize(height, width)
    root.maxsize(height, width)
    root.resizable = False
    center_window(root)

    app = App(root)

    root.mainloop()
