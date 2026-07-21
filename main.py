import tkinter as tk
from gui.app import SistemaBancarioApp

def main():
    root = tk.Tk()
    app = SistemaBancarioApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
