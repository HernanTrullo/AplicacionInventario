from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import pandas as pd
from tkinter import messagebox
import tkinter as tk
from utilidades.ListaUsuarios import Listausuario, SOCIO
from BaseDatos.control_bd_socios import BD_Socios as BD
from BaseDatos.control_bd_variables import BD_Variables
from utilidades.excepcion import ErrorBusqueda as ExcepBus
from utilidades.EntryP import LabelP
import datetime
import utilidades.generc as utl
from tktooltip import ToolTip
from tkinter import simpledialog

class WinSocios(ttk.Frame):
    def __init__(self, root:ttk.Notebook, app):
        super().__init__(root)
        self.root = root
        
        self.app = app
        # Variables incluidas 
        self.var_nombre_op = tk.StringVar()
        self.var_fecha = tk.StringVar()
        self.var_hora = tk.StringVar()
        
        self.var_total = tk.StringVar()
        self.var_total_vendido = tk.StringVar()
        self.var_delta_time = tk.IntVar()
        self.var_buscar_cod = tk.StringVar()
        self.var_buscar_nombre = tk.StringVar()
        
        self.var_descrip_cod = tk.StringVar()
        self.var_descrip_nombre = tk.StringVar()
        
        self.foco_frame = None
        
        self.create_widget()
        
        
    def create_widget(self):
        # Frame que contiene el nombre del operario e información básica
        self.top_frame = ttk.Frame(self, style="Cabecera.TFrame")
        
        self.nameFrame = ttk.Label(self.top_frame, text="Bienvenido: ", style="CCustomLarge.TLabel")
        self.nameFrame.grid(row=0, column=0)
        self.nombre_op = ttk.Label(self.top_frame, textvariable=self.var_nombre_op, style="CCustomMedium.TLabel")
        self.nombre_op.grid(row=0, column=1)
        
        self.lb_fecha = ttk.Label(self.top_frame, text="Fecha: ", style="CCustomLarge.TLabel")
        self.lb_fecha.grid(row=1,column=0)
        self.fecha = ttk.Label(self.top_frame, textvariable=self.var_fecha,style="CCustomSmall.TLabel")
        self.fecha.grid(row=1, column=1)
        
        self.lb_hora = ttk.Label(self.top_frame, text="Hora: ", style="CCustomLarge.TLabel")
        self.lb_hora.grid(row=2, column=0)
        self.hora = ttk.Label(self.top_frame, textvariable=self.var_hora, style="CCustomSmall.TLabel")
        self.hora.grid(row=2, column=1)
        
        self.lb_hora = ttk.Label(self.top_frame, text="Dias de Licencia Restantes: ", style="CCustomLarge.TLabel")
        self.lb_hora.grid(row=2, column=2)
        self.hora = ttk.Label(self.top_frame, textvariable=self.var_delta_time, style="CCustomLarge.TLabel")
        self.hora.grid(row=2, column=3)
        
        self.top_frame.grid(row=0,column=0, sticky="nsew")
        
        # Agregar fecha y hora
        self.var_fecha.set(datetime.date.today().strftime('%d/%m/%Y'))
        self.actualizar_hora()
        
        # Frame del buscar de datos
        self.ingreso_datos = ttk.Frame(self)
        
        self.lb_codigo = ttk.Label(self.ingreso_datos, text="Cedula", style="CustomSmall.TLabel").grid(row=0, column=0)
        
        self.entry_codigo = ttk.Entry(self.ingreso_datos, textvariable=self.var_buscar_cod,style="Custom.TEntry")
        self.entry_codigo.grid(row=1, column=0,sticky="nsew")
        self.entry_codigo.bind("<Return>", self.buscar_socio)
        
        self.lb_nombre_user = ttk.Label(self.ingreso_datos, text="Nombre",style="CustomSmall.TLabel").grid(row=0, column=1)
        self.entry_nombre = ttk.Combobox(self.ingreso_datos, textvariable=self.var_buscar_nombre)
        self.entry_nombre.grid(row=1, column=1,sticky="nsew")
        self.entry_nombre.bind("<KeyRelease>", self.actualizar_nombre_usuarios)
        self.entry_nombre.bind("<Return>", self.buscar_socio)
        
        # guardar foco del frame
        self.entry_codigo.bind("<FocusIn>", self.controlador_de_foco)
        self.entry_nombre.bind("<FocusIn>", self.controlador_de_foco)
        
        self.expandir_widget(self.ingreso_datos, colum=3)
        self.ingreso_datos.grid(row=1, column=0,sticky="nsew",pady=20)
        
        # Frame descripción del producto (Compra)
        self.frame_descrip_producto = ttk.Frame(self)
        
        self.lb_cod_descrp_user = ttk.Label(self.frame_descrip_producto, text="Cédula", style="CustomSmall.TLabel")
        self.lb_cod_descrp_user.grid(row=0, column=0,sticky="nsew")
        self.entry_cod_descrp_user = ttk.Entry(self.frame_descrip_producto, textvariable=self.var_descrip_cod)
        self.entry_cod_descrp_user.grid(row=1, column=0,sticky="nsew")
        
        self.lb_nombre_descrp_user = ttk.Label(self.frame_descrip_producto, text="Nombre",style="CustomSmall.TLabel")
        self.lb_nombre_descrp_user.grid(row=0, column=1,sticky="nsew")
        self.entry_nombre_descrp_user = ttk.Entry(self.frame_descrip_producto, textvariable=self.var_descrip_nombre)
        self.entry_nombre_descrp_user.grid(row=1, column=1,sticky="nsew") # Entry
        
        #self.cambiar_widget()
        self.frame_descrip_producto.grid(row=2, column=0,sticky="nsew")
        self.expandir_widget(self.frame_descrip_producto, colum=4)
        
        
        # Frame Botones
        self.frame_botones = ttk.Frame(self)
        self.img_mod = utl.leer_imagen("./Imagenes/BTN_Modificar.png", (24,24))
        self.img_add = utl.leer_imagen("./Imagenes/BTN_Agregar.png", (24,24))
        self.img_per = utl.leer_imagen("./Imagenes/BTN_Agregar.png", (24,24))
        
        self.btn_agregar = ttk.Button(self.frame_botones, image=self.img_add, style="Primary.TButton",command=self.agregar_socio)
        self.btn_agregar.grid(row=0, column=3, pady=10)  
        self.btn_modificar = ttk.Button(self.frame_botones, image=self.img_mod,style="Primary.TButton" ,command=self.modificar_socio)
        self.btn_modificar.grid(row=0, column=2)
        
        # Se configuran los tooltip
        ToolTip(self.btn_agregar, "Agregar Producto", delay=0.5)
        ToolTip(self.btn_modificar, "Modificar Producto", delay=0.5)
        
        self.frame_botones.columnconfigure(0, weight= 7)
        self.frame_botones.columnconfigure(4, weight= 1)
        self.frame_botones.grid(row=3, column=0, sticky="nsew")
        
        
        # Frame lista de productos
        self.frame_lista_producto = ttk.Frame(self)
        self.win_lista_producto = Listausuario(self.frame_lista_producto, self,[SOCIO.cedula, SOCIO.nombre, SOCIO.total_cartera, SOCIO.total_comprado])
        self.frame_lista_producto.grid(row=4, column=0, sticky="nsew")
        
        
        # Bóton para cargar los datos al inventario, salir y log out y cambio de clave
        self.frame_inventario = ttk.Frame(self)
        
        self.btn_cargar_inventario = ttk.Button(self.frame_inventario, text="Cargar Datos Usuario", command=self.cargar_usuario_mod,style="Primary.TButton")
        self.btn_cargar_inventario.grid(row=0,column=0, sticky="nsew")
        
        self.btn_salir  = ttk.Button(self.frame_inventario, text="Salir",command=self.salir, style="Primary.TButton")
        self.btn_salir.grid(row=1, column=0,sticky="nsew")
        
        self.btn_log_out  = ttk.Button(self.frame_inventario, text="Cerrar Sesión",command=self.log_out, style="Primary.TButton")
        self.btn_log_out.grid(row=3, column=0,sticky="nsew")
        
        self.btn_cambiar_clave  = ttk.Button(self.frame_inventario, text="Abonar",command=self.abonar, style="Primary.TButton")
        self.btn_cambiar_clave.grid(row=2, column=0,sticky="nsew")
        
        self.expandir_widget(self.frame_inventario, row=4, colum=1)
        self.frame_inventario.grid(row=0, column=1, rowspan=5, sticky="nsew")
        
        ## Configurar el frame principal del operario
        self.rowconfigure(4, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        
    
    def abonar(self):
        pass
    
    def log_out(self):
        pass
    
    def cargar_usuario_mod(self):
        
        pass
    
    def salir(self):
        pass
    
    def agregar_socio(self):
        user = {
            SOCIO.cedula: self.var_descrip_cod.get(),
            SOCIO.nombre: self.var_descrip_nombre.get(),
            SOCIO.total_comprado: 0,
            SOCIO.total_cartera: 0
        }
        messaje = f"Está seguro que desea agregar el usuario {user[SOCIO.nombre]}?"
        resp = messagebox.askokcancel("SOFTRU SOLUCIONS", messaje)
        if resp:
            BD.agregar_socio(user)
            messaje = "¡Socio agregado correctamente!"
            messagebox.showinfo("SOFTRU SOLUCIONS", messaje)
    
    def modificar_socio(self):
        pass
    
    
    def actualizar_hora(self):
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        self.var_hora.set(hora_actual)
        self.after(1000, self.actualizar_hora)
    
    def expandir_widget(self, frame:ttk.LabelFrame, row=2, colum=2):
        for i in range(row):
            frame.rowconfigure(i, weight=1)
        for i in range(colum):
            frame.columnconfigure(i, weight=1)
            
    def controlador_de_foco(self, event):
        self.foco_frame = event.widget
            
    def actualizar_nombre_usuarios(self, event):
        try:
            self.entry_nombre['values']=BD.retornar_nombres_socios(self.var_buscar_nombre.get())     
        except:
            self.entry_nombre['values'] = [""]
    
    def buscar_socio(self, event):
        if self.foco_frame == self.entry_codigo or self.foco_frame == self.entry_nombre:
            try:
                if self.foco_frame == self.entry_codigo:
                    values = BD.buscar_socio_cedula(self.var_buscar_cod.get())   
                    self.var_descrip_cod.set(values[0])
                    
                elif self.foco_frame == self.entry_nombre:
                    values = BD.buscar_socio_nombre(self.var_buscar_nombre.get())
                    self.var_descrip_cod.set(values[0])
                        
            except  ExcepBus as e:  
                respuesta=messagebox.askokcancel("SOFTRULLO SOLUCIONS", "Cédula o nombre no encontrado. ¿Desea agregar un nuevo usuario?")
                if respuesta:
                    if self.foco_frame == self.entry_codigo:
                        self.cambiar_widget(2)
                        self.limpiar_variables()
                        self.var_descrip_cod.set(self.var_buscar_cod.get())
                    elif self.foco_frame == self.entry_nombre:
                        self.cambiar_widget(1)
                        self.limpiar_variables()
                        self.var_descrip_nombre.set(self.var_buscar_nombre.get())
                        
            self.var_buscar_cod.set("")
            self.var_buscar_nombre.set("")
    
    def cambiar_widget(self, comand=0):
        if comand==0:
            # Se dejan todo desactivados
            pass
        elif comand ==1:
            # Se activan todos menos la cedula
            pass
    
    def limpiar_variables(self):
        pass
    
    
        