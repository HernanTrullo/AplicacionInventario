from BaseDatos.VentasBD import VentasSql, VentaEstructuraSql
from BaseDatos.InventarioBD import BD_Inventario as BD, ProductoDB
import utilidades.generc as utl

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
    return resultado