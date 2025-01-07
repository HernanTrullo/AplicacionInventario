from BaseDatos.VentasBD import VentasSql, VentaEstructuraSql
from BaseDatos.InventarioBD import BD_Inventario as BD, ProductoDB
import utilidades.generc as utl
import json

def obtener_dict_codigo_cantidad(codigos_json):
    lista_codigos_multiples = []
    for codigo in codigos_json:
        lista_codigos_multiples.append(utl.jsonToDict(codigo))
    
    resultado = {}
    for sublista in lista_codigos_multiples:
        for item in sublista:
            codigo = item[ProductoDB.codigo]
            cantidad = item[ProductoDB.cantidad]
            if codigo in resultado:
                resultado[codigo] += cantidad
            else:
                resultado[codigo] = cantidad
        
        resultado = dict(sorted(resultado.items(), key=lambda item: item[1], reverse=True))
        
        print(resultado)
    return resultado

def dict_to_json(datos):
    # Organizar los datos en formato JSON
    resultados_json = []
    for id_venta, fecha, productos_str, es_cartera in datos:
        productos = json.loads(productos_str)
        resultados_json.append({
            VentaEstructuraSql.id: id_venta,
            VentaEstructuraSql.fecha: fecha,
            VentaEstructuraSql.productos_vendidos: productos,
            VentaEstructuraSql.es_cartera: "Fiado" if es_cartera else "Cancelado"
        })

    # Convertir a JSON completo
    return resultados_json