from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import pandas as pd
from tkinter import messagebox
import tkinter as tk
from utilidades.ListaProducto import Producto, ListaProducto
from BaseDatos.InventarioBD import BD_Inventario as BD
from BaseDatos.InventarioBD import ProductoDB
from BaseDatos.InventarioBD import Categorias
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
        self.var_total_vendido = tk.StringVar()

        self.var_buscar_nombre = tk.StringVar()
        self.var_buscar_cod = tk.StringVar()
        self.var_categoria = tk.StringVar()
        
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
        
        # Frame que muestra los precios que añade el administrador
        self.frame_precios = ttk.Frame(self, style="Cabecera.TFrame")
        self.lb_total = ttk.Label(self.frame_precios, text="Total_PC", style="CCustomMedium.TLabel")
        self.lb_total.grid(row=0, column=0, sticky="nsew")
        self.total = LabelP(self.frame_precios, textvariable=self.var_total, style="CCustomMedium.TLabel")
        self.total.grid(row=0, column=1, sticky="nsew")
        
        self.lb_total_venta = ttk.Label(self.frame_precios, text="Total_PV", style="CCustomMedium.TLabel")
        self.lb_total_venta.grid(row=1, column=0, sticky="nsew")
        self.total_venta = LabelP(self.frame_precios, textvariable=self.var_total_vendido, style="CCustomMedium.TLabel")
        self.total_venta.grid(row=1, column=1, sticky="nsew")
        
        self.frame_precios.grid(row=0, column=1, sticky="nsew")
        self.expandir_widget(self.frame_precios,row=1)
        
        # Bóton para cargar los datos al inventario, salir y log out
        self.frame_inventario = ttk.Frame(self)
        self.btn_cargar_inventario = ttk.Button(self.frame_inventario, text="Actualizar", command=self.cargar_productos_totales,style="Primary.TButton")
        self.btn_cargar_inventario.grid(row=0,column=0, sticky="nsew")
        self.btn_salir  = ttk.Button(self.frame_inventario, text="Salir",command=self.salir, style="Primary.TButton")
        self.btn_salir.grid(row=2, column=0,sticky="nsew")
        self.btn_log_out  = ttk.Button(self.frame_inventario, text="Salir Cuenta",command=self.log_out, style="Primary.TButton")
        self.btn_log_out.grid(row=1, column=0,sticky="nsew")
        
        self.expandir_widget(self.frame_inventario, row=3, colum=1)
        self.frame_inventario.grid(row=1, column=1, rowspan=3, sticky="nsew")
        
        # Frame buscar por nombre
        self.ingreso_datos = ttk.Frame(self)
        
        self.lb_nombre_producto = ttk.Label(self.ingreso_datos, text="Nombre",style="CustomSmall.TLabel")
        self.lb_nombre_producto.grid(row=0, column=1)
        self.entry_nombre_producto = ttk.Combobox(self.ingreso_datos, textvariable=self.var_buscar_nombre)
        self.entry_nombre_producto.grid(row=1, column=1,sticky="nsew")
        self.entry_nombre_producto.bind("<KeyRelease>", self.actualizar_nombre_productos)
        self.entry_nombre_producto.bind("<Return>", self.mostrar_producto)
        
        self.lb_codigo = ttk.Label(self.ingreso_datos, text="Código", style="CustomSmall.TLabel")
        self.lb_codigo.grid(row=0, column=0)
        self.entry_codigo = ttk.Entry(self.ingreso_datos, textvariable=self.var_buscar_cod,style="Custom.TEntry")
        self.entry_codigo.grid(row=1, column=0,sticky="nsew")
        
        self.lb_categoria = ttk.Label(self.ingreso_datos, text="Categoría", style="CustomSmall.TLabel")
        self.lb_categoria.grid(row=0, column=2)
        
        self.cbox_categoria = ttk.Combobox(
            self.ingreso_datos, 
            textvariable=self.var_categoria,
            state="readonly",
            values=Categorias.categorias)
        self.cbox_categoria.set(Categorias.tienda)
        self.cbox_categoria.grid(row=1, column=2,sticky="nsew")
        self.cbox_categoria.bind("<<ComboboxSelected>>", self.cargar_inventario_por_categoria)
        
        self.ingreso_datos.grid(row=1, column=0, sticky="nsew")
        self.expandir_widget(self.ingreso_datos, colum=3)
        
        # Frame lista de productos
        self.frame_lista_producto = ttk.Frame(self)
        self.win_lista_producto = ListaProducto(self.frame_lista_producto, self,[Producto.codigo,Producto.nombre, Producto.precio, Producto.precio_entrada,Producto.cantidad, Producto.categoria])
        self.frame_lista_producto.grid(row=2, column=0, sticky="nsew")
        self.expandir_widget(self.frame_lista_producto,row=1, colum=1)
        # Agregar le evento de seleción
        self.win_lista_producto.bind("<<TreeviewSelect>>", self.set_sub_total)
        
        ## Configurar el frame principal del operario
        self.rowconfigure(2, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(0, weight=0)
        
        
        # guardar foco del frame
        self.entry_codigo.bind("<FocusIn>", self.controlador_de_foco)
        self.entry_nombre_producto.bind("<FocusIn>", self.controlador_de_foco)
        
        # Agregar producto automaticamente 
        self.entry_codigo.bind("<Return>", self.mostrar_producto)
        
    def controlador_de_foco(self, event):
        self.foco_frame = event.widget
    
    
    def mostrar_producto(self, event):
        try:
            if self.foco_frame == self.entry_nombre_producto:
                prod = BD.buscar_producto_nombre(self.var_buscar_nombre.get())
                self.win_lista_producto.vaciar_productos()
                self.win_lista_producto.agregar_producto(
                self.retornar_valores_producto(prod))
                
                
            elif self.foco_frame == self.entry_codigo:
                prod = BD.buscar_producto_cod(self.var_buscar_cod.get())
                self.win_lista_producto.vaciar_productos()
                self.win_lista_producto.agregar_producto(
                self.retornar_valores_producto(prod))
                
        except ExcepBus as e:
            messagebox.showinfo("LMH SOLUTIONS", e)
            
        except :
            messagebox.showerror("LMH SOLUTIONS", "Algo ha ocurrido con la aplicación, comuníquese con soporte")
        
        self.vaciar_widget()
    
    
    
    def vaciar_widget(self):
        self.var_buscar_nombre.set("")
        self.var_buscar_cod.set("")
            
    def actualizar_nombre_productos(self, event):
        try:
            self.entry_nombre_producto['values']=BD.retornar_nombres_productos(self.var_buscar_nombre.get())     
        except:
            self.entry_nombre_producto['values'] = [""]
    
    
    def set_sub_total(self, event):
        valor_t = 0
        selected_item = self.win_lista_producto.selection()
        for s_item in selected_item:
            producto = self.win_lista_producto.item(s_item, "values")
            valor_t += int(producto[6])
        
        self.set_valor_total(valor_t)
    
    def actualizar_hora(self):
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        self.var_hora.set(hora_actual)
        self.after_id = self.after(1000, self.actualizar_hora)
        
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
            
    def cargar_inventario(self,categoria = Categorias.tienda):
        try:
            productos = BD.obtener_productos(categoria=categoria)
            self.win_lista_producto.vaciar_productos()
            productos_data = []
            for producto in productos:
                productos_data.append(self.retornar_valores_producto(producto))
                
            self.win_lista_producto.agregar_productos_en_bloque(productos_data)
            self.set_valor_total(self.win_lista_producto.calcular_precio_productos_entrada())
            self.set_valor_total_vendido(self.win_lista_producto.calcular_precio_productos_vendido())
        except:
            self.set_valor_total(0)
            self.set_valor_total_vendido(0)
            messagebox.showinfo("LMH SOLUTIONS", "No productos la referencia de la categoria")
    
    def cargar_productos_totales(self):
        try:
            productos = BD.obtener_productos_totales()
            self.win_lista_producto.vaciar_productos()
            productos_data = []
            for producto in productos:
                productos_data.append(self.retornar_valores_producto(producto))
                
            self.win_lista_producto.agregar_productos_en_bloque(productos_data)
            self.set_valor_total(self.win_lista_producto.calcular_precio_productos_entrada())
            self.set_valor_total_vendido(self.win_lista_producto.calcular_precio_productos_vendido())
        except:
            self.set_valor_total(0)
            self.set_valor_total_vendido(0)
            messagebox.showinfo("LMH SOLUTIONS", "No productos la referencia de la categoria")
    
    def set_valor_total(self, valor):
        self.var_total.set(valor)
        self.total.formatear_valor()
        
    def set_valor_total_vendido(self, valor):
        self.var_total_vendido.set(valor)
        self.total_venta.formatear_valor()    
    
    def retornar_valores_producto(self, producto):
        return {
            Producto.codigo: [producto[ProductoDB.codigo]],
            Producto.nombre: [producto[ProductoDB.nombre]],
            Producto.precio: [producto[ProductoDB.precio]],
            Producto.precio_entrada: [producto[ProductoDB.precio_entrada]],
            Producto.cantidad: [producto[ProductoDB.cantidad]],
            Producto.categoria: [producto[Producto.categoria]]
        }
        
    def cargar_inventario_por_categoria(self, event):
        self.cargar_inventario(self.cbox_categoria.get())
        
    def doble_click_producto_modificar(self, values):
        pass
            
    def expandir_widget(self, frame:ttk.LabelFrame, row=2, colum=2):
        for i in range(row):
            frame.rowconfigure(i, weight=1)
        for i in range(colum):
            frame.columnconfigure(i, weight=1)