from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import pandas as pd
from tkinter import messagebox
import tkinter as tk
from utilidades.ListaProducto import Producto, ListaProducto
from BaseDatos.InventarioBD import BD_Inventario as BD
from BaseDatos.InventarioBD import ProductoDB
from BaseDatos.control_bd_variables import BD_Variables
from utilidades.excepcion import ErrorBusqueda as ExcepBus
from utilidades.EntryP import LabelP
import datetime
import utilidades.generc as utl
from tktooltip import ToolTip
from tkinter import simpledialog
from BaseDatos.control_bd_variables import BD_Variables as BD_Var
from utilidades.Printer import Printer
from TopLevels.WinCierreCaja import TopLevelWinCierreCaja as WinCaja
from TopLevels.WinInformeVentas import TopLevelInformeVentas as WinVentasInforme
from TopLevels.WinInformeProductos import TopLevelInformeProductos as WinProductoInforme

class WinAdmin(ttk.Frame):
    def __init__(self, root:ttk.Notebook, app):
        super().__init__(root)
        self.root = root
        
        # Variables incluidas 
        self.var_nombre_op = tk.StringVar()
        self.var_fecha = tk.StringVar()
        self.var_hora = tk.StringVar()
        
        self.var_descrip_nombre = tk.StringVar()
        self.var_descrip_cod = tk.StringVar()
        self.var_descrip_precio = tk.DoubleVar()
        self.var_descrip_precio_entra = tk.DoubleVar()
        self.var_descrip_cantidad = tk.IntVar()
        self.var_cantidad_inventario = tk.IntVar()
        
        self.var_buscar_nombre = tk.StringVar()
        self.var_buscar_cod = tk.StringVar()
        self.var_categoria = tk.StringVar()
        
        self.var_total = tk.StringVar()
        self.var_total_vendido = tk.StringVar()
        self.var_valor_ventido_op = IntVar()
        
        self.var_saldo_caja = tk.IntVar()
        self.value_ocultar =True
        
        self.foco_frame = None
        
        self.app = app
        
        self.create_widget()
        self.pack(fill="both", expand=True)
        
        
        # Inicializar variables
        self.actualizar_valor_vendido(BD_Variables.get_valor_ventas_turno())
        self.actualizar_valor_saldo_caja(int(BD_Var.get_saldo_caja()))
        
        self.bind("<FocusIn>", self.actualizar)
    
    def actualizar(self, event):
        self.actualizar_valor_vendido(BD_Variables.get_valor_ventas_turno())
        self.actualizar_valor_saldo_caja(int(BD_Var.get_saldo_caja()))
        
    def create_widget(self):
        # Frame que contiene el nombre del operario e información básica
        self.top_frame = ttk.Frame(self, style="Cabecera.TFrame")
        
        self.nameFrame = ttk.Label(self.top_frame, text="Bienvenido: ", style="CCustomLarge.TLabel")
        self.nameFrame.grid(row=0, column=0)
        self.nombre_op = ttk.Label(self.top_frame, textvariable=self.var_nombre_op, style="CCustomMedium.TLabel")
        self.nombre_op.grid(row=0, column=1)
        
        self.lb_fecha = ttk.Label(self.top_frame, text="Fecha: ", style="CCustomLarge.TLabel")
        self.lb_fecha.grid(row=1,column=0)
        self.fecha = ttk.Label(self.top_frame, textvariable=self.var_fecha,style="CCustomSmall.TLabel")
        self.fecha.grid(row=1, column=1)
        
        self.lb_hora = ttk.Label(self.top_frame, text="Hora: ", style="CCustomLarge.TLabel")
        self.lb_hora.grid(row=2, column=0)
        self.hora = ttk.Label(self.top_frame, textvariable=self.var_hora, style="CCustomSmall.TLabel")
        self.hora.grid(row=2, column=1)
        
        self.lb_saldo_caja = ttk.Label(self.top_frame, text="Saldo Caja ", style="CCustomLarge.TLabel")
        self.lb_saldo_caja.grid(row=2, column=2)
        self.saldo_caja = LabelP(self.top_frame, textvariable=self.var_saldo_caja, style="CCustomLarge.TLabel")
        self.saldo_caja.grid(row=2, column=3)
        
        self.lb_valor_vendido_op =  ttk.Label(self.top_frame, text="Valor Vendido: ", style="CCustomMedium.TLabel")
        self.lb_valor_vendido_op.grid(row=0, column=2, padx=10)
        self.valor_vendido_op = LabelP(self.top_frame, textvariable=self.var_valor_ventido_op, style="CCustomMedium.TLabel")
        self.valor_vendido_op.grid(row=0, column=3, padx=10)
        # Asociar el evento de clic al Label
        self.lb_valor_vendido_op.bind("<Button-1>", lambda event: self.toggle_visibility())
        self.top_frame.grid(row=0,column=0, sticky="nsew")
        
        
        # Cabecera de la cuenta
        self.frame_top_cuenta = ttk.Frame(self, style="Cabecera.TFrame")
        self.lb_cuenta = ttk.Label(self.frame_top_cuenta, text="Total_PV", style="CCustomMedium.TLabel")
        self.lb_cuenta.grid(row=0, column=0, padx=10)
        self.out_total_vendido = LabelP(self.frame_top_cuenta, textvariable=self.var_total_vendido ,style="CCustomMedium.TLabel") # La salida del total
        self.out_total_vendido.grid(row=0,column=1,padx=10)
        
        
        self.lb_total = ttk.Label(self.frame_top_cuenta, text="Total_PC", style="CCustomMedium.TLabel")
        self.lb_total.grid(row=1, column=0, padx=10)
        self.out_total = LabelP(self.frame_top_cuenta, textvariable=self.var_total ,style="CCustomMedium.TLabel") # La salida del total
        self.out_total.grid(row=1,column=1,padx=10)
        
        
        self.frame_top_cuenta.grid(row=0, column=1,sticky="nsew", rowspan=3)
        self.expandir_widget(self.frame_top_cuenta)
        
        # Bóton para cargar los datos al inventario, salir y log out y cambio de clave
        self.frame_inventario = ttk.Notebook(self)
        self.frame1_usuario = ttk.Frame(self.frame_inventario)
        self.frame2_operaciones = ttk.Frame(self.frame_inventario)
        self.frame3_caja = ttk.Frame(self.frame_inventario)
        self.frame4_ventas_inventario = ttk.Frame(self.frame_inventario)
        
        self.frame_inventario.add(self.frame2_operaciones, text="Operaciones")
        self.frame_inventario.add(self.frame1_usuario, text="Usuario")
        self.frame_inventario.add(self.frame3_caja, text= "Caja")
        self.frame_inventario.add(self.frame4_ventas_inventario, text="Ventas e Inventario")
        
        self.btn_cargar_inventario = ttk.Button(self.frame2_operaciones, text="Cargar al inventario", command=self.cargar_inventario,style="Primary.TButton")
        self.btn_cargar_inventario.grid(row=0,column=0,sticky="nsew")
        self.btn_devolver_producto = ttk.Button(self.frame2_operaciones, text="Devolver Producto", command=self.devolver_valor_vendido, style="Primary.TButton")
        self.btn_devolver_producto.grid(row=1, column=0,sticky="nsew")
        
        self.btn_cierre_caja  = ttk.Button(self.frame3_caja, text="Informe de Caja",command=self.cierre_de_caja_infome, style="Primary.TButton")
        self.btn_cierre_caja.grid(row=0, column=0,sticky="nsew")
        self.btn_asignar_saldo_caja = ttk.Button(self.frame3_caja, text="Asignar Saldo Caja", command=self.asignar_saldo_caja, style="Primary.TButton")
        self.btn_asignar_saldo_caja.grid(row=1, column=0, sticky="nsew")
        
        self.btn_salir  = ttk.Button(self.frame1_usuario, text="Salir",command=self.salir, style="Primary.TButton")
        self.btn_salir.grid(row=0, column=0,sticky="nsew")
        self.btn_cambiar_clave  = ttk.Button(self.frame1_usuario, text="Cambiar Clave",command=self.cambiar_clave, style="Primary.TButton")
        self.btn_cambiar_clave.grid(row=1, column=0,sticky="nsew")
        
        self.btn_informe_ventas = ttk.Button(self.frame4_ventas_inventario, text="Informe Ventas",command=self.generar_informe_ventas, style="Primary.TButton")
        self.btn_informe_ventas.grid(row=0, column=0, sticky="nsew")
        self.btn_informe_inventario = ttk.Button(self.frame4_ventas_inventario, text="Informe Inventario",command=self.generar_informe_inventario, style="Primary.TButton")
        self.btn_informe_inventario.grid(row=1, column=0, sticky="nsew")
        
        
        self.expandir_widget(self.frame_inventario, row=0, colum=0)
        self.expandir_widget(self.frame1_usuario, row=2, colum=1)
        self.expandir_widget(self.frame2_operaciones, row=2, colum=1)
        self.expandir_widget(self.frame3_caja, row=2, colum=1)
        self.expandir_widget(self.frame4_ventas_inventario, row=2, colum=1)
        
        self.frame_inventario.grid(row=3, column=1, rowspan=2,columnspan=2, sticky="nsew")
        
        
        # Frame del buscar de datos
        self.ingreso_datos = ttk.Frame(self)
        
        self.lb_codigo = ttk.Label(self.ingreso_datos, text="Código", style="CustomSmall.TLabel")
        self.lb_codigo.grid(row=0, column=0)
        self.entry_codigo = ttk.Entry(self.ingreso_datos, textvariable=self.var_buscar_cod,style="Custom.TEntry")
        self.entry_codigo.grid(row=1, column=0,sticky="nsew")
        
        self.lb_nombre_producto = ttk.Label(self.ingreso_datos, text="Nombre",style="CustomSmall.TLabel")
        self.lb_nombre_producto.grid(row=0, column=1)
        self.entry_nombre_producto = ttk.Combobox(self.ingreso_datos, textvariable=self.var_buscar_nombre)
        self.entry_nombre_producto.grid(row=1, column=1,sticky="nsew")
        self.entry_nombre_producto.bind("<KeyRelease>", self.actualizar_nombre_productos)
        
        self.lb_categoria = ttk.Label(self.ingreso_datos, text="Categoria",style="CustomSmall.TLabel")
        self.lb_categoria.grid(row=0, column=2)
        self.entry_categoria= ttk.Combobox(self.ingreso_datos, textvariable=self.var_categoria)
        self.entry_categoria.grid(row=1, column=2,sticky="nsew")
        
        self.entry_categoria["values"] = ["Tienda", "Almacen"]
        
        self.expandir_widget(self.ingreso_datos, colum=3, row=3)
        self.ingreso_datos.grid(row=1, column=0,sticky="nsew",pady=20)
        
        # Frame descripción del producto (Compra)
        self.frame_descrip_producto = ttk.Frame(self)
        
        self.lb_cod_descrp_producto = ttk.Label(self.frame_descrip_producto, text="Código", style="CustomSmall.TLabel")
        self.lb_cod_descrp_producto.grid(row=0, column=0,sticky="nsew")
        self.entry_cod_descrp_producto = ttk.Entry(self.frame_descrip_producto, textvariable=self.var_descrip_cod)
        self.entry_cod_descrp_producto.grid(row=1, column=0,sticky="nsew")
        
        self.lb_nombre_descrp_producto = ttk.Label(self.frame_descrip_producto, text="Nombre",style="CustomSmall.TLabel")
        self.lb_nombre_descrp_producto.grid(row=0, column=1,sticky="nsew")
        self.entry_nombre_descrp_producto = ttk.Entry(self.frame_descrip_producto, textvariable=self.var_descrip_nombre)
        self.entry_nombre_descrp_producto.grid(row=1, column=1,sticky="nsew") # Entry
        
        vc = (self.register(utl.validar_numero), "%P")
        self.lb_precio_decrip_producto = ttk.Label(self.frame_descrip_producto, text="Precio",style="CustomSmall.TLabel")
        self.lb_precio_decrip_producto.grid(row=0,column=2,sticky="nsew")
        self.entry_precio_decrip_producto = ttk.Entry(self.frame_descrip_producto, textvariable=self.var_descrip_precio, validate="key", validatecommand=vc)
        self.entry_precio_decrip_producto.grid(row=1,column=2,sticky="nsew")
        
        self.lb_precioe_decrip_producto = ttk.Label(self.frame_descrip_producto, text="Precio Entrada",style="CustomSmall.TLabel")
        self.lb_precioe_decrip_producto.grid(row=0,column=3,sticky="nsew")
        self.entry_precioe_decrip_producto = ttk.Entry(self.frame_descrip_producto, textvariable=self.var_descrip_precio_entra, validate="key", validatecommand=vc)
        self.entry_precioe_decrip_producto.grid(row=1,column=3,sticky="nsew")
        
        
        self.lb_cantidad_decrip_producto = ttk.Label(self.frame_descrip_producto, text="Cantidad",style="CustomSmall.TLabel", width=20)
        self.lb_cantidad_decrip_producto.grid(row=0,column=4,sticky="nsew")
        self.entry_cantidad_decrip_producto = ttk.Entry(self.frame_descrip_producto, textvariable=self.var_descrip_cantidad,width=20, validate="key", validatecommand=vc)
        self.entry_cantidad_decrip_producto.grid(row=1,column=4,sticky="nsew")
        
        self.lb_cantidad_inventario = ttk.Label(self.frame_descrip_producto, text="Cant. Inventario",style="CustomSmall.TLabel", width=20).grid(row=0,column=5,sticky="nsew")
        self.cantidad_inventario = ttk.Label(self.frame_descrip_producto, textvariable=self.var_cantidad_inventario, width=20)
        self.cantidad_inventario.grid(row=1,column=5,sticky="nsew")
        
        self.cambiar_widget()
        self.frame_descrip_producto.grid(row=2, column=0,sticky="nsew")
        self.expandir_widget(self.frame_descrip_producto, colum=5)
        
        # Frame lista de productos
        self.frame_lista_producto = ttk.Frame(self)
        self.win_lista_producto = ListaProducto(self.frame_lista_producto, self,[Producto.codigo,Producto.nombre, Producto.precio, Producto.precio_entrada,Producto.cantidad])
        self.frame_lista_producto.grid(row=4, column=0, sticky="nsew")
        self.win_lista_producto.bind("<BackSpace>", self.eliminar_producto_auto)
        
        # Frame Botones
        self.frame_botones = ttk.Frame(self)
        self.img_mod = utl.leer_imagen("./Imagenes/BTN_Modificar.png", (24,24))
        self.img_add = utl.leer_imagen("./Imagenes/BTN_Agregar.png", (24,24))
        self.img_per = utl.leer_imagen("./Imagenes/BTN_Percent.png", (24,24))
        
        self.btn_agregar = ttk.Button(self.frame_botones, image=self.img_add, style="Primary.TButton",command=self.agregar_producto)
        self.btn_agregar.grid(row=0, column=3, pady=10)  
        self.btn_modificar = ttk.Button(self.frame_botones, image=self.img_mod,style="Primary.TButton" ,command=self.modificar_producto)
        self.btn_modificar.grid(row=0, column=2)
        self.btn_view_percent = ttk.Button(self.frame_botones, text="%",style="Primary.TButton", image=self.img_per)
        self.btn_view_percent.grid(row=0, column=1)
        
        # Se configuran los tooltip
        ToolTip(self.btn_agregar, "Agregar Producto", delay=0.5)
        ToolTip(self.btn_modificar, "Modificar Producto", delay=0.5)
        ToolTip(self.btn_view_percent, self.mesaje, delay=0.5)
        
        self.frame_botones.columnconfigure(0, weight= 7)
        self.frame_botones.columnconfigure(4, weight= 1)
        
        
        self.frame_botones.grid(row=3, column=0, sticky="nsew")
        
        ## Configurar el frame principal del operario
        self.rowconfigure(4, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(0, weight=0)
        
        # guardar foco del frame
        self.entry_codigo.bind("<FocusIn>", self.controlador_de_foco)
        self.entry_nombre_producto.bind("<FocusIn>", self.controlador_de_foco)
        
        # Agregar producto automaticamente 
        self.entry_codigo.bind("<Return>", self.agregar_automaticamente)
        self.entry_nombre_producto.bind("<Return>", self.agregar_automaticamente)
        
        # Agregar fecha y hora
        self.var_fecha.set(datetime.date.today().strftime('%d/%m/%Y'))
        self.actualizar_hora()
        
        # Comprobar nombre o codigo
        self.entry_cod_descrp_producto.bind("<FocusOut>",self.comprobar_codigo_producto)
        self.entry_nombre_descrp_producto.bind("<FocusOut>",self.comprobar_nombre_producto)
        
        
    
    def toggle_visibility(self):
        if self.value_ocultar:
            self.valor_vendido_op.grid_forget()
            self.value_ocultar = False
        else:
            self.valor_vendido_op.grid(row=0, column=3, padx=10)
            self.value_ocultar = True
    
    def devolver_valor_vendido(self):
        resp = messagebox.askokcancel("LMH SOLUTIONS", "¿Está seguro que desea devolver el valor vendido?")
        if (resp):
            valor_resto = simpledialog.askinteger("LMH SOLUTIONS", "Ingrese el valor a devolver")
            value_actualizado = self.var_valor_ventido_op.get() - valor_resto
            value_actualizado_r = "${:,.2f}".format(value_actualizado)
            resp = messagebox.askokcancel("LMH SOLUTIONS", f"El valor actualizado es: {value_actualizado_r}")
            if (resp):
                BD_Var.set_valor_ventas_turno(str(value_actualizado))
                self.actualizar_valor_vendido(value_actualizado)
                messagebox.showinfo("LMH SOLUTIONS", "Operación Exitosa!")

    def mesaje (self):
        num = 0
        try:
            num = (self.var_descrip_precio.get()-self.var_descrip_precio_entra.get())*(100/self.var_descrip_precio_entra.get())
        except:
            pass
        
        text = str(int(num)) + " %"
        
        return text
    
    def actualizar_nombre_productos(self, event):
        try:
            self.entry_nombre_producto['values']=BD.retornar_nombres_productos(self.var_buscar_nombre.get())     
        except:
            self.entry_nombre_producto['values'] = [""]
    
    def actualizar_hora(self):
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        self.var_hora.set(hora_actual)
        self.after_id = self.after(1000, self.actualizar_hora)
        
    def comprobar_nombre_producto(self, event):
        if (BD.esta_el_producto_nombre(self.var_descrip_nombre.get())):
            messagebox.showwarning("LMH SOLUTIONS", "Nombre Duplicado")
            event.widget.focus()
    
    def comprobar_codigo_producto(self, event):
        if (BD.esta_el_producto_cod(self.var_descrip_cod.get())):
            messagebox.showwarning("LMH SOLUTIONS", "Código Duplicado")
            event.widget.focus()
        
    def salir(self):
        self.app.on_close()
    
    def cambiar_clave(self):
        clave_nueva = simpledialog.askstring("LMH SOLUTIONS", "Digite una clave de admin nueva")
        clave_antigua = f"{BD_Variables.get_clave_admin()}"
        respuesta = messagebox.askokcancel("LMH SOLUTIONS", f"""La clave antigua es: {clave_antigua}, la nueva es: {clave_nueva} \n¿Está seguro(a) que va a cambiarla?""")
        
        if (respuesta):
            messagebox.showinfo("LMH SOLUTIONS", "Clave cambiada correctamente")
            BD_Variables.set_clave_admin(clave_nueva)
            notebok_tabs= self.root.tabs()
            self.root.tab(notebok_tabs[5], state="hidden")
            self.root.tab(notebok_tabs[4], state="hidden")
            self.root.tab(notebok_tabs[2], state="hidden")
            self.root.tab(notebok_tabs[1], state="hidden")
            self.root.tab(notebok_tabs[0], state="normal")
            self.root.select(notebok_tabs[0])
            
            
    def asignar_saldo_caja(self):
        resp = messagebox.askokcancel("LMH SOLUTIONS", "Va a asignar un saldo de caja,\n¿está seguro que desea hacerlo?")
        if resp:
            resp = simpledialog.askinteger("LMH SOLUTIONS", "Digite el saldo en caja con el que va a iniciar")
            if resp:
                self.actualizar_valor_saldo_caja(resp)
                
                BD_Var.set_saldo_caja(self.var_saldo_caja.get())
                messagebox.showinfo("LMH SOLUTIONS", "Saldo añadido correctamente")
                

    def cierre_de_caja_infome(self):
        self.win_caja = WinCaja(self, BD_Var.get_saldo_caja(), BD_Var.get_valor_ventas_turno())
    
    def actualizar_valor_vendido (self, value):
        self.var_valor_ventido_op.set(value)
        self.valor_vendido_op.formatear_valor()
    
    def controlador_de_foco(self, event):
        self.foco_frame = event.widget
    
    def eliminar_producto_auto(self, event):
        self.eliminar_producto()
        
    def agregar_automaticamente(self, event):
        self.buscar_producto()
        
    def buscar_producto(self):
        if self.foco_frame == self.entry_codigo or self.foco_frame == self.entry_nombre_producto:
            try:
                if self.foco_frame == self.entry_codigo:
                    producto = BD.buscar_producto_cod(self.var_buscar_cod.get())   
                    self.var_descrip_cod.set(producto[ProductoDB.codigo])
                    self.var_descrip_nombre.set(producto[ProductoDB.nombre])
                    self.var_descrip_precio.set(producto[ProductoDB.precio])
                    self.var_descrip_precio_entra.set(producto[ProductoDB.precio_entrada])
                    self.var_descrip_cantidad.set(1)
                    self.var_cantidad_inventario.set(producto[ProductoDB.cantidad])
                    
                elif self.foco_frame == self.entry_nombre_producto:
                    producto = BD.buscar_producto_nombre(self.var_buscar_nombre.get())
                    self.var_descrip_cod.set(producto[ProductoDB.codigo])
                    self.var_descrip_nombre.set(producto[ProductoDB.nombre])
                    self.var_descrip_precio.set(producto[ProductoDB.precio])
                    self.var_descrip_precio_entra.set(producto[ProductoDB.precio_entrada])
                    self.var_descrip_cantidad.set(1)
                    self.var_cantidad_inventario.set(producto[ProductoDB.cantidad])
                        
            except  ExcepBus as e:  
                respuesta=messagebox.askokcancel("LMH SOLUTIONS", "Codigo o Nombre no encontrado. ¿Desea agregar uno?")
                if respuesta:
                    if self.foco_frame == self.entry_codigo:
                        self.cambiar_widget(2)
                        self.limpiar_variables()
                        self.var_descrip_cod.set(self.var_buscar_cod.get())
                    elif self.foco_frame == self.entry_nombre_producto:
                        self.cambiar_widget(1)
                        self.limpiar_variables()
                        self.var_descrip_nombre.set(self.var_buscar_nombre.get())
                        
            self.var_buscar_cod.set("")
            self.var_buscar_nombre.set("")
            
        
    def cargar_inventario(self):
        resp = messagebox.askokcancel("LMH SOLUTIONS", "¿Está seguro que desea agregar los productos al inventario?")
        if resp:
            try:
                BD.cargar_inventario(self.win_lista_producto.retornar_productos())
                
                self.win_lista_producto.vaciar_productos()
                self.var_total.set(0)
                self.out_total.formatear_valor()
                
                self.var_total_vendido.set(0)
                self.out_total_vendido.formatear_valor()
                messagebox.showinfo("LMH SOLUTIONS", "Productos agregados correctamente")
            except:
                messagebox.showerror("LMH SOLUTIONS", """Algo inesperado a ocurrido con la base de datos
                                    por favor comunicarse con el soporte técnico""")
                
        self.entry_codigo.focus()
            
            
    def agregar_producto(self):
        # Se verifica si el código ya está en la base de datos
        if self.var_descrip_precio.get() > self.var_descrip_precio_entra.get():
            self.win_lista_producto.agregar_producto(self.retornar_valores_producto())
            self.limpiar_variables()
            self.cambiar_widget()
            self.actualizar_precio_total()
            self.entry_codigo.focus()
        else:
            messagebox.showwarning("LMH SOLUTIONS", "El precio de venta es menor que el de compra")
        
        
    def eliminar_producto(self):
        self.win_lista_producto.eliminar_producto()
        self.cambiar_widget()
        self.limpiar_variables()
        self.actualizar_precio_total()
        self.entry_codigo.focus()

    def modificar_producto(self):
        if self.var_descrip_precio.get() > self.var_descrip_precio_entra.get():
            res = messagebox.askokcancel("LMH SOLUTIONS", "Está seguro de que desea modificar los parámetros del producto?")
            if res:
                self.win_lista_producto.modificar_producto(self.retornar_valores_producto())
                self.cambiar_widget()
                self.limpiar_variables()
                messagebox.showinfo("LMH SOLUTIONS", "Producto modificado correctamente")
                self.bloquear_botones(False)
                self.actualizar_precio_total()
                self.entry_codigo.focus()
        else:
            messagebox.showwarning("LMH SOLUTIONS", "El precio de venta es menor que el de compra")
    
    ## La disposición del inventario y las ventas
    def generar_informe_ventas(self):
        self.winVentasInforme = WinVentasInforme(self)
    
    def generar_informe_inventario(self):
        self.winProductoInforme = WinProductoInforme(self)
    
    def expandir_widget(self, frame:ttk.LabelFrame, row=2, colum=2):
        for i in range(row):
            frame.rowconfigure(i, weight=1)
        for i in range(colum):
            frame.columnconfigure(i, weight=1)
            
    def cambiar_widget(self, comand=0):
        if comand==0:
            self.entry_nombre_descrp_producto.config(state="disabled")
            self.entry_precio_decrip_producto.config(state="disabled")
            self.entry_precioe_decrip_producto.config(state="disabled")
            self.entry_cantidad_decrip_producto.config(state="normal")
            self.entry_cod_descrp_producto.config(state="disabled")
        elif comand==1:
            self.entry_nombre_descrp_producto.config(state="normal")
            self.entry_precio_decrip_producto.config(state="normal")
            self.entry_precioe_decrip_producto.config(state="normal")
            self.entry_cantidad_decrip_producto.config(state="normal")
            self.entry_cod_descrp_producto.config(state="normal")
        elif comand ==2:
            self.entry_nombre_descrp_producto.config(state="normal")
            self.entry_precio_decrip_producto.config(state="normal")
            self.entry_precioe_decrip_producto.config(state="normal")
            self.entry_cantidad_decrip_producto.config(state="normal")
            self.entry_cod_descrp_producto.config(state="disabled")
        elif comand ==3:
            self.entry_nombre_descrp_producto.config(state="disable")
            self.entry_precio_decrip_producto.config(state="normal")
            self.entry_precioe_decrip_producto.config(state="normal")
            self.entry_cantidad_decrip_producto.config(state="normal")
            self.entry_cod_descrp_producto.config(state="disabled")
        
    def bloquear_botones(self, comand=True):
        if comand:
            self.btn_agregar.config(state="disabled")
            self.btn_cargar_inventario.config(state="disabled")
        else:
            self.btn_agregar.config(state="normal")
            self.btn_cargar_inventario.config(state="normal")
            
    def limpiar_variables(self):
        self.var_descrip_nombre.set("")
        self.var_descrip_cod.set("")
        self.var_descrip_precio.set(0)
        self.var_descrip_precio_entra.set(0)
        self.var_descrip_cantidad.set(0)
        self.var_cantidad_inventario.set(0)
        
    def doble_click_producto_modificar(self, valores):
        self.cambiar_widget(3)
        self.bloquear_botones()
        
        self.var_descrip_nombre.set(valores[1])
        self.var_descrip_cod.set(valores[0])
        self.var_descrip_precio.set(valores[2])
        self.var_descrip_precio_entra.set(valores[3])
        self.var_descrip_cantidad.set(valores[4]) 
        
    def retornar_valores_producto(self):
        return {
            Producto.codigo: [self.var_descrip_cod.get()],
            Producto.nombre: [self.var_descrip_nombre.get().title()],
            Producto.precio: [self.var_descrip_precio.get()],
            Producto.precio_entrada: [self.var_descrip_precio_entra.get()],
            Producto.cantidad: [self.var_descrip_cantidad.get()]
        }
    
    # Se actualiza el precio total de entrada y salida que hay en los produstos del list
    def actualizar_precio_total(self):
        self.var_total.set(self.win_lista_producto.calcular_precio_productos_entrada())
        self.var_total_vendido.set(self.win_lista_producto.calcular_precio_productos_vendido())
        self.out_total.formatear_valor() # Formato de peso
        self.out_total_vendido.formatear_valor() # Formato de peso
        
    def actualizar_valor_saldo_caja(self, value):
        self.var_saldo_caja.set(value)
        self.saldo_caja.formatear_valor()
