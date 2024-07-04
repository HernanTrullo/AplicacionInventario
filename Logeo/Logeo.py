from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import utilidades.generc as utl
from BaseDatos.control_bd_logeo import BD_Usuario
from tkinter import messagebox
from tkinter import simpledialog
from BaseDatos.control_bd_variables import BD_Variables

class WinLogeo(ttk.Frame):
    def __init__(self, root:ttk.Notebook, app):
        super().__init__(root)
        self.root = root
        self.app = app
        self.create_widget()
        self.pack(fill="both", expand=True)
        
        
    def create_widget(self):
        self.imagen = utl.leer_imagen("./Imagenes/LogoEmpresa.png", (493,495))
        self.logo = ttk.Label(self,image=self.imagen, style="CustomFrame.TLabel")
        self.logo.grid(row=0, column=0, sticky="nsew")
        
        
        self.frame_logeo = ttk.Frame(self)
        self.frame_logeo.grid(row=0,column=1,sticky="nsew")
        self.nameFrame = ttk.Label(self.frame_logeo, text="¡Bienvenido!", style="CustomLarge.TLabel")
        self.nameFrame1 = ttk.Label(self.frame_logeo, text="Inicio de Sesión", style="CustomMedium.TLabel")
        self.nameFrame.grid(row=1, column=1, sticky="w")
        self.nameFrame1.grid(row=2, column=1,sticky="w")
        
        # Usuario
        self.lb_user = ttk.Label(self.frame_logeo, text="Usuario", style="CustomSmall.TLabel")
        self.lb_user.grid(row=4, column=1, sticky="w",pady=10)
        self.entry_user = ttk.Entry(self.frame_logeo)
        self.entry_user.grid(row=5, column=1, sticky="ew")
        
        # Contraseña
        self.lb_pass = ttk.Label(self.frame_logeo, text="Contraseña", style="CustomSmall.TLabel")
        self.lb_pass.grid(row=6, column=1,sticky="w",pady=10)
        self.entry_pass = ttk.Entry(self.frame_logeo, show="*")
        self.entry_pass.grid(row=7, column=1,sticky="ew")
        
        # Botón de acceso
        self.btn_ingresar = ttk.Button(self.frame_logeo, text="Ingresar",command=self.login, style="Primary.TButton")
        self.btn_ingresar.grid(row=9, column=1, sticky="w", pady=5)
        # Etiqueta de registro
        self.btn_registro = ttk.Button(self.frame_logeo, text="Registrase", style="Clickable.TLabel",command=self.singup)
        self.btn_registro.grid(row=10, column=1, sticky="w", pady=20)
        
        # Diseño del panel user
        self.frame_logeo.columnconfigure(0, weight=1)
        self.frame_logeo.columnconfigure(1, weight=2)
        self.frame_logeo.columnconfigure(2, weight=1)
        
        self.frame_logeo.rowconfigure(0, weight=3)
        self.frame_logeo.rowconfigure(3, weight=1)
        self.frame_logeo.rowconfigure(8, weight=1)
        self.frame_logeo.rowconfigure(11, weight=2)
        
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)
        
        
    def login(self):
        try:
            resp = BD_Usuario().es_admin(self.entry_user.get(), self.entry_pass.get())
            if resp[0]:
                notebok_tabs= self.root.tabs()
                self.root.tab(notebok_tabs[5], state="normal") # Afiliados
                self.root.tab(notebok_tabs[4], state="normal") # Inventario
                self.root.tab(notebok_tabs[2], state="normal") # Admin
                self.root.tab(notebok_tabs[1], state="normal") # Operario
                self.root.tab(notebok_tabs[0], state="hidden") # Logeo
                self.root.select(notebok_tabs[2])
                
                dato = resp[1]
                # Se setea el nombre del operario
                self.app.win_operario.var_nombre_op.set(f"{dato[0]} {dato[1]}")
                self.app.win_admin.var_nombre_op.set(f"{dato[0]} {dato[1]}")
                self.app.win_inventario.var_nombre_op.set(f"{dato[0]} {dato[1]}")
                self.app.win_socios.var_nombre_op.set(f"{dato[0]} {dato[1]}")
                
                # Se setean los dias faltantes
                self.app.win_operario.var_delta_time.set(self.app.delta_time)
                self.app.win_admin.var_delta_time.set(self.app.delta_time)
                self.app.win_inventario.var_delta_time.set(self.app.delta_time)
                self.app.win_socios.var_delta_time.set(self.app.delta_time)
            else:
                notebok_tabs= self.root.tabs()
                self.root.tab(notebok_tabs[5], state="normal") # Afiliados
                self.root.tab(notebok_tabs[4], state="normal") # Inventario
                self.root.tab(notebok_tabs[1], state="normal") #Operario
                self.root.tab(notebok_tabs[0], state="hidden") #Logeo
                
                self.root.select(notebok_tabs[1])
                # Se setea el nombre del operario
                dato = resp[1]
                self.app.win_operario.var_nombre_op.set(f"{dato[0]} {dato[1]}")
                self.app.win_inventario.var_nombre_op.set(f"{dato[0]} {dato[1]}")
                self.app.win_socios.var_nombre_op.set(f"{dato[0]} {dato[1]}")
                
                self.app.win_operario.var_delta_time.set(self.app.delta_time)
                self.app.win_inventario.var_delta_time.set(self.app.delta_time)
                self.app.win_socios.var_delta_time.set(self.app.delta_time)
        except:
            messagebox.showerror("LMH SOLUTIONS", "Usuario y/o contraseña no válidos")
        
        self.clean_entries()
        
    def singup(self):
        clave= simpledialog.askstring("LMH SOLUTIONS","      Ingrese contraseña de admin       ", parent=self)
        if clave == BD_Variables.get_clave_admin(): # Clave en hexadecimal
            notebok_tabs= self.root.tabs()
            self.root.tab(notebok_tabs[3], state="normal")
            self.root.select(notebok_tabs[3])
        else:
            messagebox.showinfo("LMH SOLUTIONS", "Contraseña de administrador/soporte no válida")
        
        self.clean_entries()
            
    
    def clean_entries(self):
        self.entry_user.delete(0,END) 
        self.entry_pass.delete(0,END)
        
        