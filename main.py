from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from App import App
from datetime import datetime as dt


def main():
    root = Tk()
    app = App(root, float("inf"))
    app.mainloop()

if __name__ == "__main__":
    main()

