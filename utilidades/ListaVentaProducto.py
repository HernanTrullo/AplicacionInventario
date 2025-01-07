from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from utilidades.ListaProducto import Producto
from BaseDatos.VentasBD import VentaEstructuraSql

class ListaProductoVenta(ttk.Treeview):
    def __init__(self, root, win,col):
        self.df = pd.DataFrame()
        for column in col:
            self.df[column] = None
        
        super().__init__(root, columns=list(self.df.columns), show="headings")
        self.win = win
        # Configuración de los nombres de las columnas
        i = 0
        for column in self.df.columns:
            self.heading(column, text=column)
            if i<2:
                self.column(column, anchor="w", width=60)
            if i ==2:
                self.column(column, anchor="w", width=80)
            else:
                self.column(column, anchor="center", width=50)
            i +=1
                
        self.pack(side="left",fill=BOTH, expand=True, padx=5, pady=15)
        
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.yview)
        self.scrollbar.pack(fill="y", side="right",padx=5, pady=15)
        
        # Configurar la Treeview para que utilice la Scrollbar
        self.configure(yscrollcommand=self.scrollbar.set)
        
        
    def agregar_producto_venta(self, producto_dict):
        self.vaciar_productos()
        for data in producto_dict:
            self.df = pd.concat([self.df, pd.DataFrame(data)], ignore_index=True)
        self.actualizar()
    
        
    def actualizar(self):
        # Borrar todos
        for item in self.get_children():
            self.delete(item)
            
        self.filas_principales = []
        for i,row in self.df.iterrows():
            self.filas_principales.append(self.insert('', 'end',values= list(row)))
            
    def vaciar_productos(self):
        # Borrar todos
        for item in self.get_children():
            self.delete(item)
            
        self.df = self.df.drop(self.df.index)
        
    def retornar_productos(self):
        return self.df
    
    def retornar_item_producto(self):
        item = self.selection()[0]  # Obtener la fila seleccionada
        valores = self.item(item, "values")
        
        data = {
            VentaEstructuraSql.id: valores[0],
            Producto.codigo : valores[1],
            Producto.cantidad : valores[4],
            Producto.precio: valores[3]
        }
        return data
    
    