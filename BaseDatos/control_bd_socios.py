import sqlite3
from tkinter import messagebox
from utilidades.excepcion import ErrorBusqueda as ExcepBus
import pandas as pd


class UsuarioDB:
    cedula = "Cedula"
    nombre= "Nombre"
    total_cartera = "Total_Cartera"
    total_comprado = "Total_Comprado"
    
class BD_Socios:
    name_bd = "./BaseDatos/BaseDatos.db"
    
    @classmethod
    def agregar_socio(cls,user):
        try:
            str = f"""INSERT INTO Socios
            ({UsuarioDB.cedula},{UsuarioDB.nombre}, {UsuarioDB.total_cartera}, {UsuarioDB.total_comprado}) 
            VALUES ('{user[UsuarioDB.cedula]}','{user[UsuarioDB.nombre]}',{user[UsuarioDB.total_cartera]},{user[UsuarioDB.total_comprado]})"""
            
            conn = sqlite3.connect(cls.name_bd)
            cur = conn.cursor()
            cur.execute(str)
            conn.commit()
            conn.close()
        except:
            messagebox.showwarning("SOFTRU SOLUCIONS", "Algo ha ocurrido con la base de datos")
            conn.close()
        
    @classmethod
    def eliminar_socio(cls,cedula):
        str = f""" DELETE FROM Socios WHERE Cedula='{cedula}';"""
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        cur.execute(str)
        conn.commit()
        conn.close()
        
    @classmethod
    def actualizar_nombre_socio(cls,user):
        str = f""" UPDATE Socios
                    SET {UsuarioDB.nombre} = {user[UsuarioDB.nombre]}
                    WHERE {UsuarioDB.cedula} = '{user[UsuarioDB.cedula]}'"""
        conn = sqlite3.connect(cls.name_bd)           
        cur = conn.cursor()
        cur.execute(str)
        conn.commit()
        conn.close()
        
        
    @classmethod
    def agregar_saldo_user(cls,user):
        str = f""" UPDATE Socios
                    SET {UsuarioDB.total_cartera} = {user[UsuarioDB.total_cartera]}, {UsuarioDB.total_comprado} = {user[UsuarioDB.total_comprado]}
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
                            WHERE {UsuarioDB.nombre} like '{clave}%'"""        
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