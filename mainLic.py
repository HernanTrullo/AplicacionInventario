from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from AppLIC import AppLIC


def main():
    root = Tk()
    app = AppLIC(root)
    app.mainloop()

if __name__ == "__main__":
    main()