# Definir una clase de excepción personalizada
class ErrorBusqueda(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)