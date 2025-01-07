import tkinter as tk
from tkinter import ttk
from utilidades.excepcion import ErrorBusqueda
import TopLevels.controller as controller
import utilidades.generc as utl
from BaseDatos.control_bd_socios import BD_Socios
from utilidades.excepcion import ErrorBusqueda as ExcepBus
from tkinter import messagebox, simpledialog
from datetime import datetime
from tkcalendar import DateEntry
from utilidades.ListaVentaProducto import Producto, ListaProductoVenta
from BaseDatos.VentasBD import VentasSql, VentaEstructuraSql
from BaseDatos.InventarioBD import BD_Inventario as BD


class TopLevelWinVentasProductos:
    def __init__(self, parent):
        self.new_window1 = tk.Toplevel(parent)
        self.new_window1.title("LMH SOLUTIONS")
        self.new_window1.state("zoomed")
        
        self.frame_principal = ttk.Labelframe(self.new_window1, style="Cabecera.TFrame")
        self.frame_principal.pack(fill="both", expand=True)
        
        self.var_buscar_nombre = tk.StringVar()
        self.var_buscar_fecha = tk.StringVar()
        
        
        
        self.cabecera = ttk.Label(self.frame_principal, text="Ventas realizadas para devolución",style="CCustomLarge.TLabel")
        self.cabecera.grid(row=0, column=0)
        self.ingreso_datos = ttk.Frame(self.frame_principal, style="Cabecera.TFrame")
        self.ingreso_datos.grid(row=0, column=1,columnspan=2,sticky="nsew")
        self.frame_lista_producto = ttk.Frame(self.frame_principal)
        self.frame_lista_producto.grid(row=1, column=0,columnspan=2,sticky="nsew")
        self.frame_botones = ttk.Frame(self.frame_principal, style="Cabecera.TFrame")
        self.frame_botones.grid(row=1, column=2,sticky="nsew")
        
        self.lb_nombre_user = ttk.Label(self.ingreso_datos, text="Nombre",style="CCustomSmall.TLabel")
        self.lb_nombre_user.grid(row=0, column=0, sticky="nsew")
        self.entry_nombre = ttk.Combobox(self.ingreso_datos, textvariable=self.var_buscar_nombre)
        self.entry_nombre.grid(row=0, column=1,sticky="w")
        
        # Crear el widget DateEntry
        self.lb_nombre_user = ttk.Label(self.ingreso_datos, text="Fecha",style="CCustomSmall.TLabel")
        self.lb_nombre_user.grid(row=1, column=0, sticky="nsew")
        self.entrada_fecha = DateEntry(self.ingreso_datos,textvariable= self.var_buscar_fecha,width=10, background='#5C1499', foreground='white', borderwidth=2)
        self.entrada_fecha.grid(row=1, column=1, sticky="w")
        
        self.win_lista_producto = ListaProductoVenta(self.frame_lista_producto, self,[VentaEstructuraSql.id,Producto.codigo,Producto.nombre, Producto.precio, Producto.cantidad, VentaEstructuraSql.fecha, VentaEstructuraSql.es_cartera])
        
        self.btn_agregar = ttk.Button(self.frame_botones, text="Devolver productos", command=self.devolver_producto,style="Primary.TButton")
        self.btn_agregar.grid(row=0, column=0, sticky="nsew") 
        self.btn_agregar = ttk.Button(self.frame_botones, text="Salir", command=self.salir,style="Primary.TButton")
        self.btn_agregar.grid(row=1, column=0, sticky="nsew") 
        
        self.frame_principal.rowconfigure(0, weight=1)
        self.frame_principal.rowconfigure(1, weight=5)
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=2)
        self.frame_principal.columnconfigure(2, weight=2)
        
        self.frame_lista_producto.rowconfigure(0, weight=1)
        self.frame_lista_producto.columnconfigure(0, weight=1)
        
        self.ingreso_datos.columnconfigure(0, weight=1)
        self.ingreso_datos.columnconfigure(1, weight=4)
        self.ingreso_datos.rowconfigure(0, weight=1)
        self.ingreso_datos.rowconfigure(1, weight=1)
        
        self.frame_botones.rowconfigure(0, weight=1)
        self.frame_botones.rowconfigure(1, weight=1)
        self.frame_botones.columnconfigure(0, weight=1)
        
        self.entry_nombre.bind("<KeyRelease>", self.actualizar_nombre_usuarios)
        self.entry_nombre.bind("<Return>", self.buscar_venta)
        self.entrada_fecha.bind("<Return>", self.buscar_fecha)
        self.entrada_fecha.bind("<<CalendarSelected>>", self.buscar_fecha)
        
    def buscar_venta(self, event):
        try:
            self.win_lista_producto.vaciar_productos()
            ventas = VentasSql.retornar_idVenta_fecha_productos_es_cartera(self.var_buscar_nombre.get())
            datos_df = self.retornar_valores_producto(controller.dict_to_json(ventas))
            fechas = []
            for venta in datos_df:
                fechas.append(venta[VentaEstructuraSql.fecha][0])
            self.resaltar_fechas(fechas)
            messagebox.showinfo("LMH Solutions", 
                                "Se han encontrado registros, vaya a la fecha para seleccionar el día de interés ", 
                                parent=self.new_window1)
        
        except ExcepBus as e:
            messagebox.showinfo("LMH Solutions", 
                                f"""No se encuentran ventas registradas""",
                                parent=self.new_window1)
            self.resaltar_fechas([])
    
    def buscar_fecha(self, event):
        try:
            self.win_lista_producto.vaciar_productos()
            fecha_objeto = datetime.strptime(self.var_buscar_fecha.get(), "%d/%m/%y")
            fecha_convertida = fecha_objeto.strftime("%Y-%m-%d")
            
            ventas = VentasSql.retornar_idVenta_fecha_productos_es_cartera(self.var_buscar_nombre.get(), fecha_convertida)
            datos_df = self.retornar_valores_producto(controller.dict_to_json(ventas))
            self.win_lista_producto.agregar_producto_venta(datos_df)
        except ExcepBus as e:
            messagebox.showinfo("LMH Solutions", f"""No se encuentran ventas registradas""",
                                parent=self.new_window1)
            
    
    def agregar_venta(self):
        self.win_lista_producto.agregar_producto_venta(self.retornar_valores_producto())
    
    def limpiar_variables_busqueda(self):
        self.var_buscar_nombre.set("")
    
    def actualizar_nombre_usuarios(self, event):
        try:
            self.entry_nombre['values']=BD_Socios.retornar_nombres_socios(self.var_buscar_nombre.get())     
        except:
            self.entry_nombre['values'] = ["0"]
            
    def retornar_valores_producto(self, ventas_json):
        productos_dict  = []
        for venta in ventas_json:
            for producto in venta[VentaEstructuraSql.productos_vendidos]:
                id_venta = venta[VentaEstructuraSql.id]
                fecha_venta = venta[VentaEstructuraSql.fecha]
                es_cartera = venta[VentaEstructuraSql.es_cartera]
                codigo = producto[Producto.codigo]
                nombre = "Nombre cualquiera"
                precio = 2000
                cantidad = producto[Producto.cantidad]
                
                productos_dict.append({
                    VentaEstructuraSql.id: [id_venta],
                    VentaEstructuraSql.fecha: [fecha_venta],
                    Producto.es_cartera: [es_cartera],
                    Producto.codigo: [codigo],
                    Producto.nombre: [nombre],
                    Producto.precio: [precio],
                    Producto.cantidad: [cantidad],
                    
                })
        return productos_dict
    
    
    def resaltar_fechas(self, fechas):
        self.calendario = self.entrada_fecha._calendar
        self.calendario.calevent_remove("all")
        fechas = list(set(fechas))
        for fecha in fechas:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            self.calendario.calevent_create(fecha_obj, "Evento", "evento")
        
        # Configurar estilo para la etiqueta "evento"
        self.calendario.tag_config("evento", background='#fdef8c')
    
    def salir(self):
        resp = messagebox.askokcancel("LMH Solutions", "Está seguro que desea salir de la ventana",
                                      parent=self.new_window1)
        if resp:
            self.destroy()
            
    def devolver_producto(self):
        resp = simpledialog.askinteger("LMH Solutions", "Ingrese la cantidad a devolver",
                                        parent=self.new_window1)
        if resp:
            item = self.win_lista_producto.retornar_item_producto()
            if (resp < int(item[Producto.cantidad]) and resp >0):
                productos_vendidos = VentasSql.retornar_productos_vendidos_por_idVenta(item[VentaEstructuraSql.id])
                productos_vendidos = utl.jsonToDict(productos_vendidos)
                for producto_vendido in productos_vendidos:
                    if (producto_vendido[Producto.codigo] == item[Producto.codigo]):
                        producto_vendido[Producto.cantidad] -= resp
                        
                total_vendido, total_comprado = self.retornar_totalVendido_totalComprado(productos_vendidos)
                VentasSql.modificar_venta_por_idVenta(item[VentaEstructuraSql.id], 
                                                                    utl.dictToJson(productos_vendidos),
                                                                    total_vendido, 
                                                                    total_comprado)
                messagebox.showinfo("LMH Solutions", 
                                    "Cantidad del producto modificada con exito", 
                                    parent = self.new_window1)
                self.win_lista_producto.vaciar_productos()
                self.var_buscar_nombre.set("0")
            
            elif(resp == int(item[Producto.cantidad])):
                productos_vendidos = VentasSql.retornar_productos_vendidos_por_idVenta(item[VentaEstructuraSql.id])
                productos_vendidos = utl.jsonToDict(productos_vendidos)
                productos_vendidos = [producto for producto in productos_vendidos if producto[Producto.codigo] != item[Producto.codigo]]
                total_vendido, total_comprado = self.retornar_totalVendido_totalComprado(productos_vendidos)
                
                VentasSql.modificar_venta_por_idVenta(item[VentaEstructuraSql.id],
                                                                    utl.dictToJson(productos_vendidos),
                                                                    total_vendido, 
                                                                    total_comprado)
                
                messagebox.showinfo("LMH Solutions", 
                                    "Cantidad del producto modificada con exito",
                                    parent= self.new_window1)
                self.win_lista_producto.vaciar_productos()
                self.var_buscar_nombre.set("0")
            
            else:
                messagebox.showwarning("LMH Solutions", 
                                        "Debe ingresar un valor menor o igual a la catidad del producto, mayor de cero",
                                        parent = self.new_window1)
        
            
        else:
            messagebox.showwarning("LMH Solutions", 
                                    "Debe ingresar un valor", 
                                    parent = self.new_window1)
    
    def retornar_totalVendido_totalComprado(self, productos_vendidos):
        total_vendido = 0
        total_comprado = 0
        for producto_vendido in productos_vendidos:
            producto = BD.buscar_producto_cod(producto_vendido[Producto.codigo])
            total_vendido += producto[Producto.precio]
            total_comprado += producto[Producto.precio_entrada]
        
        return (total_vendido, total_comprado)