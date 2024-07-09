import tkinter as tk
from tkinter import ttk
from BaseDatos.InventarioBD import BD_Inventario as BD, ProductoDB
from BaseDatos.VentasBD import VentasSql
from utilidades.EntryP import LabelP
import utilidades.generc as utl
from BaseDatos.VentasBD import VentasSql, VentaEstructuraSql
import TopLevels.controller as controller
from tkinter import messagebox
from utilidades.excepcion import ErrorBusqueda
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

class TopLevelInformeVentas():
    def __init__(self, parent) -> None:
        self.new_window1 = tk.Toplevel(parent)
        self.new_window1.title("Informe de ventas-utilidades")
        self.new_window1.geometry("750x600")
        self.new_window1.state("zoomed") 
        
        
        self. var_mod_filtro_cat = tk.StringVar()
        self. var_mod_filtro_time = tk.StringVar()
        
        self.var_xlabel = tk.StringVar()
        self.var_ylabel = tk.StringVar()
        self.var_title = tk.StringVar()
        
        self.categorias = []
        self.values = []
        
        
        self.filtros_cat = ["Ventas", "Costos", "Utilidades"]
        self.filtros_time = ["Dias", "Meses", "Años"]
        
        
        
        self.new_window = ttk.Labelframe(self.new_window1, style="TFrame")
        self.new_window.pack(fill="both", expand=True)
        self.lb_fecha = ttk.Label(self.new_window, text="Informes generales de la tienda ", style="CCustomLarge.TLabel", anchor="center")
        self.lb_fecha.grid(row=0,column=0, columnspan=3, sticky="nswe")
        
        self.entry_mod_categoria = ttk.Combobox(
            self.new_window, 
            textvariable=self.var_mod_filtro_cat,
            state="readonly",
            values=self.filtros_cat)
        self.entry_mod_categoria.grid(row=1, column=1, sticky="es")
        self.entry_mod_categoria.set(self.filtros_cat[0])
        
        self.entry_mod_tiempo = ttk.Combobox(
            self.new_window, 
            textvariable=self.var_mod_filtro_time,
            state="readonly",
            values=self.filtros_time)
        self.entry_mod_tiempo.grid(row=1, column=2, sticky="ws")
        self.entry_mod_tiempo.set(self.filtros_time[0])
        
        self.filtro_categoría_cambiada(1)
        self.expandir_widget(self.new_window, colum=3)
        
        ## Se campturan los evetos del combobox
        self.entry_mod_categoria.bind("<<ComboboxSelected>>", self.filtro_categoría_cambiada)
        self.entry_mod_tiempo.bind("<<ComboboxSelected>>", self.filtro_categoría_cambiada)
        
    def expandir_widget(self, frame:ttk.LabelFrame, row=3, colum=1):
        for i in range(row):
            frame.rowconfigure(i, weight=1)
        for i in range(colum):
            frame.columnconfigure(i, weight=1)
    
    def pintar_datos(self):
        fig, ax = plt.subplots()
        bars = ax.bar(self.categorias, self.values)
        
        # Agregar etiquetas con los valores encima de cada barra
        for bar in bars:
            height = bar.get_height()
            ax.annotate('${:,}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 puntos de desplazamiento vertical
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        ax.set_xlabel(self.var_xlabel.get())
        ax.set_ylabel(self.var_ylabel.get())
        ax.set_title(self.var_title.get())
        
        self.canvas = FigureCanvasTkAgg(fig, self.new_window)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=3,sticky="nsew")

    def filtro_categoría_cambiada(self, event):
        categoria =  self.entry_mod_categoria.get()
        tiempo = self.entry_mod_tiempo.get()
        # Se va a crear el gráfico
        if (tiempo == self.filtros_time[0]): # Dias
            if (categoria == self.filtros_cat[0]):# Ventas
                lista_fechas, lista_cantidades = self.obtener_datos_diarios(categoria=VentaEstructuraSql.total_vendido)
            elif (categoria == self.filtros_cat[1]): # Compras
                lista_fechas, lista_cantidades = self.obtener_datos_diarios(categoria=VentaEstructuraSql.total_comprado)
            elif (categoria == self.filtros_cat[2]): # Utilidad
                lista_fechas, lista_cantidades = self.obtener_datos_diarios(categoria=VentaEstructuraSql.utilidad)
            lista_fechas = [fecha_mod[-5:] for fecha_mod in lista_fechas]
        
        elif(tiempo == self.filtros_time[1]): # meses
            if (categoria == self.filtros_cat[0]):# Ventas
                lista_fechas, lista_cantidades = self.obtener_datos_mensuales(categoria=VentaEstructuraSql.total_vendido)
            elif (categoria == self.filtros_cat[1]): # Compras
                lista_fechas, lista_cantidades = self.obtener_datos_mensuales(categoria=VentaEstructuraSql.total_comprado)
            elif (categoria == self.filtros_cat[2]): # Utilidad
                lista_fechas, lista_cantidades = self.obtener_datos_mensuales(categoria=VentaEstructuraSql.utilidad)    
        
        elif(tiempo == self.filtros_time[2]): # Años
            if (categoria == self.filtros_cat[0]):# Ventas
                lista_fechas, lista_cantidades = self.obtener_datos_anuales(categoria=VentaEstructuraSql.total_vendido)
            elif (categoria == self.filtros_cat[1]): # Compras
                lista_fechas, lista_cantidades = self.obtener_datos_anuales(categoria=VentaEstructuraSql.total_comprado)
            elif (categoria == self.filtros_cat[2]): # Utilidad
                lista_fechas, lista_cantidades = self.obtener_datos_anuales(categoria=VentaEstructuraSql.utilidad)
        
        self.categorias = lista_fechas
        self.values = lista_cantidades
        
        self.var_xlabel.set(f"{tiempo}: {len(lista_fechas)}")
        self.var_ylabel.set("Pesos")
        self.var_title.set(f"{categoria} por {tiempo}")        
        self.pintar_datos()
    
    def obtener_datos_diarios(self,categoria):
        fecha_inicio = (datetime.datetime.now() - relativedelta(days=14)).strftime("%Y-%m-%d")
        fecha_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        return VentasSql.retornar_valor_diario(fecha_inicio, fecha_fin, categoria)
    
    def obtener_datos_mensuales(self, categoria):
        fecha_inicio = (datetime.datetime.now() - relativedelta(months=6)).strftime("%Y-%m-%d")
        fecha_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        return VentasSql.retornar_valor_mes(fecha_inicio, fecha_fin, categoria)
    
    def obtener_datos_anuales(self, categoria):
        fecha_inicio = (datetime.datetime.now() - relativedelta(years=12)).strftime("%Y-%m-%d")
        fecha_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        return VentasSql.retornar_valor_anio(fecha_inicio, fecha_fin, categoria)
    