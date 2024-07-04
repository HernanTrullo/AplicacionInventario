import sqlite3
from tkinter import messagebox
from utilidades.excepcion import ErrorBusqueda as ExcepBus


class BD_Usuario:
    name_bd = "./BaseDatos/BaseDatos.db"
    
    @classmethod
    def buscar_usuario(cls, user, password):
        str = f"""SELECT * FROM UsuariosMercadeo
                    WHERE {BD_Usuario_Mod.user} = '{user}' AND {BD_Usuario_Mod.password} = '{password}'"""
                    
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        
        if len(res) >0:
            return res[0]
        else:
            raise ExcepBus("Usuario No Encontrado")
    
    @classmethod  
    def es_admin(cls, user, password):
        resp = cls.buscar_usuario(user, password)
        return (resp[4], (resp[0], resp[1], resp[2], resp[3]))
    
    @classmethod
    def add_user(cls, nombre, apellido, user, password, es_admin):
        try:
            str = f"""INSERT INTO UsuariosMercadeo
                    ({BD_Usuario_Mod.nombre},{BD_Usuario_Mod.apellido},{BD_Usuario_Mod.user},{BD_Usuario_Mod.password},{BD_Usuario_Mod.es_admin})
                    VALUES (?,?,?,?,?)"""

            us = (nombre, apellido, user, password, es_admin)
            
            conn = sqlite3.connect(cls.name_bd)
            cur = conn.cursor()
            res = cur.execute(str, us)
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("LMH SOLUTIONS","Usuario invalido o repetido")
            conn.close()
        

class BD_Usuario_Mod:
    user="User"
    password="PassWord"
    es_admin = "Es_Admin"
    nombre = "Nombre"
    apellido = "Apellido"
    

