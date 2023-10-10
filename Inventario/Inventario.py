from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import pandas as pd
from tkinter import messagebox
import tkinter as tk
from utilidades.ListaProducto import Producto, ListaProducto
from BaseDatos.InventarioBD import BD_Inventario as BD
from utilidades.excepcion import ErrorBusqueda as ExcepBus
from utilidades.EntryP import LabelP
import datetime


class WinInventario(ttk.Frame):
    def __init__(self, root:ttk.Notebook, app):
        super().__init__(root)
        self.root = root
        self.app = app
        # Variables incluidas 
        self.var_nombre_op = tk.StringVar()
        self.var_fecha = tk.StringVar()
        self.var_hora = tk.StringVar()
        
        self.var_total = tk.StringVar()
        
        self.create_widget()
        
    def create_widget(self):
        # Frame que contiene el nombre del operario e información básica
        self.top_frame = ttk.LabelFrame(self)
        
        self.nameFrame = ttk.Label(self.top_frame, text="Bienvenido: ", style="Custom.TLabel")
        self.nameFrame.grid(row=0, column=0)
        self.nombre_op = ttk.Label(self.top_frame, textvariable=self.var_nombre_op, style="Custom.TLabel")
        self.nombre_op.grid(row=0, column=1)
        
        self.lb_fecha = ttk.Label(self.top_frame, text="Fecha: ", style="Custom.TLabel")
        self.lb_fecha.grid(row=1,column=0)
        self.fecha = ttk.Label(self.top_frame, textvariable=self.var_fecha)
        self.fecha.grid(row=1, column=1)
        
        self.lb_hora = ttk.Label(self.top_frame, text="Hora: ", style="Custom.TLabel")
        self.lb_hora.grid(row=2, column=0)
        self.hora = ttk.Label(self.top_frame, textvariable=self.var_hora)
        self.hora.grid(row=2, column=1)
        self.top_frame.grid(row=0,column=0, sticky="nsew")
        
        # Agregar fecha y hora
        self.var_fecha.set(datetime.date.today().strftime('%d/%m/%Y'))
        self.actualizar_hora()
        
        # Frame que muestra los precios que añade el administrador
        self.frame_precios = ttk.LabelFrame(self)
        self.lb_total = ttk.Label(self.frame_precios, text="Total", style="Custom.TLabel")
        self.lb_total.grid(row=0, column=0, sticky="nsew")
        self.total = LabelP(self.frame_precios, textvariable=self.var_total, style="Custom13.TLabel")
        self.total.grid(row=0, column=1, sticky="nsew")
        self.frame_precios.grid(row=0, column=1, sticky="nsew")
        self.expandir_widget(self.frame_precios,row=1)
        
        # Bóton para cargar los datos al inventario, salir y log out
        self.frame_inventario = ttk.LabelFrame(self)
        self.btn_cargar_inventario = ttk.Button(self.frame_inventario, text="Actualizar", command=self.calcular_total,style="CustomOperacion.TButton")
        self.btn_cargar_inventario.grid(row=0,column=0, sticky="nsew")
        self.btn_salir  = ttk.Button(self.frame_inventario, text="Salir",command=self.salir, style="CustomQuit.TButton")
        self.btn_salir.grid(row=2, column=0,sticky="nsew")
        self.btn_log_out  = ttk.Button(self.frame_inventario, text="Salir Cuenta",command=self.log_out, style="CustomQuit.TButton")
        self.btn_log_out.grid(row=1, column=0,sticky="nsew")
        
        self.expandir_widget(self.frame_inventario, row=3, colum=1)
        self.frame_inventario.grid(row=1, column=1, rowspan=3, sticky="nsew")
        
        # Frame lista de productos
        self.frame_lista_producto = ttk.LabelFrame(self)
        self.win_lista_producto = ListaProducto(self.frame_lista_producto, self,[Producto.codigo,Producto.nombre, Producto.precio, Producto.precio_entrada,Producto.cantidad])
        self.frame_lista_producto.grid(row=2, column=0, sticky="nsew")
        
        # Agregar le evento de seleción
        self.win_lista_producto.bind("<<TreeviewSelect>>", self.set_sub_total)
        
        ## Configurar el frame principal del operario
        self.rowconfigure(2, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(0, weight=0)
        
    
    def set_sub_total(self, event):
        valor_t = 0
        selected_item = self.win_lista_producto.selection()
        for s_item in selected_item:
            producto = self.win_lista_producto.item(s_item, "values")
            valor_t += int(producto[5])
        
        self.set_valor_total(valor_t)
    
    def actualizar_hora(self):
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        self.var_hora.set(hora_actual)
        self.after(1000, self.actualizar_hora)
        
    def salir(self):
        self.app.on_close()
    
    def log_out(self):
        if messagebox.askokcancel("Log Out", "¿Estás seguro de que quieres terminar sesión?"):
            notebok_tabs= self.root.tabs()
            self.root.tab(notebok_tabs[2], state="disabled")
            self.root.tab(notebok_tabs[1], state="disabled")
            self.root.tab(notebok_tabs[0], state="normal")
            self.root.select(notebok_tabs[0])
            
    def calcular_total(self):
        productos = BD.obtener_productos()
        self.win_lista_producto.vaciar_productos()
        for producto in productos:
            self.win_lista_producto.agregar_producto(self.retornar_valores_producto(producto))

        self.set_valor_total(self.win_lista_producto.calcular_precio_productos())
        
    def set_valor_total(self, valor):
        self.var_total.set(valor)
        self.total.formatear_valor()
    
    def retornar_valores_producto(self, producto):
        return {
            Producto.codigo: [producto[0]],
            Producto.nombre: [producto[1]],
            Producto.precio: [producto[2]],
            Producto.precio_entrada: [producto[3]],
            Producto.cantidad: [producto[4]]
        }
        
        
    def doble_click_producto_modificar(self, values):
        pass
            
    def expandir_widget(self, frame:ttk.LabelFrame, row=2, colum=2):
        for i in range(row):
            frame.rowconfigure(i, weight=1)
        for i in range(colum):
            frame.columnconfigure(i, weight=1)