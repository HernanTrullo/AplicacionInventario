from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from style import StyleAPP as sty
from datetime import datetime as dt
import datetime
from Licencia.Licencia import Licencia
from tkinter import simpledialog
from tkinter import messagebox

class AppLIC(ttk.Frame):
    def __init__(self, root:Tk):
        super().__init__(root)
        self.root = root
        self.style = sty(root)
        self.root.title("Licencia")
        self.root.geometry("400x300")
        
        self.var_clave = StringVar()
        self.var_fecha_ini = StringVar()
        self.var_ena_clave = BooleanVar()
        self.var_dias_pass = IntVar()
        
        self.create_widgets()
        self.pack(fill="both", expand=True)
        
        
    def create_widgets(self):
        self.lb_clave = ttk.Label(self,text="Clave", style="CustomMedium.TLabel").grid(row=2, column=1, sticky="nsew")
        self.lb_fecha_ini = ttk.Label(self,text="Fecha Inicio", style="CustomMedium.TLabel").grid(row=3, column=1,sticky="nsew")
        self.lb_habilitar_clave = ttk.Label(self,text="Habilitar Clave", style="CustomMedium.TLabel").grid(row=4, column=1,sticky="nsew")
        self.lb_habilitar_clave = ttk.Label(self,text="Días de Clave", style="CustomMedium.TLabel").grid(row=5, column=1,sticky="nsew")
        
        self.clave = ttk.Entry(self, textvariable=self.var_clave)
        self.clave.grid(row=2, column=2, sticky="ew")
        self.fecha_ini = ttk.Entry(self,textvariable=self.var_fecha_ini)
        self.fecha_ini.grid(row=3, column=2, sticky="ew")
        self.ena_clave = ttk.Checkbutton(self,variable=self.var_ena_clave)
        self.ena_clave.grid(row=4, column=2, sticky="ew")
        self.days_pass = ttk.Entry(self,textvariable=self.var_dias_pass)
        self.days_pass.grid(row=5, column=2, sticky="ew")
        
        self.btn_validar = ttk.Button(self,text="Cargar Licencia",command=self.cargar, style="Primary.TButton")
        self.btn_validar.grid(row=6, column=2, sticky="nsew")
        
        for i in range(5):
            self.rowconfigure(i, weight=1)
        
        self.rowconfigure(7, weight=3)
            
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=3)
        
        self.fecha_ini.bind("<FocusIn>", self.retornar_fecha)
        
        
    def retornar_fecha(self, event):
        date = dt.today().strftime("%Y-%m-%d")
        self.var_fecha_ini.set(date)
        
    def cargar(self):
        clave= simpledialog.askstring("LMH SOLUTIONS","      Ingrese contraseña de admin       ", parent=self)
        if clave == "434c415645444541444d494e4953545241444f523130313040323032304033303330": # Clave en hexadecimal
            clave = self.var_clave.get()
            state = self.var_ena_clave.get()
            date_ini = self.var_fecha_ini.get()
            
            dt_data = dt.strptime(date_ini,"%Y-%m-%d")
            dt_data = dt_data + datetime.timedelta(days=self.var_dias_pass.get())
            date_fin = dt_data.strftime("%Y-%m-%d")
            Licencia().set_lic(clave, state, date_ini, date_fin)
            messagebox.showinfo("LMH SOLUTIONS", "Licencia actualizada existosamente")
        else:
            messagebox.showerror("LMH SOLUTIONS", "Contraseña de administrador/soporte no válida")
            
        
        
        