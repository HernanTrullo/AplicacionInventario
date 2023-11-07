import sqlite3
from tkinter import messagebox

class BD_Variables:
    name_bd = "./BaseDatos/BaseDatos.db"
    
    # Codigos de las variables de que se almacenas temporalmente durante un dia 
    ventas_tem_dia = "VVentas_001"
    clave_admin = "ClaveAdmin"
    
    @classmethod
    def get_valor_variable(cls, cod):
        str = f" SELECT {BD_Variables_Mod.valor} FROM Variables WHERE {BD_Variables_Mod.id} = '{cod}'"         
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        return res[0]
    
    @classmethod
    def set_valor_variable(cls, cod, value):
        str = f""" UPDATE Variables
                    SET {BD_Variables_Mod.valor} = '{value}' 
                    WHERE {BD_Variables_Mod.id} = '{cod}';"""
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        conn.commit()
        conn.close()
                
    @classmethod
    def set_valor_ventas_turno(cls, value):
        cls.set_valor_variable(cls.ventas_tem_dia, value)
    
    @classmethod
    def get_valor_ventas_turno(cls):
        return cls.get_valor_variable(cls.ventas_tem_dia)[0]
    
    @classmethod    
    def set_clave_admin(cls,value):
        cls.set_valor_variable(cls.clave_admin, value)
    
    @classmethod
    def get_clave_admin(cls):    
        return cls.get_valor_variable(cls.clave_admin)[0]
    
    @classmethod
    def reset_valor_ventas_turno(cls): # Se resetea el valor de las ventas a cero
        cls.set_valor_variable(cls.ventas_tem_dia,0)
        
class BD_Variables_Mod():
    valor = "Valor"
    id = "ID"