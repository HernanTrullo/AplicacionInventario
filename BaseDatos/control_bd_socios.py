import sqlite3
from tkinter import messagebox
from utilidades.excepcion import ErrorBusqueda as ExcepBus
import pandas as pd
from datetime import datetime


class UsuarioDB:
    cedula = "Cedula"
    nombre= "Nombre"
    total_cartera = "Total_Cartera"
    total_comprado = "Total_Comprado"
    ultima_fecha_abono = "Ultima_Fecha_Abono"
    
class BD_Socios:
    name_bd = "./BaseDatos/BaseDatos.db"
    
    @classmethod
    def agregar_socio(cls,user):
        try:
            str = f"""INSERT INTO Socios
            ({UsuarioDB.cedula},{UsuarioDB.nombre}, {UsuarioDB.total_cartera}, {UsuarioDB.total_comprado}, {UsuarioDB.ultima_fecha_abono}) 
            VALUES ('{user[UsuarioDB.cedula]}','{user[UsuarioDB.nombre]}',{user[UsuarioDB.total_cartera]},{user[UsuarioDB.total_comprado]}, '{datetime.now().strftime("%Y-%m-%d")}')"""
            
            conn = sqlite3.connect(cls.name_bd)
            cur = conn.cursor()
            cur.execute(str)
            conn.commit()
            conn.close()
        except:
            messagebox.showwarning("SOFTRU SOLUCIONS", "Algo ha ocurrido con la base de datos")
            conn.close()
    
    @classmethod
    def guardar_info_usuarios(cls, df:pd.DataFrame):
        for index,row in df.iterrows():
            try:
                socio = cls.buscar_socio_cedula(row[UsuarioDB.cedula])
                cls.actualizar_socio(row)
            except ExcepBus as e:
                socio ={
                    UsuarioDB.cedula: row[UsuarioDB.cedula],
                    UsuarioDB.nombre: row[UsuarioDB.nombre],
                    UsuarioDB.total_cartera: row[UsuarioDB.total_cartera],
                    UsuarioDB.total_comprado: row[UsuarioDB.total_comprado],
                    UsuarioDB.ultima_fecha_abono: datetime.now().strftime("%Y-%m-%d")
                }
                cls.agregar_socio(socio)
    
    @classmethod
    def eliminar_socio(cls,cedula):
        str = f""" DELETE FROM Socios WHERE Cedula='{cedula}';"""
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        cur.execute(str)
        conn.commit()
        conn.close()
        
    @classmethod
    def actualizar_socio(cls,user):
        str = f""" UPDATE Socios
                    SET {UsuarioDB.total_cartera} = {user[UsuarioDB.total_cartera]}, {UsuarioDB.ultima_fecha_abono}='{datetime.now().strftime("%Y-%m-%d")}'
                    WHERE {UsuarioDB.cedula} = '{user[UsuarioDB.cedula]}'"""
        
        
        conn = sqlite3.connect(cls.name_bd)           
        cur = conn.cursor()
        cur.execute(str)
        conn.commit()
        conn.close()
        
    
    
    @classmethod
    def obtener_usuarios(cls):
        str = f"SELECT * FROM Socios ORDER BY {UsuarioDB.total_cartera}"
                    
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        
        if len(res) >0:
            return res
        else:
            raise ExcepBus("Socios no encontrado")
        
    @classmethod
    def buscar_socio_nombre(cls,nombre):
        str = f""" SELECT * FROM Socios
                    WHERE {UsuarioDB.nombre} = '{nombre}'"""
                    
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        
        if len(res) >0:
            return res[0]
        else:
            raise ExcepBus("Socio no encontrado")
        
    @classmethod
    def retornar_nombres_socios(cls, clave):
        str = f""" SELECT {UsuarioDB.nombre} FROM Socios
                            WHERE {UsuarioDB.nombre} like '%{clave}%'"""        
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
    def buscar_socio_cedula(cls,cod):
        str = f""" SELECT * FROM Socios
                    WHERE {UsuarioDB.cedula} = '{cod}'"""
                    
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        
        if len(res) >0:
            return res[0]
        else:
            raise ExcepBus("Socio no encontrado")
        
    @classmethod
    def buscar_socios_nombre(cls, clave):
        str = f""" SELECT {UsuarioDB.cedula} FROM Socios
                            WHERE {UsuarioDB.cedula} like '{clave}%'"""        
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        if len(res) >0:
            return [cedulas[0] for cedulas in res]
        else:
            raise ExcepBus("Nombre no encontrado")
    
    @classmethod
    def obtener_fechas_en_mora_socios(cls):
        str = f""" SELECT {UsuarioDB.nombre}, {UsuarioDB.ultima_fecha_abono} 
                    FROM Socios
                    WHERE {UsuarioDB.total_cartera} > 0
                    ORDER By {UsuarioDB.ultima_fecha_abono} DESC
                    """        
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        if len(res) >0:
            return [{UsuarioDB.nombre: item[0], UsuarioDB.ultima_fecha_abono: item[1]} for item in res]
        else:
            raise ExcepBus("Nombre no encontrado")
    
    @classmethod
    def obtener_valor_en_mora_socios(cls):
        str = f""" SELECT {UsuarioDB.nombre}, {UsuarioDB.total_cartera} 
                    FROM Socios
                    WHERE {UsuarioDB.total_cartera} > 0 
                    ORDER By {UsuarioDB.total_cartera} DESC
                    """
                    
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        if len(res) >0:
            return [{UsuarioDB.nombre: item[0], UsuarioDB.total_cartera: item[1]} for item in res][:20]
        else:
            raise ExcepBus("Nombre no encontrado")