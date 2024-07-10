import sqlite3
from datetime import datetime
from utilidades.excepcion import ErrorBusqueda as E

class VentaEstructuraSql:
    id = "Id"
    fecha = "Fecha"
    total_vendido = "Total_Vendido"
    total_comprado = "Total_Comprado"
    productos_vendidos = "Productos_Vendidos"
    utilidad = "Utilidad"
    
class VentaModel():
    def __init__(self,id=None, fecha=None,total_vendido=None, total_comprado=None, productos_vendidos= None):
        self.id = id
        self.fecha = fecha
        self.total_vendido = total_vendido
        self.total_comprado = total_comprado
        self.productos_vendidos = productos_vendidos
        
class VentasSql():
    name_bd = "./BaseDatos/BaseDatos.db"
    
    @classmethod
    def agregar_venta(cls, venta_objet:VentaModel):
        str = f'''
        INSERT INTO Ventas ({VentaEstructuraSql.fecha}, {VentaEstructuraSql.total_vendido}, {VentaEstructuraSql.total_comprado}, {VentaEstructuraSql.productos_vendidos})
        VALUES (?, ?, ?, ?)
        '''
        str2 = f"""
        UPDATE Ventas
        SET {VentaEstructuraSql.utilidad} = {VentaEstructuraSql.total_vendido} - {VentaEstructuraSql.total_comprado};
        """
        conn = sqlite3.connect(cls.name_bd)
        cursor = conn.cursor()
        cursor.execute(str, (venta_objet.fecha, venta_objet.total_vendido, venta_objet.total_comprado, venta_objet.productos_vendidos))
        cursor.execute(str2)
        conn.commit()
        conn.close()
        
    @classmethod
    def retornar_codigo_productos_vendidos(cls, fecha):
        str = f""" SELECT {VentaEstructuraSql.productos_vendidos} FROM Ventas
                    WHERE {VentaEstructuraSql.fecha} = '{fecha}'"""        
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        if len(res) >0:
            return [codigo[0] for codigo in res]
        else:
            raise E("Fecha no encontrada")
        
    @classmethod
    def retornar_valor_diario(cls, fecha_inicio, fecha_fin, req):
        str = f"""  SELECT {VentaEstructuraSql.fecha}, SUM({req}) as Total_V
                    FROM Ventas
                    WHERE {VentaEstructuraSql.fecha} BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
                    GROUP BY {VentaEstructuraSql.fecha}
                    ORDER BY {VentaEstructuraSql.fecha}"""        
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        if len(res) >0:
            return [item[0] for item in res],[item[1] for item in res]
        else:
            raise E("Fecha no encontrada")
    
    @classmethod
    def retornar_valor_mes(cls, fecha_inicio, fecha_fin, req):
        str = f"""  SELECT strftime('%Y-%m', {VentaEstructuraSql.fecha}) AS Mes, SUM({req}) AS Total_Mensual
                    FROM Ventas
                    WHERE {VentaEstructuraSql.fecha} BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
                    GROUP BY Mes"""
        print(str)
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        if len(res) >0:
            return [item[0] for item in res],[item[1] for item in res]
        else:
            raise E("Fecha no encontrada")
        
    @classmethod
    def retornar_valor_anio(cls, fecha_inicio, fecha_fin, req):
        str = f"""  SELECT strftime('%Y', {VentaEstructuraSql.fecha}) AS Anio, SUM({req}) AS Total_Anual
                    FROM Ventas
                    WHERE {VentaEstructuraSql.fecha} BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
                    GROUP BY Anio"""        
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        if len(res) >0:
            return [item[0] for item in res],[item[1] for item in res]
        else:
            raise E("Fecha no encontrada")
        
    @classmethod
    def retornar_productos_vendidos(cls, fecha_inicio, fecha_fin):
        str = f"""  
                    SELECT {VentaEstructuraSql.productos_vendidos}
                    FROM Ventas
                    WHERE {VentaEstructuraSql.fecha} BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
                """ 
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        res = cur.execute(str)
        res = res.fetchall()
        conn.close()
        if len(res) >0:
            return [item[0] for item in res] # Voy a retornar los productos vendidos
        else:
            raise E("Fecha no encontrada")
    