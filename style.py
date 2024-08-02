from tkinter import ttk
from tkinter import *
from tkinter.ttk import *

class StyleAPP:
    def __init__(self, root) -> None:
        
        bg_gen= "#5C1499"
        cl_letter = "#4D4D4D" 
        bg_lb_gen = "white"
        
        bg_lb_cab = "#5C1499"
        fr_lb_cab = "white"
        
        bg_btn = "#5C1499"
        bg_btn_var = '#9A75BF'
        fr_btn = "white"
        
        bg_entry_dis = '#9A75BF'
        
        self.style = ttk.Style(root)
        self.style.theme_use("default")
        self.style.configure('TButton', width=20,borderwidth=1)
        self.style.configure("CustomFrame.TLabel", background=bg_gen, borderwidth=0)
        
        # Estilos para los botones
        self.style.configure("Primary.TButton", background=bg_btn, foreground=fr_btn,font=("Roboto", 13))
        self.style.map('TButton',
                background=[('pressed', bg_btn),
                            ('active', bg_btn_var)]
        )
        # Estilos del Notebook
        self.style.configure("TNotebook", background="white")
        self.style.configure("TFrame", background="white" )
        
        # Estilo TFRAME de cabecera
        self.style.configure("Cabecera.TFrame", background=bg_gen)
        
        self.style.configure("TCombobox",
                fieldbackground="white",
                background= bg_gen,
                arrowcolor="white")
        
        self.style.configure(
                "TProgressbar",
                background= bg_gen)
        
        ## Estilos para los label general
        self.style.configure("CustomMedium.TLabel", foreground=cl_letter, background=bg_lb_gen, font=("Roboto", 15))
        self.style.configure("CustomSmall.TLabel", foreground=cl_letter, background=bg_lb_gen,font=("Roboto", 13))
        self.style.configure("CustomLarge.TLabel", foreground=cl_letter, background=bg_lb_gen,font=("Roboto", 20))
        self.style.configure("Clickable.TLabel",foreground=cl_letter, background=bg_lb_gen,font=("Roboto", 13))
        self.style.map("Clickable.TLabel",
                    foreground=[('pressed', cl_letter),
                            ('active', bg_gen)],
                    background=[
                        ('pressed', bg_lb_gen),
                            ('active', bg_lb_gen)
                    ]    
        )
        
        ## Estilos para los label cabecera
        self.style.configure("CCustomMedium.TLabel", foreground=fr_lb_cab, background=bg_lb_cab, font=("Roboto", 15))
        self.style.configure("CCustomSmall.TLabel", foreground=fr_lb_cab, background=bg_lb_cab,font=("Roboto", 13))
        self.style.configure("CCustomLarge.TLabel", foreground=fr_lb_cab, background=bg_lb_cab,font=("Roboto", 20))
        self.style.configure("CErrorCustomMedium.TLabel", foreground="red", background=bg_lb_cab, font=("Roboto", 15))
        
        
        # Estilo para el treeview
        self.style.configure("Treeview", background="white")
        
        
        # Estilos para los entry 
        self.style.configure("TEntry", foreground="black")
        
        self.style.configure("Custom.TButton", foreground="blue", font=("Roboto", 16))
        self.style.configure("CustomOperacion.TButton", foreground="blue", font=("Roboto", 12))
        self.style.configure("CustomQuit.TButton", foreground="red", font=("Roboto", 16))
        
        self.style.configure("Custom13.TLabel", foreground="black", font=("Roboto", 13))
        self.style.configure("CustomError.TLabel", foreground="red", font=("Roboto", 16))
        
        self.style.configure("Clickable2.TLabel", background="white",foreground="blue",font=("Roboto", 14))
        self.style.configure("RoundedButton.TButton", background="lightblue")
        