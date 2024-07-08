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
    def esta_el_producto_cod(cls,cod):
        hay_producto = False
        str = f""" SELECT * FROM Inventario
                    WHERE {ProductoDB.codigo} = '{cod}'"""
                    
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        
        if len(res)>0:
            hay_producto = True
        
        return hay_producto
    @classmethod
    def esta_el_producto_nombre(cls,nombre):
        hay_producto = False
        str = f""" SELECT * FROM Inventario
                    WHERE {ProductoDB.nombre} = '{nombre}'"""
                    
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        
        if len(res)>0:
            hay_producto = True
        
        return hay_producto
    
    @classmethod
    def obtener_productos(cls):
        str = f"SELECT * FROM Inventario ORDER BY {ProductoDB.codigo}"
                    
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        
        if len(res) >0:
            lista_producto = []
            for producto in res:
                lista_producto.append(cls.formaterProducto(producto))
            return lista_producto
        else:
            raise ExcepBus("No se encuentran productos")
    
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
            messagebox.showerror("LMH SOLUTIONS", "Ya ha ingresado artículo con ese código o nombre")
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
            return cls.formaterProducto(res[0])
            #res[0] # (cod, nombre, precio, precio_compra, cantidad)
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
            return cls.formaterProducto(res[0])
        else:
            raise ExcepBus("Producto no encontrado")
    
    @classmethod
    def buscar_producto_nombre_por_codigo(cls,codigo):
        str = f""" SELECT {ProductoDB.nombre} FROM Inventario
                    WHERE {ProductoDB.codigo} = '{codigo}'"""            
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        
        if len(res) >0:
            return res[0][0]
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
    def modificar_cantidad_producto(cls, codigo, cantidad):
        str = f""" UPDATE Inventario
                    SET {ProductoDB.cantidad} = {cantidad} 
                    WHERE {ProductoDB.codigo} = '{codigo}'"""
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
                p_actualizado = [producto[ProductoDB.codigo], producto[ProductoDB.nombre], row[ProductoDB.precio], row[ProductoDB.precio_entrada], row[ProductoDB.cantidad]+producto[ProductoDB.cantidad]]
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
                cantidad = producto[ProductoDB.cantidad]-row[ProductoDB.cantidad]
                cls.modificar_cantidad_producto(producto[ProductoDB.codigo], cantidad)
            except:
                messagebox.showerror("LMH SOLUTIONS", "Algo inesperado ha ocurrido con un código interno en la base de datos")
    
    @classmethod
    def retornar_valor_compras_stock(cls, df:pd.DataFrame):
        lista_codigos = []
        lista_cantidades = []
        tupla_codigo_cantidad = []
        for index, row in df.iterrows():
            lista_codigos.append(row[ProductoDB.codigo])
            lista_cantidades.append(row[ProductoDB.cantidad])
            tupla_codigo_cantidad.append((row[ProductoDB.codigo], ProductoDB.cantidad))
        
        values = ','.join('?' for _ in lista_codigos)
        str = f""" SELECT {ProductoDB.codigo},{ProductoDB.precio_entrada} 
                    FROM Inventario 
                    WHERE {ProductoDB.codigo} IN ({values})"""
        
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str, list(lista_codigos))
        res = res.fetchall()
        conn.close()
        
        dict_codigo_precioEntrada = dict(res)
            
        suma = 0
        for codigo,cantidad in zip(lista_codigos, lista_cantidades):
            if codigo in dict_codigo_precioEntrada:
                suma = suma + dict_codigo_precioEntrada[codigo]*cantidad
        return suma
        
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

    @classmethod
    def formaterProducto(cls, producto):
        return {
            ProductoDB.codigo: producto[0],
            ProductoDB.nombre: producto[1],
            ProductoDB.precio: producto[2],
            ProductoDB.precio_entrada: producto[3],
            ProductoDB.cantidad: producto[4]
        }
    