from tkinter import ttk
import tkinter as tk


class LabelP(ttk.Label):
    def __init__(self, root:ttk.Frame, textvariable, style):
        self.root = root
        super().__init__(root, text="$0.00",style=style)
        self.text_variable = textvariable
        
    def formatear_valor(self):
        value = float(self.text_variable.get())
        self.configure(text=f"{self.format_currency(value)}")
        
    
    def format_currency(self,value):
        return "${:,.2f}".format(value)