import tkinter as tk
from tkinter import ttk
from BaseDatos.InventarioBD import BD_Inventario as BD, ProductoDB
from BaseDatos.control_bd_socios import BD_Socios, UsuarioDB
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

class TopLevelInformeSocios():
    def __init__(self, parent) -> None:
        self.new_window1 = tk.Toplevel(parent)
        self.new_window1.title("Informe Socios")
        self.new_window1.geometry("750x600")
        self.new_window1.state("zoomed") 
        
        self.numero_items_por_frame = 10
        self.numero_total_paginas = 0;
        self.numero_pagina = 1
        self.index_inicial = 0
        self.index_final = 10
        
        self. var_mod_filtro_cat = tk.StringVar()
        self. var_mod_filtro_time = tk.StringVar()
        
        self.var_xlabel = tk.StringVar()
        self.var_ylabel = tk.StringVar()
        self.var_title = tk.StringVar()
        
        self.categorias = []
        self.values = []
        
        
        self.filtros_cat = ["Valor Cartera", "Dias en mora"]
        
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
        
        self.filtro_categoría_cambiada(1)
        self.expandir_widget(self.new_window, colum=3)
        
        ## Se campturan los evetos del combobox
        self.entry_mod_categoria.bind("<<ComboboxSelected>>", self.filtro_categoría_cambiada)
        self.new_window1.bind('<Right>', self.siguiente_pagina)
        self.new_window1.bind('<Left>', self.anterior_pagina)
        
    def expandir_widget(self, frame:ttk.LabelFrame, row=3, colum=1):
        for i in range(row):
            frame.rowconfigure(i, weight=1)
        for i in range(colum):
            frame.columnconfigure(i, weight=1)
    
    def pintar_datos(self, rot, categorias_pagina, valores_pagina):
        fig, ax = plt.subplots()
        bars = ax.bar(range(len(categorias_pagina)), valores_pagina, tick_label=categorias_pagina)
        
        # Agregar etiquetas con los valores encima de cada barra
        for bar in bars:
            height = bar.get_height()
            ax.annotate('{:,}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 puntos de desplazamiento vertical
                        textcoords="offset points",
                        ha='center', va='bottom',rotation=rot)
        
        ax.set_xlabel(self.var_xlabel.get())
        ax.set_ylabel(self.var_xlabel.get())
        ax.set_title(self.var_title.get())
        ax.set_xticks(range(len(categorias_pagina)))
        ax.set_xticklabels(categorias_pagina, rotation=15, ha='right')
        
        self.canvas = FigureCanvasTkAgg(fig, self.new_window)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=3,sticky="new")

    def filtro_categoría_cambiada(self, event):
        self.index_final = 10
        self.index_inicial = 0
        self.numero_pagina = 1
        try:
            categoria =  self.entry_mod_categoria.get()
            if (categoria == self.filtros_cat[0]): # Valor cartera
                result = BD_Socios.obtener_valor_en_mora_socios()
                values = [item[UsuarioDB.total_cartera] for item in result]
                rotacion = 15
            else: # Dias en mora
                result = BD_Socios.obtener_fechas_en_mora_socios()
                hoy = datetime.datetime.now()
                aux_result = []
                for cliente in result:
                    fecha_abono = datetime.datetime.strptime(cliente[UsuarioDB.ultima_fecha_abono], '%Y-%m-%d')
                    dias_mora = (hoy - fecha_abono).days
                    if dias_mora >= 1:
                        cliente[UsuarioDB.ultima_fecha_abono] = dias_mora
                        aux_result.append(cliente)
                        
                result = aux_result
                values = [item[UsuarioDB.ultima_fecha_abono] for item in result]
                rotacion = 0
            
            self.categorias = [item[UsuarioDB.nombre][:16] for item in result]
            self.values = values
            self.numero_total_paginas = len(values)//10 + 1
            
            self.var_ylabel.set("Pesos")
            self.var_title.set(f"{categoria}: Usuarios")        
            self.pintar_datos(rotacion, self.categorias[self.index_inicial:self.index_final], self.values[self.index_inicial:self.index_final])
            
        except:
            messagebox.showinfo("LMH SOLUTIONS", "No hay clientes en mora")
    
    def siguiente_pagina(self, event):
        self.numero_pagina = self.numero_pagina + 1
        if (self.numero_pagina <= self.numero_total_paginas):
            self.index_inicial = (self.numero_pagina-1)*self.numero_items_por_frame - 1
            self.index_final = (self.numero_pagina)*self.numero_items_por_frame
            
            numero_items = len(self.values)
            if (self.index_final > numero_items):
                self.index_final = numero_items
                self.index_inicial = numero_items - numero_items%10 - 1
            
            self.pintar_datos(15, self.categorias[self.index_inicial:self.index_final], self.values[self.index_inicial:self.index_final])
    
        else:
            self.numero_pagina = self.numero_total_paginas
    def anterior_pagina(self, event):
        self.numero_pagina = self.numero_pagina - 1
        if (self.numero_pagina >1):
            self.index_inicial = (self.numero_pagina-1)*self.numero_items_por_frame - 1
            self.index_final = (self.numero_pagina)*self.numero_items_por_frame
            
            numero_items = len(self.values)
            if (self.index_final > numero_items):
                self.index_final = numero_items
                self.index_inicial = numero_items - numero_items%10 - 1
            
            self.pintar_datos(15, self.categorias[self.index_inicial:self.index_final], self.values[self.index_inicial:self.index_final])

        else:
            self.numero_pagina = 1
            self.index_inicial = 0
            self.index_final = 10
            self.pintar_datos(15, self.categorias[self.index_inicial:self.index_final], self.values[self.index_inicial:self.index_final])
            
        