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
    id_cliente = "Id_cliente"
    es_cartera = "Es_cartera"
    
class VentaModel():
    def __init__(self,id=None, fecha=None,total_vendido=None, total_comprado=None, productos_vendidos= None, id_cliente="0", es_cartera=0):
        self.id = id
        self.fecha = fecha
        self.total_vendido = total_vendido
        self.total_comprado = total_comprado
        self.productos_vendidos = productos_vendidos
        self.id_cliente = id_cliente
        self.es_cartera = es_cartera
        
class VentasSql():
    name_bd = "./BaseDatos/BaseDatos.db"
    
    @classmethod
    def agregar_venta(cls, venta_objet:VentaModel):
        str = f'''
        INSERT INTO Ventas ({VentaEstructuraSql.fecha}, {VentaEstructuraSql.total_vendido}, {VentaEstructuraSql.total_comprado}, {VentaEstructuraSql.productos_vendidos}, {VentaEstructuraSql.id_cliente}, {VentaEstructuraSql.es_cartera})
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        str2 = f"""
        UPDATE Ventas
        SET {VentaEstructuraSql.utilidad} = {VentaEstructuraSql.total_vendido} - {VentaEstructuraSql.total_comprado};
        """
        conn = sqlite3.connect(cls.name_bd)
        cursor = conn.cursor()
        cursor.execute(str, (venta_objet.fecha, venta_objet.total_vendido, venta_objet.total_comprado, venta_objet.productos_vendidos, venta_objet.id_cliente, venta_objet.es_cartera))
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
        
    @classmethod
    def retornar_idVenta_fecha_productos_es_cartera(cls,id_cliente, fecha= None):
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        if fecha:
        # Consulta SQL
            str = f"""
                SELECT {VentaEstructuraSql.id}, {VentaEstructuraSql.fecha}, {VentaEstructuraSql.productos_vendidos}, {VentaEstructuraSql.es_cartera}
                FROM Ventas
                WHERE {VentaEstructuraSql.id_cliente} = ? AND {VentaEstructuraSql.fecha} = ?
            """
            res = cur.execute(str, (id_cliente,fecha,))
        else:
            str = f"""
                SELECT {VentaEstructuraSql.id}, {VentaEstructuraSql.fecha}, {VentaEstructuraSql.productos_vendidos}, {VentaEstructuraSql.es_cartera}
                FROM Ventas
                WHERE {VentaEstructuraSql.id_cliente} = ?
            """
            res = cur.execute(str, (id_cliente,))
        
        res = res.fetchall()
        conn.close()
        
        if len(res) >0:
            return res
        else:
            raise E("Ventas no encontradas")
        
    @classmethod
    def modificar_venta_por_idVenta(cls, id_venta, productos_vendidos, total_vendido, total_comprado):
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        
        str = f"""  UPDATE Ventas
                    SET {VentaEstructuraSql.productos_vendidos} = ?, {VentaEstructuraSql.total_vendido}=?, {VentaEstructuraSql.total_comprado}=?
                    WHERE {VentaEstructuraSql.id} = ?"""
        
        str2 = f"""
                    UPDATE Ventas
                    SET {VentaEstructuraSql.utilidad} = {VentaEstructuraSql.total_vendido} - {VentaEstructuraSql.total_comprado};
        """
        
        cur.execute(str, (productos_vendidos, total_vendido, total_comprado, id_venta))
        cur.execute(str2)
        conn.commit()
        conn.close()
        
    @classmethod
    def retornar_productos_vendidos_por_idVenta(cls, id_venta):
        conn = sqlite3.connect(cls.name_bd)
        cur = conn.cursor()
        
        str = f"""  SELECT {VentaEstructuraSql.productos_vendidos} FROM Ventas
                    WHERE {VentaEstructuraSql.id} = ?"""
        
        res = cur.execute(str, (id_venta,))
        res = res.fetchall()
        conn.close()
        
        if len(res) >0:
            return res[0][0]
        else:
            raise E("Ventas no encontradas")
        
    
    