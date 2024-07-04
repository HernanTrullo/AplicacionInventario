import win32print
import datetime


class Printer():
    def __init__(self) -> None:
        # Obtener la impresora predeterminada
        self.impresora = win32print.GetDefaultPrinter()

        # Configurar la impresión
        self.hPrinter = win32print.OpenPrinter(self.impresora)


        # Definir la posición inicial
        self.x_pos_unit = 0
        self.x_pos_producto = 4
        self.x_pos_precio = 17
        self.x_pos_subt = 25
    
    def imprimir_linea(self):
        output_string = f"""-------------------------------\n""".encode('utf-8')
        # Enviar datos a la impresora
        win32print.WritePrinter(self.hPrinter, output_string)
        
    def imprimir_salto_de_linea(self):
        output_string = f"""\n""".encode('utf-8')
        # Enviar datos a la impresora
        win32print.WritePrinter(self.hPrinter, output_string)
        
    def imprimir_cabecera(self):
        ## Se construye la cabecera
        output_string = f"""|   Auto Servicio Pedregal    |\n""".encode('utf-8')
        # Enviar datos a la impresora
        win32print.WritePrinter(self.hPrinter, output_string)
        
        ## LA fecha
        fecha = datetime.datetime.now()
        fecha = fecha.strftime("%d/%m/%Y %H:%M:%S")
        output_string = f"""| Fecha: {fecha}  |\n""".encode('utf-8')
        # Enviar datos a la impresora
        win32print.WritePrinter(self.hPrinter, output_string)
        
        output_string = f"""|    Pedregal-Inza-Cauca      |\n""".encode('utf-8')
        # Enviar datos a la impresora
        win32print.WritePrinter(self.hPrinter, output_string)
    
    def plotear_datos(self, productos, total, codigo):
        self.hJob = win32print.StartDocPrinter(self.hPrinter, 1, ("Lista de Productos", None, "RAW"))
        win32print.StartPagePrinter(self.hPrinter)
        
        self.imprimir_linea()
        self.imprimir_cabecera()
        self.imprimir_linea()
        
        # Construir la cadena de impresión
        output_string = f"""{'Und':<{self.x_pos_producto - self.x_pos_unit}}{'Descrip':<{self.x_pos_precio-self.x_pos_producto}}{'P.unit':<{self.x_pos_subt-self.x_pos_precio}}Sub\n""".encode('utf-8')
        # Enviar datos a la impresora
        win32print.WritePrinter(self.hPrinter, output_string)
        
        for producto, precio,cant,subt in productos:
            if (len(producto)>=12):
                producto = producto[:11] + "."
                
            output_string = f"""{(str(cant)):<{self.x_pos_producto - self.x_pos_unit}}{(producto):<{self.x_pos_precio-self.x_pos_producto}}{str(precio):<{self.x_pos_subt-self.x_pos_precio}}{str(subt)}\n""".encode('utf-8')
            win32print.WritePrinter(self.hPrinter, output_string)

        self.imprimir_linea()
        output_string = f"""{'Total:':<{self.x_pos_subt - self.x_pos_unit}}{str(total)}\n""".encode('utf-8')
        win32print.WritePrinter(self.hPrinter, output_string)
        
        self.imprimir_linea()
        output_string = f"""{'Cliente:':<{self.x_pos_subt - self.x_pos_unit}}{codigo}\n""".encode('utf-8')
        win32print.WritePrinter(self.hPrinter, output_string)
        
        self.imprimir_linea()
        output_string = f"""|   Gracias por su compra!   |\n""".encode('utf-8')
        # Enviar datos a la impresora
        win32print.WritePrinter(self.hPrinter, output_string)
        
        for i in range(3):
            self.imprimir_salto_de_linea()
            
        win32print.EndDocPrinter(self.hPrinter)
        
        