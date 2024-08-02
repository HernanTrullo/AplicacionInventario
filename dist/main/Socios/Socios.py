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
from TopLevels.WinInformeSocios import TopLevelInformeSocios as WinInformeSocios

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
        
        # Frame descripción del usuario
        self.frame_descrip_socio = ttk.Frame(self)
        
        self.lb_cod_descrp_user = ttk.Label(self.frame_descrip_socio, text="Cédula", style="CustomSmall.TLabel")
        self.lb_cod_descrp_user.grid(row=0, column=0,sticky="nsew")
        self.entry_cod_descrp_user = ttk.Entry(self.frame_descrip_socio, textvariable=self.var_descrip_cod)
        self.entry_cod_descrp_user.grid(row=1, column=0,sticky="nsew")
        
        self.lb_nombre_descrp_user = ttk.Label(self.frame_descrip_socio, text="Nombre",style="CustomSmall.TLabel")
        self.lb_nombre_descrp_user.grid(row=0, column=1,sticky="nsew")
        self.entry_nombre_descrp_user = ttk.Entry(self.frame_descrip_socio, textvariable=self.var_descrip_nombre)
        self.entry_nombre_descrp_user.grid(row=1, column=1,sticky="nsew") # Entry
        
        #self.cambiar_widget() row=2, column=0,sticky="nsew"
        self.expandir_widget(self.frame_descrip_socio, colum=4)
        
        
        # Frame Botones
        self.frame_botones = ttk.Frame(self)
        self.img_mod = utl.leer_imagen("./Imagenes/BTN_Modificar.png", (24,24))
        
        
        self.btn_modificar = ttk.Button(self.frame_botones, image=self.img_mod,style="Primary.TButton" ,command=self.modificar_socio)
        self.btn_modificar.grid(row=0, column=2)
        
        # Se configuran los tooltip
        
        ToolTip(self.btn_modificar, "Modificar Usuario", delay=0.5)
        
        self.frame_botones.columnconfigure(0, weight= 7)
        self.frame_botones.columnconfigure(4, weight= 1)
        self.frame_botones.grid(row=3, column=0, sticky="nsew")
        
        
        # Frame lista de productos
        self.frame_lista_socio = ttk.Frame(self)
        self.win_lista_socio = Listausuario(self.frame_lista_socio, self,[SOCIO.cedula, SOCIO.nombre, SOCIO.total_cartera, SOCIO.total_comprado])
        self.win_lista_socio.bind("<BackSpace>", self.eliminar_producto_lista)
        self.frame_lista_socio.grid(row=4, column=0, sticky="nsew")
        
        
        
        # Bóton para cargar los datos al inventario, salir y log out y cambio de clave
        self.frame_inventario = ttk.Frame(self)
        
        self.btn_cargar_inventario = ttk.Button(self.frame_inventario, text="Guardar Datos Usuarios", command=self.guardar_datos,style="Primary.TButton")
        self.btn_cargar_inventario.grid(row=0,column=0, sticky="nsew", columnspan=2)
        
        self.btn_abonar  = ttk.Button(self.frame_inventario, text="Abonar",command=self.abonar, style="Primary.TButton")
        self.btn_abonar.grid(row=1, column=0,sticky="nsew")
        self.btn_quitar_abono = ttk.Button(self.frame_inventario, text="Quitar Abono",command=self.quitar_abono, style="Primary.TButton")
        self.btn_quitar_abono.grid(row=1, column=1,sticky="nsew")
        
        self.btn_mostrar_todos  = ttk.Button(self.frame_inventario, text="Obtener Usuarios",command=self.mostrar_users, style="Primary.TButton")
        self.btn_mostrar_todos.grid(row=2, column=0,sticky="nsew")
        self.btn_mostrar_todos  = ttk.Button(self.frame_inventario, text="Informe Usuario",command=self.obtener_informe_usuarios, style="Primary.TButton")
        self.btn_mostrar_todos.grid(row=2, column=1,sticky="nsew")
        
        self.btn_log_out  = ttk.Button(self.frame_inventario, text="Cerrar Sesión",command=self.log_out, style="Primary.TButton")
        self.btn_log_out.grid(row=3, column=0,sticky="nsew")
        
        self.btn_salir  = ttk.Button(self.frame_inventario, text="Salir",command=self.salir, style="Primary.TButton")
        self.btn_salir.grid(row=3, column=1,sticky="nsew")
        
        self.expandir_widget(self.frame_inventario, row=4, colum=1)
        self.frame_inventario.grid(row=0, column=1, rowspan=5, sticky="nsew")
        
        ## Configurar el frame principal del operario
        self.rowconfigure(4, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
    
    def eliminar_producto_lista(self, event):
        self.win_lista_socio.eliminar_usuario()
    
    def mostrar_users(self):
        usuarios = BD.obtener_usuarios()
        self.win_lista_socio.vaciar_productos()
        for user in usuarios:
            self.win_lista_socio.agregar_usuario(self.return_socio_dict(user))
        
    def quitar_abono(self):
        abono = simpledialog.askinteger("LMH SOLUTIONS","Ingrese un valor para quitar abono", initialvalue=0)
        if(abono>0):
            if (abono>0):
                self.win_lista_socio.abonar_cartera(-abono)
            else:
                messagebox.showwarning("LMH SOLUTIONS","El valor debe ser positivo")   
    
    def abonar(self):
        abono = simpledialog.askinteger("LMH SOLUTIONS","Ingrese un valor para abonar", initialvalue=0)
        if(abono):
            if(abono>0):
                self.win_lista_socio.abonar_cartera(abono)
            else:
                messagebox.showwarning("LMH SOLUTIONS","El valor debe ser positivo")
    
    def log_out(self):
        for tab in self.root.tabs():
            self.root.tab(tab, state="hidden")
        self.root.tab(self.root.tabs()[0], state="normal")
        self.root.select(self.root.tabs()[0])
    
    def guardar_datos(self):
        resp = messagebox.askokcancel("LMH SOLUTIONS", "Esta seguro que va a guardar los datos?")
        if (resp):
            try:
                BD.guardar_info_usuarios(self.win_lista_socio.retornar_productos())
                messagebox.showinfo("LMH SOLUTIONS", "Datos guardados correctamente!")
                self.win_lista_socio.vaciar_productos()
            except:
                messagebox.showerror("LMH SOLUTIONS", "Ha ocurrido un error con la base de datos comuniquese con el técnico de soporte")
        
    def salir(self):
        self.app.on_close()
    
    def agregar_socio(self, bandera_cod, dato):
        self.win_lista_socio.vaciar_productos()
        self.win_lista_socio.agregar_usuario(self.return_socio_dict(self.pedir_datos(bandera_cod, dato)))
        self.limpiar_variables_busqueda()
    
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
                    self.win_lista_socio.vaciar_productos()
                    self.win_lista_socio.agregar_usuario(self.return_socio_dict(values))
                    
                elif self.foco_frame == self.entry_nombre:
                    values = BD.buscar_socio_nombre(self.var_buscar_nombre.get())
                    self.win_lista_socio.vaciar_productos()
                    self.win_lista_socio.agregar_usuario(self.return_socio_dict(values))
            except  ExcepBus as e:  
                respuesta=messagebox.askokcancel("LMH SOLUTIONS", "Cédula o nombre no encontrado. ¿Desea agregar un nuevo usuario?")
                if respuesta:
                    if self.foco_frame == self.entry_codigo:
                        self.agregar_socio(True,self.var_buscar_cod.get())
                    elif self.foco_frame == self.entry_nombre:
                        self.agregar_socio(False,self.var_buscar_nombre.get())
                    
            self.limpiar_variables_busqueda()
            
    def obtener_informe_usuarios(self):
        self.win_informe_socios = WinInformeSocios(self)
    
    def cambiar_widget(self, comand=0):
        if comand==0:
            # Se dejan todo desactivados
            pass
        elif comand ==1:
            # Se activan todos menos la cedula
            pass
    
    def limpiar_variables_busqueda(self):
        self.var_buscar_cod.set("")
        self.var_buscar_nombre.set("")
        self.asignar_foco(self.foco_frame)
    
    def return_socio_dict(self, user_list):
        return  {
            SOCIO.cedula: user_list[0],
            SOCIO.nombre: user_list[1],
            SOCIO.total_comprado: user_list[3],
            SOCIO.total_cartera: user_list[2]
        }
        
    def asignar_foco(self, widget):
        widget.focus()
        
    def mostrar_widget(self, row, column, sticky, widget):
        widget.grid(row=row, column=column, sticky=sticky)
    
    def ocultar_widget(self, widget):
        widget.grid_remove()
        
    def pedir_datos(self, bandera_cod, dato):
        if (bandera_cod):
            cedula = dato
            nombre = simpledialog.askstring("SOFTRU SOLUCIONS", "Ingrese la nombre:", parent=self)    
        else:
            cedula = simpledialog.askstring("SOFTRU SOLUCIONS", "Ingrese la cedula:", parent=self)
            nombre = dato
        
        return (cedula, nombre, 0, 0)