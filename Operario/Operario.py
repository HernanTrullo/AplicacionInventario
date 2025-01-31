from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import pandas as pd
from tkinter import messagebox
from tkinter import simpledialog
import tkinter as tk
from utilidades.ListaProducto import Producto, ListaProducto
from BaseDatos.InventarioBD import BD_Inventario as BD
from BaseDatos.InventarioBD import ProductoDB
from utilidades.excepcion import ErrorBusqueda as ExcepBus
from utilidades.EntryP import LabelP
from tkinter import simpledialog
import utilidades.generc as utl
import datetime
from BaseDatos.control_bd_variables import BD_Variables as BD_Var
from BaseDatos.control_bd_socios import BD_Socios as SOCIO
from BaseDatos.control_bd_socios import UsuarioDB as SOCIO_US
from BaseDatos.VentasBD import VentasSql
from BaseDatos.VentasBD import VentaModel
import TopLevels.controller as controller
from utilidades.Infomes import Informe
import random

import numpy as np
from utilidades.Printer import Printer as Impresora

class WinOperario(ttk.Frame):
    def __init__(self, root:ttk.Notebook, app):
        super().__init__(root)
        self.root = root
        self.app = app
        
        # Se conecta la impresora
        self.impresora = Impresora()
        
        # Variables incluidas 
        self.var_nombre_op = tk.StringVar()
        self.var_fecha = tk.StringVar()
        self.var_hora = tk.StringVar()
        
        self.var_descrip_nombre = tk.StringVar()
        self.var_descrip_cod = tk.StringVar()
        self.var_descrip_precio = tk.DoubleVar()
        self.var_descrip_cantidad = tk.IntVar()
        
        self.var_buscar_nombre = tk.StringVar()
        self.var_buscar_cod = tk.StringVar()
        
        self.var_total = tk.IntVar()
        self.var_valor_ventido_op = IntVar()
        self.var_valor_comprado_op_stock = IntVar()
        
        self.var_aporte_cliente = IntVar()
        self.var_saldo_cliente = IntVar()
        
        
        self.var_saldo_efectivo = tk.IntVar()
        self.var_saldo_fiado = tk.IntVar()
        self.var_saldo_pagado = tk.IntVar()
        
        self.var_cedula_check = tk.StringVar()
        
        self.var_es_cartera = tk.BooleanVar()
        self.value_ocultar = True
        
        self.foco_frame = None
        
        self.create_widget()
        self.pack(fill="both", expand=True)
        
        # Inicializar variables
        self.actualizar(0)
        self.bind("<FocusIn>", self.actualizar)
        
    def actualizar(self, event):
        self.actualizar_valor_vendido(BD_Var.get_valor_ventas_turno())
        self.actualizar_saldo_efectivo(BD_Var.get_saldo_efectivo())
        self.actualizar_saldo_fiado(BD_Var.get_saldo_fiado())
        self.actualizar_saldo_pagado_clientes(BD_Var.get_saldo_pagado_clientes())
        
        
    def create_widget(self):
        # Frame que contiene el nombre del operario e información básica
        self.top_frame = ttk.Frame(self, style="Cabecera.TFrame")
        
        self.nameFrame = ttk.Label(self.top_frame, text="Bienvenido: ", style="CCustomLarge.TLabel")
        self.nameFrame.grid(row=0, column=0)
        self.nombre_op = ttk.Label(self.top_frame, textvariable=self.var_nombre_op, style="CCustomMedium.TLabel")
        self.nombre_op.grid(row=0, column=1)
        
        self.lb_valor_vendido_op =  ttk.Label(self.top_frame, text="Vendido: ", style="CCustomSmall.TLabel")
        self.lb_valor_vendido_op.grid(row=0, column=2, padx=10)
        self.valor_vendido_op = LabelP(self.top_frame, textvariable=self.var_valor_ventido_op, style="CCustomSmall.TLabel")
        self.valor_vendido_op.grid(row=0, column=3, padx=10)
        self.lb_valor_vendido_op.bind("<Button-1>", lambda event: self.toggle_visibility())
            
        self.lb_fecha = ttk.Label(self.top_frame, text="Fecha: ", style="CCustomLarge.TLabel")
        self.lb_fecha.grid(row=1,column=0)
        self.fecha = ttk.Label(self.top_frame, textvariable=self.var_fecha,style="CCustomSmall.TLabel")
        self.fecha.grid(row=1, column=1)
        
        self.lb_hora = ttk.Label(self.top_frame, text="Hora: ", style="CCustomLarge.TLabel")
        self.lb_hora.grid(row=2, column=0)
        self.hora = ttk.Label(self.top_frame, textvariable=self.var_hora, style="CCustomSmall.TLabel")
        self.hora.grid(row=2, column=1)
        
        self.lb_efectivo = ttk.Label(self.top_frame, text="Efectivo: ", style="CCustomSmall.TLabel")
        self.lb_efectivo.grid(row=1, column=2)
        self.saldo_efectivo = LabelP(self.top_frame, textvariable=self.var_saldo_efectivo, style="CCustomSmall.TLabel")
        self.saldo_efectivo.grid(row=1, column=3)
        
        self.lb_fiado = ttk.Label(self.top_frame, text="Fiado: ", style="CCustomSmall.TLabel")
        self.lb_fiado.grid(row=2, column=2)
        self.saldo_fiado = LabelP(self.top_frame, textvariable=self.var_saldo_fiado, style="CCustomSmall.TLabel")
        self.saldo_fiado.grid(row=2, column=3)
        
        self.lb_pagado = ttk.Label(self.top_frame, text="Deudas pagadas: ", style="CCustomSmall.TLabel")
        self.lb_pagado.grid(row=3, column=2)
        self.saldo_pagado = LabelP(self.top_frame, textvariable=self.var_saldo_pagado, style="CCustomSmall.TLabel")
        self.saldo_pagado.grid(row=3, column=3)
        
        self.top_frame.grid(row=0,column=0, sticky="nsew")
        
        # Cabecera de la cuenta
        self.frame_top_cuenta = ttk.Frame(self,style="Cabecera.TFrame")
        self.lb_cuenta = ttk.Label(self.frame_top_cuenta, text="Cuenta Cliente", style="CCustomMedium.TLabel")
        self.lb_cuenta.grid(row=0, column=0, padx=10, pady=15,columnspan=2)
        
        self.lb_total = ttk.Label(self.frame_top_cuenta, text="Total", style="CCustomMedium.TLabel")
        self.lb_total.grid(row=1, column=0, padx=10)
        
        self.out_total = LabelP(self.frame_top_cuenta, textvariable=self.var_total ,style="CCustomMedium.TLabel") # La salida del total
        self.out_total.grid(row=1,column=1,padx=10)
        
        
        self.frame_top_cuenta.grid(row=0, column=1, rowspan=2,sticky="nsew")
        self.expandir_widget(self.frame_top_cuenta)
        
        # Frame del buscar de datos
        self.ingreso_datos = ttk.Frame(self)
        
        self.lb_codigo = ttk.Label(self.ingreso_datos, text="Código",style="CustomSmall.TLabel" )
        self.lb_codigo.grid(row=0, column=0)
        self.entry_codigo = ttk.Entry(self.ingreso_datos, textvariable=self.var_buscar_cod)
        self.entry_codigo.grid(row=1, column=0,sticky="nsew")
        
        self.lb_nombre_producto = ttk.Label(self.ingreso_datos, text="Nombre",style="CustomSmall.TLabel")
        self.lb_nombre_producto.grid(row=0, column=1)
        self.entry_nombre_producto = ttk.Combobox(self.ingreso_datos, textvariable=self.var_buscar_nombre)
        self.entry_nombre_producto.grid(row=1, column=1,sticky="nsew")
        self.entry_nombre_producto.bind("<KeyRelease>", self.actualizar_nombre_productos)
        
        self.expandir_widget(self.ingreso_datos, colum=3, row=2)
        self.ingreso_datos.grid(row=1, column=0,sticky="nsew", pady=10)
        
        # Frame botones de cálculo de cuenta y logeo-salir
        self.frame_calculo_cuenta = ttk.Frame(self,style="Cabecera.TFrame")
        
        vc = (self.register(utl.validar_numero), "%P")
        self.lb_aporte_cliente = ttk.Label(self.frame_calculo_cuenta, text="Pago Cliente", style="CCustomMedium.TLabel")
        self.lb_aporte_cliente.grid(row=0, column=0)
        self.aporte_cliente = ttk.Entry(self.frame_calculo_cuenta, textvariable=self.var_aporte_cliente, validate="key", validatecommand=vc)
        self.aporte_cliente.grid(row = 0, column=1)
        self.aporte_cliente.bind("<KeyRelease>", self.calcular_precio)
        
        
        self.lb_saldo_cliente = ttk.Label(self.frame_calculo_cuenta, text="Saldo Cliente", style="CCustomMedium.TLabel").grid(row=1, column=0)
        self.saldo_cliente = LabelP(self.frame_calculo_cuenta, textvariable=self.var_saldo_cliente, style="CCustomMedium.TLabel")
        self.saldo_cliente.grid(row = 1, column=1)
        
        self.lb_cedula_check = ttk.Label(self.frame_calculo_cuenta, text="Código Cliente", style="CCustomMedium.TLabel").grid(row=2, column=0)
        self.cedula_check = ttk.Combobox(self.frame_calculo_cuenta, textvariable=self.var_cedula_check)
        self.cedula_check.grid(row=2, column=1)
        self.cedula_check.bind("<KeyRelease>", self.buscar_cedula)
        self.cedula_check["values"] = ["0"]
        self.cedula_check.set(0)
        
        self.lb_es_cartera_cliente = ttk.Label(self.frame_calculo_cuenta, text="Cartera", style="CCustomMedium.TLabel").grid(row=3, column=0)
        self.es_cartera = ttk.Checkbutton(self.frame_calculo_cuenta, variable=self.var_es_cartera)
        self.es_cartera.grid(row=3, column=1)
        
        self.notebook_buttons = ttk.Notebook(self.frame_calculo_cuenta)
        self.notebook_buttons.grid(row=4, column=0, columnspan=2, sticky="nsew")
        
        self.frame1_ventas_caja = ttk.Frame(self.notebook_buttons)
        self.frame2_opciones_user = ttk.Frame(self.notebook_buttons)
        self.notebook_buttons.add(self.frame1_ventas_caja, text="Ventas y Caja")
        self.notebook_buttons.add(self.frame2_opciones_user, text="Opciones de Usuario")
        
        self.btn_vender  = ttk.Button(self.frame1_ventas_caja, text="Vender",command=self.vender, style="Primary.TButton")
        self.btn_vender.grid(row=0, column=0, sticky="nsew")
        self.btn_vender  = ttk.Button(self.frame1_ventas_caja, text="Cerrar Caja",command=self.cerrar_caja, style="Primary.TButton")
        self.btn_vender.grid(row=1, column=0, sticky="nsew")
        
        self.btn_salir  = ttk.Button(self.frame2_opciones_user, text="Salir",command=self.salir, style="Primary.TButton")
        self.btn_salir.grid(row=0, column=0,sticky="nsew")
        self.btn_log_out  = ttk.Button(self.frame2_opciones_user, text="Salir Cuenta",command=self.log_out, style="Primary.TButton")
        self.btn_log_out.grid(row=1, column=0,sticky="nsew")
        
        self.expandir_widget(self.frame1_ventas_caja, row=2, colum=1)
        self.expandir_widget(self.frame2_opciones_user, row=2, colum=1)
        self.expandir_widget(self.frame_calculo_cuenta, row=3, colum=2)
        
        self.frame_calculo_cuenta.rowconfigure(4, weight=2)
        self.frame_calculo_cuenta.grid(row=2, column=1,sticky="nsew")
        
        # Frame lista de productos
        self.frame_lista_producto = ttk.Frame(self)
        self.win_lista_producto = ListaProducto(self.frame_lista_producto, self,[Producto.codigo,Producto.nombre, Producto.precio, Producto.cantidad], 100)
        self.frame_lista_producto.grid(row=2, column=0, sticky="nsew")
        self.expandir_widget(self.frame_lista_producto,row=1, colum=1)
        self.win_lista_producto.bind("<BackSpace>", self.eliminar_producto_auto)
        
        ## Configurar el frame principal del operario
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(2, weight=3)
        
        # guardar foco del frame
        self.entry_codigo.bind("<FocusIn>", self.controlador_de_foco)
        self.entry_nombre_producto.bind("<FocusIn>", self.controlador_de_foco)
        
        # Agregar producto automaticamente 
        self.entry_codigo.bind("<Return>", self.agregar_automaticamente)
        self.entry_nombre_producto.bind("<Return>", self.agregar_automaticamente)
        
        # Agregar fecha y hora
        self.var_fecha.set(datetime.date.today().strftime('%d/%m/%Y'))
        self.actualizar_hora()
        
    
    def toggle_visibility(self):
        if self.value_ocultar:
            self.valor_vendido_op.grid_forget()
            self.value_ocultar = False
        else:
            self.valor_vendido_op.grid(row=0, column=3, padx=10)
            self.value_ocultar = True
    
    def buscar_cedula(self, event):
        try:
            values = SOCIO.buscar_socios_nombre(self.var_cedula_check.get())
            if values:
                self.cedula_check["values"] =  values
            else:
                self.cedula_check["values"] = ["0"]
        except:
            self.cedula_check["values"] = ["0"]
    
    def actualizar_nombre_productos(self, event):
        try:
            self.entry_nombre_producto['values']=BD.retornar_nombres_productos(self.var_buscar_nombre.get())     
        except:
            self.entry_nombre_producto['values'] = [""]
            
            
    def actualizar_hora(self):
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        self.var_hora.set(hora_actual)
        self.after_id = self.after(1000, self.actualizar_hora)
        
    def cerrar_caja(self):
        if messagebox.askokcancel("Cierre de Caja", "¿Estás seguro de que quieres cerrar caja?\nAdicionamente, generar el informe del cierre de caja?"):
            # Una funcion para imprimir un resumen del informes
            try:
                saldo_caja = BD_Var.get_saldo_caja() 
                ventas_turno = BD_Var.get_valor_ventas_turno()
                efectivo = BD_Var.get_saldo_efectivo()
                saldo_fiado = BD_Var.get_saldo_fiado()
                saldo_pagado = BD_Var.get_saldo_pagado_clientes()
                
                fecha = datetime.datetime.now().strftime("%Y-%m-%d")
                codigos_json = VentasSql.retornar_codigo_productos_vendidos(fecha)
                resultado = controller.obtener_dict_codigo_cantidad(codigos_json)
                
                self.lista_nombres = []        
                for codigo, cantidad in resultado.items():
                    self.lista_nombres.append({"nombre":BD.buscar_producto_nombre_por_codigo(codigo),
                                            "cantidad": cantidad})
            except ExcepBus as e:
                messagebox.showinfo("LMH SOLUTIOS", "No se han encontrado ventas en las fechas establecidas")
            
            Informe.generar_informe_caja(int(ventas_turno), int(saldo_caja),int(efectivo) , int(saldo_fiado), int(saldo_pagado),self.lista_nombres)
            #Resetear el valor de las ventas temporales del dia por el operario
            BD_Var.reset_valor_ventas_turno()
            self.actualizar(0)
    
    def vender(self):
        try:
            values_socio = list(SOCIO.buscar_socio_cedula(self.var_cedula_check.get()))
            resp = messagebox.askokcancel("LMH SOLUTIONS", "Esta seguro que desea vender los anteriores productos?")
            if resp:
                try:
                    productos_data_frame =  self.win_lista_producto.retornar_productos()
                    BD.sacar_productos(productos_data_frame) # Se sacan los productos de la bases de datos
                    valor_comprado_stock =   BD.retornar_valor_compras_stock(productos_data_frame)
                    value_total_venta = int(BD_Var.get_valor_ventas_turno()) + self.var_total.get() # Valor total de ventas del turno
                    
                    #Se actualizan las variables de afiliado
                    values_socio[3] = self.var_total.get() + values_socio[3]
                    valor_cartera = values_socio[2]
                    if (self.var_es_cartera.get()):
                        values_socio[2] = valor_cartera + self.var_total.get() # valor cartera
                        BD_Var.set_saldo_fiado(int(BD_Var.get_saldo_fiado()) + self.var_total.get())
                        self.actualizar_saldo_fiado(int(BD_Var.get_saldo_fiado()))
                    else:
                        BD_Var.set_saldo_efectivo(int(BD_Var.get_saldo_efectivo()) + self.var_total.get())
                        self.actualizar_saldo_efectivo(int(BD_Var.get_saldo_efectivo()))
                        
                    dict_u= {
                        SOCIO_US.cedula: values_socio[0],
                        SOCIO_US.nombre: values_socio[1],
                        SOCIO_US.total_cartera: values_socio[2],
                        SOCIO_US.total_comprado: values_socio[3]
                    }
                    SOCIO.actualizar_socio(dict_u)
                    
                    # Imprimir la tirilla
                    if (messagebox.askokcancel("LMH SOLUTIONS", "Desea imprimir el ticket?")):
                        self.impresora.plotear_datos(self.dataFrame2listTuple(productos_data_frame), self.var_total.get(), self.var_cedula_check.get())
                    else:
                        self.impresora.no_plotear_datos()
                    
                    
                    BD_Var.set_valor_ventas_turno(str(value_total_venta))
                    self.actualizar_valor_vendido(value_total_venta)
                    
                    
                    # Set del valor de compra de los articulos
                    BD_Var.set_valor_comprado_stock(valor_comprado_stock + int(BD_Var.get_valor_comprado_stock()))
                    # Enviar datos venta a la base de datos
                
                    lista_productos = []
                    for index, row in productos_data_frame.iterrows():
                        lista_productos.append({Producto.codigo: row[Producto.codigo]  ,Producto.cantidad: row[Producto.cantidad]})
                    
                    fecha_ac = datetime.datetime.now().strftime("""%Y-%m-%d""")
                    tot_vendido = self.var_total.get()
                    tot_comprado = valor_comprado_stock

                    venta = VentaModel(fecha=fecha_ac, 
                                        total_vendido= tot_vendido, 
                                        total_comprado= tot_comprado, 
                                        productos_vendidos= utl.dictToJson(lista_productos), 
                                        id_cliente=self.var_cedula_check.get(), 
                                        es_cartera= self.var_es_cartera.get())    
                    VentasSql.agregar_venta(venta)
                    
                    self.win_lista_producto.vaciar_productos()
                    self.var_es_cartera.set(False)
                    self.var_cedula_check.set(0)
                    self.var_saldo_cliente.set(0)
                    self.var_aporte_cliente.set(0)
                    
                    self.saldo_cliente.formatear_valor()
                    self.actualizar_precio_total()
                    
                    messagebox.showinfo("LMH SOLUTIONS", "Operacion Exitosa!")
                    
                except NameError as e:
                    messagebox.showerror("LMH SOLUTIONS", e)
        except NameError as e:
            messagebox.showerror("LMH SOLUTIONS", e)
                                
    
    
    def calcular_precio(self, event):
        try:
            valor_aporte = self.var_aporte_cliente.get()
            saldo = valor_aporte - self.var_total.get()
            # Estas dos funciones siempre van juntas cuando la clase es LabelP
            self.var_saldo_cliente.set(saldo)
            self.saldo_cliente.formatear_valor()
            
            if saldo < 0:
                self.saldo_cliente.configure(style="CErrorCustomMedium.TLabel")
            else:
                self.saldo_cliente.configure(style="CCustomMedium.TLabel")
        except:
            pass
        
    
    def salir(self):
        self.app.on_close()
    
    def log_out(self):
        if messagebox.askokcancel("Log Out", "¿Estás seguro de que quieres terminar sesión?"):
            notebok_tabs= self.root.tabs()
            self.root.tab(notebok_tabs[4], state="hidden")
            self.root.tab(notebok_tabs[2], state="hidden")
            self.root.tab(notebok_tabs[1], state="hidden")
            self.root.tab(notebok_tabs[0], state="normal")
            self.root.select(notebok_tabs[0])
            
    
    def controlador_de_foco(self, event):
        self.foco_frame = event.widget
    
    def agregar_automaticamente(self, event):
        self.buscar_producto()
    
    def eliminar_producto_auto(self, event):
        self.eliminar_producto()
        
        
    def buscar_producto(self):
        if self.foco_frame == self.entry_codigo or self.foco_frame == self.entry_nombre_producto:
            try:
                if self.foco_frame == self.entry_codigo:
                    producto = BD.buscar_producto_cod(self.var_buscar_cod.get())   
                    self.var_descrip_cod.set(producto[ProductoDB.codigo])
                    self.var_descrip_nombre.set(producto[ProductoDB.nombre])
                    self.var_descrip_precio.set(producto[ProductoDB.precio])
                    
                    if producto[ProductoDB.cantidad] < 5:
                        messagebox.showwarning("LMH SOLUTIONS", f"El producto {producto[ProductoDB.nombre]} se está agotando del stock")
                    self.var_descrip_cantidad.set(1)
                    
                    self.agregar_producto()
                    
                elif self.foco_frame == self.entry_nombre_producto:
                    producto = BD.buscar_producto_nombre(self.var_buscar_nombre.get())
                    self.var_descrip_cod.set(producto[ProductoDB.codigo])
                    self.var_descrip_nombre.set(producto[ProductoDB.nombre])
                    self.var_descrip_precio.set(producto[ProductoDB.precio])
                    if producto[ProductoDB.cantidad] < 1:
                        messagebox.showwarning("LMH SOLUTIONS", f"El producto {producto[ProductoDB.nombre]} debería estar en stock")
                    self.var_descrip_cantidad.set(1)

                    self.agregar_producto()
                        
            except  ExcepBus as e:  
                messagebox.showwarning("LMH SOLUTIONS", "Codigo o Nombre no encontrado. ¡Vaya al panel de administrador para agregarlo!")
                        
            self.var_buscar_cod.set("")
            self.var_buscar_nombre.set("")
    
    
    # Funciones de la visualización de los productos temporal
    def agregar_producto(self):
        self.win_lista_producto.agregar_producto(self.retornar_valores_producto())
        self.limpiar_variables()
        self.actualizar_precio_total()
        
    def eliminar_producto(self):
        self.win_lista_producto.eliminar_producto()
        self.actualizar_precio_total()

    def modificar_producto(self):   
        self.win_lista_producto.modificar_producto(self.retornar_valores_producto())
        self.limpiar_variables()
        self.actualizar_precio_total()
    
    def expandir_widget(self, frame:ttk.LabelFrame, row=2, colum=2):
        for i in range(row):
            frame.rowconfigure(i, weight=1)
        for i in range(colum):
            frame.columnconfigure(i, weight=1)
    
    def limpiar_variables(self):
        self.var_descrip_nombre.set("")
        self.var_descrip_cod.set("")
        self.var_descrip_precio.set(0)
        self.var_descrip_cantidad.set(0)
        
    def doble_click_producto_modificar(self,valores):
        self.var_descrip_cod.set(valores[0])
        self.var_descrip_nombre.set(valores[1])
        self.var_descrip_precio.set(valores[2])
        
        res = simpledialog.askinteger("LMH SOLUTIONS", "Ingrese una cantidad")
        if res:
            self.var_descrip_cantidad.set(res)
            self.modificar_producto()
        
    def retornar_valores_producto(self):
        return {
            Producto.codigo: [self.var_descrip_cod.get()],
            Producto.nombre: [self.var_descrip_nombre.get()],
            Producto.precio: [self.var_descrip_precio.get()],
            Producto.cantidad: [self.var_descrip_cantidad.get()]
        }
        
    def dataFrame2listTuple(self, df:pd.DataFrame):
        prod = list()
        for index,row in df.iterrows():
            prod.append((row[Producto.nombre], int(row[Producto.precio]), int(row[Producto.cantidad]), int(row[Producto.sub_total])))
        return prod
            
    def actualizar_precio_total(self):
        # Calcular precio total 
        self.var_total.set(self.win_lista_producto.calcular_precio_productos())
        self.out_total.formatear_valor()
    
    def actualizar_valor_vendido (self, value):
        self.var_valor_ventido_op.set(value)
        self.valor_vendido_op.formatear_valor()
        
    def actualizar_saldo_efectivo(self, value):
        self.var_saldo_efectivo.set(value)
        self.saldo_efectivo.formatear_valor()
        
    def actualizar_saldo_fiado(self, value):
        self.var_saldo_fiado.set(value)
        self.saldo_fiado.formatear_valor()
        
    def actualizar_saldo_pagado_clientes(self, value):
        self.var_saldo_pagado.set(value)
        self.saldo_pagado.formatear_valor()



