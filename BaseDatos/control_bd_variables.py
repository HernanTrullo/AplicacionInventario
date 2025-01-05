import sqlite3
from tkinter import messagebox

class BD_Variables:
    name_bd = "./BaseDatos/BaseDatos.db"
    
    # Codigos de las variables de que se almacenas temporalmente durante un dia 
    name_tabla = "Variables"
    ventas_tem_dia = "VVentas_001"
    valor_compras_tem_dia = "VCompras_001"
    saldo_caja = "SaldoCaja_001"
    saldo_efectivo = "SaldoEfectivo_001"
    saldo_pagado = "SaldoPagado_001"
    saldo_fiado = "SaldoFiado_001"
    clave_admin = "ClaveAdmin"
    
    @classmethod
    def get_valor_variable(cls, cod):
        str = f" SELECT {BD_Variables_Mod.valor} FROM {cls.name_tabla} WHERE {BD_Variables_Mod.id} = '{cod}'"         
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        return res[0]
    
    @classmethod
    def set_valor_variable(cls, codigo_variable, valor_variable):
        str = f""" UPDATE {cls.name_tabla}
                    SET {BD_Variables_Mod.valor} = '{valor_variable}' 
                    WHERE {BD_Variables_Mod.id} = '{codigo_variable}';"""
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        cur.execute(str)
        conn.commit()
        conn.close()
                
    @classmethod
    def set_valor_ventas_turno(cls, value):
        cls.set_valor_variable(cls.ventas_tem_dia, value)
    
    @classmethod
    def get_valor_ventas_turno(cls):
        return cls.get_valor_variable(cls.ventas_tem_dia)[0]
    
    @classmethod
    def set_valor_comprado_stock(cls, value):
        cls.set_valor_variable(cls.valor_compras_tem_dia, value)
        
    @classmethod
    def get_valor_comprado_stock(cls):
        return cls.get_valor_variable(cls.valor_compras_tem_dia)[0]
    
    @classmethod    
    def set_clave_admin(cls,value):
        cls.set_valor_variable(cls.clave_admin, value)
    
    @classmethod
    def get_clave_admin(cls):    
        return cls.get_valor_variable(cls.clave_admin)[0]
    
    @classmethod
    def get_saldo_caja(cls):
        return cls.get_valor_variable(cls.saldo_caja)[0]

    @classmethod
    def set_saldo_caja(cls, value):
        return cls.set_valor_variable(cls.saldo_caja, value)
    
    @classmethod
    def set_saldo_efectivo(cls, value):
        cls.set_valor_variable(cls.saldo_efectivo, value)
    
    @classmethod
    def set_saldo_pagado(cls, value):
        cls.set_valor_variable(cls.saldo_pagado, value)
    
    @classmethod
    def set_saldo_fiado(cls, value):
        cls.set_valor_variable(cls.saldo_fiado, value)
    
    @classmethod
    def get_saldo_efectivo(cls):
        return cls.get_valor_variable(cls.saldo_efectivo)[0]
    
    @classmethod
    def get_saldo_fiado(cls):
        return cls.get_valor_variable(cls.saldo_fiado)[0]
    
    @classmethod
    def get_saldo_pagado_clientes(cls):
        return cls.get_valor_variable(cls.saldo_pagado)[0]
    
    @classmethod
    def reset_valor_ventas_turno(cls): # Se resetea el valor de las ventas a cero
        cls.set_valor_variable(cls.ventas_tem_dia,0)
        cls.set_valor_variable(cls.valor_compras_tem_dia, 0)
        cls.set_valor_variable(cls.saldo_caja, 0)
        cls.set_valor_variable(cls.saldo_efectivo, 0)
        cls.set_valor_variable(cls.saldo_fiado, 0)
        cls.set_valor_variable(cls.saldo_pagado, 0)
        
class BD_Variables_Mod():
    valor = "Valor"
    id = "ID"