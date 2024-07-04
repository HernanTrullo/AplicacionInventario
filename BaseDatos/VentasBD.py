import sqlite3
from datetime import datetime

class VentaEstructuraSql:
    id = "Id"
    fecha = "Fecha"
    total_vendido = "Total_Vendido"
    total_comprado = "Total_Comprado"
    
class VentaModel():
    def __init__(self,id=None, fecha=None,total_vendido=None, total_comprado=None):
        self.id = id
        self.fecha = fecha
        self.total_vendido = total_vendido
        self.total_comprado = total_comprado
        
class VentasSql():
    name_bd = "./BaseDatos/BaseDatos.db"
    
    @classmethod
    def agregar_venta(cls, venta_objet:VentaModel):
        str = f'''
        INSERT INTO Ventas ({VentaEstructuraSql.fecha}, {VentaEstructuraSql.total_vendido}, {VentaEstructuraSql.total_comprado})
        VALUES (?, ?, ?)
        '''
        
        conn = sqlite3.connect(cls.name_bd)
        cursor = conn.cursor()
        cursor.execute(str, (venta_objet.fecha, venta_objet.total_vendido, venta_objet.total_comprado))
        conn.commit()
        conn.close()
    
    
    