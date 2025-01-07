import tkinter as tk
from tkinter import ttk
from BaseDatos.InventarioBD import BD_Inventario as BD
from utilidades.EntryP import LabelP
from datetime import datetime
from BaseDatos.VentasBD import VentasSql
import TopLevels.controller as controller
from tkinter import messagebox
from utilidades.excepcion import ErrorBusqueda

class TopLevelWinCierreCaja:
    def __init__(self, parent, saldo, ventas, efectivo, valor_pagado):
        self.new_window1 = tk.Toplevel(parent)
        self.new_window1.title("Cierre de Caja")
        self.new_window1.geometry("700x500")
        
        self.new_window = ttk.Labelframe(self.new_window1, style="Cabecera.TFrame")
        self.new_window.pack(fill="both", expand=True)
        
        self.var_ventas_diarias = tk.IntVar()
        self.var_saldo = tk.IntVar()
        self.var_ventas_saldo = tk.IntVar()
        self.var_saldo_efectivo = tk.IntVar()
        self.var_saldo_pagado = tk.IntVar()
        
        self.var_buscar_nombre = tk.StringVar()
        self.var_cantidad = tk.StringVar()
        
        # Agregar contenido a la nueva ventana
        self.lb_nombre_producto = ttk.Label(self.new_window, text="Nombre Producto",style="CCustomMedium.TLabel")
        self.lb_nombre_producto.grid(row=0, column=0, sticky="e")
        self.entry_nombre_producto = ttk.Combobox(self.new_window, textvariable=self.var_buscar_nombre)
        self.entry_nombre_producto.grid(row=0, column=1, sticky="ew")
        self.lb_cantidad = ttk.Label(self.new_window, textvariable=self.var_cantidad,style="CCustomMedium.TLabel").grid(row=0, column=2, sticky="w", padx=10)
        self.entry_nombre_producto.bind("<<ComboboxSelected>>", self.on_selected_nombre)
        
        self.lb_ventas_diarias = ttk.Label(self.new_window, text="Total (Ventas Diarias): ", style="CCustomMedium.TLabel").grid(row=1, column=0, sticky="e")
        self.ventas_diarias = LabelP(self.new_window, self.var_ventas_diarias, style="CCustomMedium.TLabel");
        self.ventas_diarias.grid(row=1, column=1, sticky="nse")
        
        self.lb_saldo_diario_pagado = ttk.Label(self.new_window, text="Valor pagado clientes: ", style="CCustomMedium.TLabel").grid(row=2, column=0, sticky="e")
        self.saldo_diario_pagado = LabelP(self.new_window, self.var_saldo_pagado, style="CCustomMedium.TLabel");
        self.saldo_diario_pagado.grid(row=2, column=1, sticky="nse")
        
        self.lb_saldo_diario = ttk.Label(self.new_window, text="Saldo Caja: ", style="CCustomMedium.TLabel").grid(row=3, column=0, sticky="e")
        self.saldo_diario = LabelP(self.new_window, self.var_saldo, style="CCustomMedium.TLabel");
        self.saldo_diario.grid(row=3, column=1, sticky="nse")
        
        self.lb_saldo_diario_efectivo = ttk.Label(self.new_window, text="Saldo efectivo: ", style="CCustomMedium.TLabel").grid(row=4, column=0, sticky="e")
        self.saldo_diario_efectivo = LabelP(self.new_window, self.var_saldo_efectivo, style="CCustomMedium.TLabel");
        self.saldo_diario_efectivo.grid(row=4, column=1, sticky="nse")
        
        self.lb_ventas_saldo = ttk.Label(self.new_window, text="Total Caja (Efectivo + Saldo caja): ",style="CCustomMedium.TLabel").grid(row=5, column=0, sticky="e")
        self.ventas_saldo = LabelP(self.new_window, self.var_ventas_saldo, style="CCustomMedium.TLabel");
        self.ventas_saldo.grid(row=5, column=1, sticky="nse") 
        
        self.var_ventas_diarias.set(ventas)
        self.var_saldo.set(saldo)
        self.var_saldo_efectivo.set(efectivo)
        self.var_saldo_pagado.set(valor_pagado)
        self.var_ventas_saldo.set(int(efectivo)+int(saldo))
        
        self.formatear_variables()
        self.expandir_widget(self.new_window, row=6, colum=3)
        
        self.var_cantidad.set("Cant: 0")
        self.actualizar_nombre_productos()
        
    def formatear_variables(self):
        self.ventas_diarias.formatear_valor()
        self.saldo_diario.formatear_valor()
        self.ventas_saldo.formatear_valor()
        self.saldo_diario_efectivo.formatear_valor()
        self.saldo_diario_pagado.formatear_valor()
    
    def expandir_widget(self, frame:ttk.LabelFrame, row=2, colum=2):
        for i in range(row):
            frame.rowconfigure(i, weight=1)
        for i in range(colum):
            frame.columnconfigure(i, weight=1)
            
    def actualizar_nombre_productos(self):
        try:
            fecha = datetime.now().strftime("%Y-%m-%d")
            codigos_json = VentasSql.retornar_codigo_productos_vendidos(fecha)
            resultado = controller.obtener_dict_codigo_cantidad(codigos_json)
            
            self.lista_nombres = []        
            for codigo, cantidad in resultado.items():
                self.lista_nombres.append({"nombre":BD.buscar_producto_nombre_por_codigo(codigo),
                                        "cantidad": cantidad})
                
            self.entry_nombre_producto['values']= [dict["nombre"] for dict in self.lista_nombres]
        except ErrorBusqueda as e:
            messagebox.showinfo("LMH SOLUTIOS", "No se han encontrado ventas en las fechas establecidas")
        
        except:
            messagebox.showerror("LMH SOLUTIOS", "Ha ocurrido un error en la base de datos,\nPor favor comunicarse con el soporte")
            
    
    def on_selected_nombre(self,event):
        selected_item = self.entry_nombre_producto.get()
        cantidad = 0
        for dict in self.lista_nombres:
            if dict["nombre"] == selected_item:
                cantidad = dict["cantidad"]
                
        self.var_cantidad.set(f"Cant: {cantidad}")