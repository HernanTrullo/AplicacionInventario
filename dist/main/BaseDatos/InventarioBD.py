import sqlite3
from tkinter import messagebox
from utilidades.excepcion import ErrorBusqueda as ExcepBus
import pandas as pd


class ProductoDB:
    codigo = "Codigo"
    nombre= "Nombre"
    precio = "Precio"
    precio_entrada = "Precio_Entrada"
    cantidad = "Cantidad"


class BD_Inventario():
    name_bd = "./BaseDatos/BaseDatos.db"
    
    @classmethod
    def obtener_productos(cls):
        str = "SELECT * FROM Inventario"
                    
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        
        if len(res) >0:
            return res
        else:
            raise ExcepBus("No se encunetran productos")
    
    @classmethod
    def agregar_productos(cls,productos):
        try:
            str = f"""INSERT INTO Inventario
            ({ProductoDB.codigo},{ProductoDB.nombre},{ProductoDB.precio},{ProductoDB.precio_entrada},{ProductoDB.cantidad}) 
            VALUES (?,?,?,?,?)"""
            
            conn = sqlite3.connect(cls.name_bd)
            cur = conn.cursor()
            cur.executemany(str, productos)
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("SOFTRULLO SOLUCIONS", "Ya ha ingresado artículo con ese código o nombre")
            conn.close()
    
    @classmethod
    def buscar_producto_cod(cls,cod):
        str = f""" SELECT * FROM Inventario
                    WHERE {ProductoDB.codigo} = '{cod}'"""
                    
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        
        if len(res) >0:
            return res[0] # (cod, nombre, precio, precio_compra, cantidad)
        else:
            raise ExcepBus("Producto no encontrado")
    
    @classmethod
    def buscar_producto_nombre(cls,nombre):
        str = f""" SELECT * FROM Inventario
                    WHERE {ProductoDB.nombre} = '{nombre}'"""
                    
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        
        if len(res) >0:
            return res[0]
        else:
            raise ExcepBus("Producto no encontrado")
    
    @classmethod
    def modificar_producto(cls, producto):
        str = f""" UPDATE Inventario
                    SET {ProductoDB.precio} = {producto[2]}, {ProductoDB.precio_entrada}={producto[3]},{ProductoDB.cantidad} = {producto[4]} 
                    WHERE {ProductoDB.codigo} = '{producto[0]}'"""
        conn = sqlite3.connect(cls.name_bd)           
        cur = conn.cursor()
        cur.execute(str)
        
        conn.commit()
        conn.close()
    
    @classmethod 
    def modificar_cantidad_producto(cls, producto):
        str = f""" UPDATE Inventario
                    SET {ProductoDB.cantidad} = {producto[1]} 
                    WHERE {ProductoDB.codigo} = '{producto[0]}'"""
        conn = sqlite3.connect(cls.name_bd)           
        cur = conn.cursor()
        cur.execute(str)
        
        conn.commit()
        conn.close()            
        
        
        
    @classmethod
    def cargar_inventario(cls,df:pd.DataFrame):
        for index,row in df.iterrows():
            try:
                producto = cls.buscar_producto_cod(row[ProductoDB.codigo])
                p_actualizado = [producto[0], producto[1], row[ProductoDB.precio], row[ProductoDB.precio_entrada], row[ProductoDB.cantidad]+producto[4]]
                cls.modificar_producto(p_actualizado)
            except ExcepBus as e:
                producto = [
                    (row[ProductoDB.codigo], row[ProductoDB.nombre], row[ProductoDB.precio], row[ProductoDB.precio_entrada], row[ProductoDB.cantidad])
                ]
                cls.agregar_productos(producto)
            
    
    @classmethod
    def sacar_productos(cls, df:pd.DataFrame):
        for index,row in df.iterrows():
            try:
                producto = cls.buscar_producto_cod(row[ProductoDB.codigo])
                p_actualizado = [producto[0], producto[4]-row[ProductoDB.cantidad]]
                cls.modificar_cantidad_producto(p_actualizado)
            except:
                messagebox.showerror("SOFTRULLO SOLUCIONS", "Algo inesperado ha ocurrido con un código interno en la base de datos")
                
    @classmethod
    def retornar_nombres_productos(cls, clave):
        str = f""" SELECT {ProductoDB.nombre} FROM Inventario
                            WHERE {ProductoDB.nombre} like '%{clave}%'"""        
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        if len(res) >0:
            return [nombres[0] for nombres in res]
        else:
            raise ExcepBus("Nombre no encontrado")
                
