from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd

class Producto:
    codigo = "Codigo"
    nombre =   "Nombre"
    precio = "Precio"
    cantidad = "Cantidad"
    precio_entrada = "Precio_Entrada"
    sub_total = "Sub_Total"
    


class ListaProducto(ttk.Treeview):
    def __init__(self, root, win,col):
        self.df = pd.DataFrame()
        for column in col:
            self.df[column] = None
        self.df[Producto.sub_total] = None
        
        super().__init__(root, columns=list(self.df.columns), show="headings")
        self.win = win
        # Configuración de los nombres de las columnas
        i = 0
        for column in self.df.columns:
            self.heading(column, text=column)
            if i<2:
                self.column(column, anchor="w")
                
            else:
                self.column(column, anchor="center", width=150)
            i +=1
                
        self.pack(side="left",fill=BOTH, expand=True, padx=5, pady=15)
        
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.yview)
        self.scrollbar.pack(fill="y", side="right",padx=5, pady=15)
        
        # Evento del doble click de cada fila
        self.bind("<Double-1>", self.doble_click_mod_productos)
        
        # Configurar la Treeview para que utilice la Scrollbar
        self.configure(yscrollcommand=self.scrollbar.set)
    
    
    
    def doble_click_mod_productos(self, event):
        item = self.selection()[0]  # Obtener la fila seleccionada
        valores = self.item(item, "values")
        self.win.doble_click_producto_modificar(valores)
        
    def eliminar_producto_auto(self, event):
        self.eliminar_producto()
        
    def agregar_producto(self, dict):
        if len(dict) == 4:
            data = {
                Producto.codigo:dict[Producto.codigo],
                Producto.nombre: dict[Producto.nombre],
                Producto.precio: dict[Producto.precio],
                Producto.cantidad: dict[Producto.cantidad],
                Producto.sub_total: [dict[Producto.precio][0] * dict[Producto.cantidad][0]]
            }
        elif len(dict)==5:
            data = {
                Producto.codigo:dict[Producto.codigo],
                Producto.nombre: dict[Producto.nombre],
                Producto.precio: dict[Producto.precio],
                Producto.precio_entrada:dict[Producto.precio_entrada],
                Producto.cantidad: dict[Producto.cantidad],
                Producto.sub_total: [dict[Producto.precio][0] * dict[Producto.cantidad][0]]
            }
        
        # Se coloca [0] pues viene de una lista 
        res = self.df.loc[self.df[Producto.codigo] == data[Producto.codigo][0]]
        if res.empty:
            self.df = pd.concat([self.df, pd.DataFrame(data)], ignore_index=True)
        else:
            cantidad_actual = res[Producto.cantidad].iloc[0]
            cantidad_actual +=data[Producto.cantidad][0]
            self.df.loc[self.df[Producto.codigo] == data[Producto.codigo][0], Producto.cantidad] = cantidad_actual
            self.df.loc[self.df[Producto.codigo] == data[Producto.codigo][0], Producto.sub_total] = data[Producto.sub_total][0] * cantidad_actual
        
        self.actualizar()
    
    def eliminar_producto(self): 
        selected_item = self.selection()
        if selected_item:
            res = messagebox.askokcancel("LMH SOLUTIONS", "Está seguro que desea eliminar el producto")
            if res:
                for s_item in selected_item:
                    self.df.drop(self.index(s_item),inplace=True)  
                
                self.df.reset_index(drop=True, inplace=True)         
        else:
            messagebox.showwarning("LMH SOLUTIONS", "!No ha seleccionado ningún producto¡")   
        
        self.actualizar()    
    
    def modificar_producto(self, dict):
        if len(dict) == 4:
            data = {
                Producto.codigo:dict[Producto.codigo],
                Producto.nombre: dict[Producto.nombre],
                Producto.precio: dict[Producto.precio],
                Producto.cantidad: dict[Producto.cantidad],
                Producto.sub_total: [dict[Producto.precio][0] * dict[Producto.cantidad][0]]
            }
            self.df.loc[self.df[Producto.codigo] == data[Producto.codigo][0], Producto.cantidad]= data[Producto.cantidad][0]
            self.df.loc[self.df[Producto.codigo] == data[Producto.codigo][0], Producto.sub_total]= data[Producto.sub_total][0]
            
        elif len(dict)==5:
            data = {
                Producto.codigo:dict[Producto.codigo],
                Producto.nombre: dict[Producto.nombre],
                Producto.precio: dict[Producto.precio],
                Producto.precio_entrada:dict[Producto.precio_entrada],
                Producto.cantidad: dict[Producto.cantidad],
                Producto.sub_total: [dict[Producto.precio][0] * dict[Producto.cantidad][0]]
            }
            self.df.loc[self.df[Producto.codigo] == data[Producto.codigo][0], Producto.cantidad]= data[Producto.cantidad][0]
            self.df.loc[self.df[Producto.codigo] == data[Producto.codigo][0], Producto.precio]= data[Producto.precio][0]
            self.df.loc[self.df[Producto.codigo] == data[Producto.codigo][0], Producto.precio_entrada]= data[Producto.precio_entrada][0]
            self.df.loc[self.df[Producto.codigo] == data[Producto.codigo][0], Producto.sub_total]= data[Producto.sub_total][0]
            
        self.actualizar()
        
    def actualizar(self):
        # Borrar todos
        for item in self.get_children():
            self.delete(item)
            
        # Insertar datos en la tabla
        for i,row in self.df.iterrows():
            self.insert('', 'end', values= list(row)) 
            
    
    def vaciar_productos(self):
        # Borrar todos
        for item in self.get_children():
            self.delete(item)
            
        self.df = self.df.drop(self.df.index)
        
    def retornar_productos(self):
        return self.df
    
    def calcular_precio_productos(self):
        precio_total = 0
        for i,row in self.df.iterrows():
            precio = row[Producto.precio] * row[Producto.cantidad]
            precio_total +=precio
        
        return precio_total
    
    def calcular_precio_productos_entrada(self):
        precio_total = 0
        for i,row in self.df.iterrows():
            precio = row[Producto.precio_entrada] * row[Producto.cantidad]
            precio_total +=precio
        
        return precio_total
    

    def calcular_precio_productos_vendido(self):
        precio_total = 0
        for i,row in self.df.iterrows():
            precio = row[Producto.precio] * row[Producto.cantidad]
            precio_total +=precio
        
        return precio_total