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

class TopLevelInformeProductos():
    def __init__(self, parent) -> None:
        self.new_window1 = tk.Toplevel(parent)
        self.new_window1.title("Informe de inventario")
        self.new_window1.geometry("750x600")
        self.new_window1.state("zoomed") 
        
        
        self. var_mod_filtro_cat = tk.StringVar()
        self. var_mod_filtro_time = tk.StringVar()
        
        self.var_xlabel = tk.StringVar()
        self.var_ylabel = tk.StringVar()
        self.var_title = tk.StringVar()
        
        self.categorias = []
        self.values = []
        
        
        self.filtros_cat = ["Mayor rotación"]
        self.filtros_time = ["Trimestral", "Semestral", "Anual"]
        
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
        bars = ax.bar(range(len(self.categorias)), self.values, tick_label=self.categorias)
        
        # Agregar etiquetas con los valores encima de cada barra
        for bar in bars:
            height = bar.get_height()
            ax.annotate('{}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 puntos de desplazamiento vertical
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        ax.set_xlabel(self.var_xlabel.get())
        ax.set_ylabel(self.var_xlabel.get())
        ax.set_title(self.var_title.get())
        ax.set_xticks(range(len(self.categorias)))
        ax.set_xticklabels(self.categorias, rotation=15, ha='right')
        
        self.canvas = FigureCanvasTkAgg(fig, self.new_window)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=3,sticky="new")

    def filtro_categoría_cambiada(self, event):
        categoria =  self.entry_mod_categoria.get()
        tiempo = self.entry_mod_tiempo.get()
        # Se va a crear el gráfico
        if (tiempo == self.filtros_time[0]): # Trimestral
            indice_rot = self.retornar_indice_rotacion(2)
        
        elif(tiempo == self.filtros_time[1]): # Semestral
            indice_rot = self.retornar_indice_rotacion(5)    
        
        else: # Anual
            indice_rot = self.retornar_indice_rotacion(12)
        
        indice_rot = sorted(indice_rot, key=lambda x: x['Ir'], reverse=True)
        indice_rot = [producto for producto in indice_rot if producto["Ir"] > 0]
        if (len(indice_rot)>20):
            indice_rot = indice_rot[:20]
            
        self.categorias = [producto["nombre"][:19] for producto in indice_rot]
        self.values = [producto["Ir"] for producto in indice_rot]
        
        self.var_xlabel.set(f"{tiempo}: {len(self.categorias)}")
        self.var_ylabel.set("Cantidad de rotaciones")
        self.var_title.set(f"{categoria}: {tiempo}")        
        self.pintar_datos()
    
    
    def retornar_indice_rotacion(self, meses):
        if (meses<=12):
            lista_codigos = self.retornar_cantidad_productos_mensual(meses=meses)
        else:
            lista_codigos = self.retornar_cantidad_productos_anual()
            
        resultado = controller.obtener_dict_codigo_cantidad(lista_codigos)
        indice_rotacion = []
        for codigo, cantidad in resultado.items():
            try:
                indice_rotacion.append({"nombre":BD.buscar_producto_nombre_por_codigo(codigo),
                                    "Ir": int(cantidad/BD.retornar_cantidad_stock(codigo))})
            except ZeroDivisionError as e:
                indice_rotacion.append({"nombre":BD.buscar_producto_nombre_por_codigo(codigo),
                                    "Ir": 0})
            except:
                pass
        return indice_rotacion
    
    def retornar_cantidad_productos_mensual(self, meses):
        fecha_inicio = (datetime.datetime.now() - relativedelta(months=meses)).strftime("%Y-%m")
        fecha_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        return VentasSql.retornar_productos_vendidos(fecha_inicio, fecha_fin)
        
    def retornar_cantidad_productos_anual(self):
        fecha_inicio = datetime.datetime.now().strftime("%Y")
        fecha_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        return VentasSql.retornar_productos_vendidos(fecha_inicio, fecha_fin)
    
    