from PIL import ImageTk, Image
import json

def leer_imagen(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size,Image.LANCZOS))

def validar_numero(P):
    # Esta función se llama cada vez que se intenta ingresar un carácter en el Entry
    # Devuelve True si el carácter es un número o está vacío, de lo contrario, devuelve False
    #return P.isdigit() or P == ""
    if P == "":
        return True  # Permite una cadena vacía

    try:
        # Intenta convertir la cadena a un número decimal (incluyendo números negativos)
        float(P)
        return True
    except ValueError:
        return False
    
def jsonToDict(jsonValue):
    return json.loads(jsonValue)
    
def dictToJson(stringValue):
    return json.dumps(stringValue)