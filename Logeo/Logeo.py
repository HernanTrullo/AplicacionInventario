from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import utilidades.generc as utl
from BaseDatos.control_bd_logeo import BD_Usuario
from tkinter import messagebox
from tkinter import simpledialog

class WinLogeo(ttk.Frame):
    def __init__(self, root:ttk.Notebook, app):
        super().__init__(root)
        self.root = root
        self.app = app
        self.create_widget()
        self.pack(fill="both", expand=True)
        
        
    def create_widget(self):
        self.imagen = utl.leer_imagen("./Imagenes/LogoEmpresa.png", (400,800))
        self.logo = ttk.Label(self,image=self.imagen)
        self.logo.grid(row=0,column=0, sticky="nsew")
        
        
        self.frame_logeo = ttk.Frame(self)
        self.frame_logeo.grid(row=0,column=1,sticky="nsew")
        self.nameFrame = ttk.Label(self.frame_logeo, text="¡Bienvenido al inicio de sesión!", style="Custom.TLabel")
        self.nameFrame.pack(fill=X, pady=160, padx=20)
        
        # Usuario
        self.lb_user = ttk.Label(self.frame_logeo, text="Usuario", style="Custom.TLabel")
        self.lb_user.pack(fill=X,padx=20, pady=5)
        self.entry_user = ttk.Entry(self.frame_logeo)
        self.entry_user.pack(fill=X,padx=20, pady=5)
        
        # Contraseña
        self.lb_pass = ttk.Label(self.frame_logeo, text="Contraseña", style="Custom.TLabel")
        self.lb_pass.pack(fill=X, padx=20, pady=5)
        self.entry_pass = ttk.Entry(self.frame_logeo, show="*")
        self.entry_pass.pack(fill=X,padx=20, pady=5)
        # Botón de acceso
        self.btn_ingresar = ttk.Button(self.frame_logeo, text="Ingresar", style="Custom.TButton", command=self.login)
        self.btn_ingresar.pack(padx=50, pady=50)
        # Etiqueta de registro
        self.btn_registro = ttk.Button(self.frame_logeo, text="Registrase", style="Clickable.TLabel", command=self.singup)
        self.btn_registro.pack()
        
        
        
        # Funciones que crean la apariencia cuando el cursor se para encima
        self.btn_registro.bind("<Enter>", self.on_enter)
        self.btn_registro.bind("<Leave>", self.on_leave)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        
        
    def login(self):
        try:
            resp = BD_Usuario().es_admin(self.entry_user.get(), self.entry_pass.get())
            if resp[0]:
                notebok_tabs= self.root.tabs()
                self.root.tab(notebok_tabs[4], state="normal")
                self.root.tab(notebok_tabs[2], state="normal")
                self.root.tab(notebok_tabs[1], state="normal")
                self.root.tab(notebok_tabs[0], state="hidden")
                self.root.select(notebok_tabs[2])
                
                dato = resp[1]
                self.app.win_operario.var_nombre_op.set(f"{dato[0]} {dato[1]}")
                self.app.win_admin.var_nombre_op.set(f"{dato[0]} {dato[1]}")
                self.app.win_inventario.var_nombre_op.set(f"{dato[0]} {dato[1]}")
            else:
                notebok_tabs= self.root.tabs()
                self.root.tab(notebok_tabs[1], state="normal")
                self.root.tab(notebok_tabs[0], state="hidden")
                self.root.select(notebok_tabs[1])
                self.app.win_operario.var_nombre_op.set(f"{dato[0]} {dato[1]}")
                self.app.win_inventario.var_nombre_op.set(f"{dato[0]} {dato[1]}")
        except:
            messagebox.showerror("SOFTTRULLO SOLUCIONES", "Usuario y/o contraseña no válidos")
            
        self.clean_entries()
        
    def singup(self):
        clave= simpledialog.askstring("SOFTRULLO SOLUCIONS","      Ingrese contraseña de admin       ", parent=self)
        if clave == "434c415645444541444d494e4953545241444f523130313040323032304033303330": # Clave en hexadecimal
            notebok_tabs= self.root.tabs()
            self.root.tab(notebok_tabs[3], state="normal")
            self.root.select(notebok_tabs[3])
        else:
            messagebox.showinfo("SOFTRULLO SOLUCIONS", "Contraseña de administrador/soporte no válida")
        
        self.clean_entries()
            
    
    def clean_entries(self):
        self.entry_user.delete(0,END) 
        self.entry_pass.delete(0,END)
        
       
    def on_enter(self,event):
        self.btn_registro.configure(style="Clickable2.TLabel")

    def on_leave(self,event):
        self.btn_registro.configure(style="Clickable.TLabel")
        
        