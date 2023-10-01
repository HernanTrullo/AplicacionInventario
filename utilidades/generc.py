from PIL import ImageTk, Image

def leer_imagen(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size,Image.ANTIALIAS))

def validar_numero(P):
    # Esta función se llama cada vez que se intenta ingresar un carácter en el Entry
    # Devuelve True si el carácter es un número o está vacío, de lo contrario, devuelve False
    return P.isdigit() or P == ""