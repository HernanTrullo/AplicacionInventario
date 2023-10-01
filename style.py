from tkinter import ttk
from tkinter import *
from tkinter.ttk import *

class StyleAPP:
    def __init__(self) -> None:
        ttk.Style().configure("Custom.TButton", foreground="blue", font=("Helvetica", 16))
        ttk.Style().configure("CustomOperacion.TButton", foreground="blue", font=("Helvetica", 12))
        ttk.Style().configure("CustomQuit.TButton", foreground="red", font=("Helvetica", 16))
        ttk.Style().configure("Custom.TLabel", foreground="black", font=("Helvetica", 16))
        ttk.Style().configure("CustomError.TLabel", foreground="red", font=("Helvetica", 16))
        ttk.Style().configure("Clickable.TLabel", background="white",font=("Helvetica", 14))
        ttk.Style().configure("Clickable2.TLabel", background="white",foreground="blue",font=("Helvetica", 14))