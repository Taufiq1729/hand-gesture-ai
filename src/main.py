import tkinter as tk
from gui import GestureApp

def main():
    """Launches the Gesture AI Control GUI."""
    root = tk.Tk()
    app = GestureApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
