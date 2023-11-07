from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import utilidades.generc as utl
from BaseDatos.control_bd_logeo import BD_Usuario
from tkinter import messagebox
from tkinter import simpledialog
import tkinter as tk


class WinRegistro(ttk.Frame):
    def __init__(self, root:ttk.Notebook, app):
        super().__init__(root)
        self.root = root
        self.app = app
        self.create_widget()
        self.pack(fill="both", expand=True)
        
    def create_widget(self):
        self.imagen = utl.leer_imagen("./Imagenes/LogoEmpresa.png", (479,285))
        self.logo = ttk.Label(self,image=self.imagen, style="CustomFrame.TLabel")
        self.logo.grid(row=0, column=0, sticky="nsew")
        
        # Variables del modulo de registro
        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_user = tk.StringVar()
        self.var_pass = tk.StringVar()
        self.var_es_admin = tk.BooleanVar()
        
        # Frame que contiene los widgets de registro
        self.frame_opciones_registro = ttk.Frame(self)
        self.frame_opciones_registro.grid(row=0, column=1, sticky="nsew")
        
        self.lb_nombre = ttk.Label(self.frame_opciones_registro, text="Nombre", style="CustomSmall.TLabel").grid(row=0, column=1, sticky="e",padx=20)
        self.lb_apellido = ttk.Label(self.frame_opciones_registro, text="Apellido",style="CustomSmall.TLabel").grid(row=1, column=1,sticky="e",padx=20)
        self.lb_admin = ttk.Label(self.frame_opciones_registro, text="Es Admin",style="CustomSmall.TLabel").grid(row=2, column=2,sticky="e",padx=20)
        self.lb_user = ttk.Label(self.frame_opciones_registro, text="Usuario",style="CustomSmall.TLabel").grid(row=3, column=1,sticky="e",padx=20)
        self.lb_pass = ttk.Label(self.frame_opciones_registro, text="Contraseña",style="CustomSmall.TLabel").grid(row=4, column=1,sticky="e", padx=20)
        
        self.nombre = ttk.Entry(self.frame_opciones_registro,textvariable=self.var_nombre)
        self.nombre.grid(row=0, column=2,columnspan=2,sticky="we")
        self.apellido = ttk.Entry(self.frame_opciones_registro, textvariable=self.var_apellido)
        self.apellido.grid(row=1, column=2,columnspan=2,sticky="we")
        self.admin = ttk.Checkbutton(self.frame_opciones_registro, variable=self.var_es_admin)
        self.admin.grid(row=2, column=1)
        self.user = ttk.Entry(self.frame_opciones_registro, textvariable=self.var_user)
        self.user.grid(row=3, column=2,columnspan=2,sticky="we")
        self.password = ttk.Entry(self.frame_opciones_registro,textvariable=self.var_pass,show="*")
        self.password.grid(row=4, column=2,columnspan=2,sticky="we")
        
        
        self.btn_registro = ttk.Button(self.frame_opciones_registro, text="Registrarse", command=self.registrar_usuario, style="Primary.TButton")
        self.btn_registro.grid(row=5, column=3, sticky="nsew")
        
        self.frame_opciones_registro.columnconfigure(0, weight=2)
        self.frame_opciones_registro.columnconfigure(3, weight=2)
        self.frame_opciones_registro.columnconfigure(4, weight=3)
        
        for i in range(6):
            self.frame_opciones_registro.rowconfigure(i, weight=1)    
        self.frame_opciones_registro.rowconfigure(7, weight=5)
    
        
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=4)
        
    def registrar_usuario(self):
        if (len(self.var_nombre.get())>0 and len(self.var_apellido.get()) >0 and len(self.var_user.get()) > 0 and len(self.var_pass.get()) > 0):
            BD_Usuario.add_user(self.var_nombre.get(), self.var_apellido.get(), self.var_user.get(),self.var_pass.get(), self.var_es_admin.get()) 
            messagebox.showinfo("SOFTRULLO SOLUCIONS", "¡Usuario registrado correctamente!")
            notebok_tabs= self.root.tabs()
            self.root.tab(notebok_tabs[3], state="hidden")
            self.root.select(notebok_tabs[0])
            self.limpiar_entries()
            
        else:
            messagebox.showerror("SOFTRULLO SOLUCIONS", "¡Los campos deben estar introducidos correctamente!")
            
    def limpiar_entries(self):
        self.var_nombre.set("")
        self.var_apellido.set("")
        self.var_user.set("")
        self.var_pass.set("")
        self.var_es_admin.set(False)
        
    