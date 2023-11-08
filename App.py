from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from Logeo.Logeo import WinLogeo
from Operario.Operario import WinOperario
from Admin.Admin import WinAdmin
from tkinter import messagebox
from style import StyleAPP as sty
from Registro.Registro import WinRegistro
from Inventario.Inventario import WinInventario
from Socios.Socios import WinSocios


GLOBAL_user_valido = False
class App(ttk.Frame):
    def __init__(self, root:Tk, delta_time):
        super().__init__(root)
        self.root = root
        self.delta_time = delta_time
        self.style = sty(root)
        self.root.title("Aplicación de Usuario")
        #self.root.attributes("-toolwindow", True)
        #self.root.attributes("-topmost", True,"-toolwindow", True)
        self.root.state("zoomed")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.create_widgets()
        self.pack(fill="both", expand=True)

    def on_close(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            self.root.destroy()
    
    
    def create_widgets(self):
        self.notebook_windows = ttk.Notebook(self)
        
        # Se crean las instancias de cada ventana y se agregan al notebook
        self.win_logeo = WinLogeo(self.notebook_windows, self)
        self.win_admin = WinAdmin(self.notebook_windows, self)
        self.win_operario = WinOperario(self.notebook_windows, self)
        self.win_registro = WinRegistro(self.notebook_windows, self)
        self.win_inventario = WinInventario(self.notebook_windows, self)
        self.win_socios = WinSocios(self.notebook_windows, self)
        
        # Se asigna cada ventana al notebook_window
        self.notebook_windows.add(self.win_logeo, text="Logeo", padding=5)
        self.notebook_windows.add(self.win_operario, text="Ventas y Operario", padding=5,state="hidden")
        self.notebook_windows.add(self.win_admin, text="Administrador", padding=5, state="hidden")
        self.notebook_windows.add(self.win_registro, text="Registro", padding=5, state="hidden")
        self.notebook_windows.add(self.win_inventario, text="Inventario", padding=5, state="hidden")
        self.notebook_windows.add(self.win_socios, text="Afiliados", padding=5, state= "hidden")
        
        self.notebook_windows.pack(fill="both", expand=True)
        
        
    

