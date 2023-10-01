from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import pandas as pd
from tkinter import messagebox
import tkinter as tk
from utilidades.ListaProducto import Producto, ListaProducto
from BaseDatos.InventarioBD import BD_Inventario as BD
from utilidades.excepcion import ErrorBusqueda as ExcepBus
from utilidades.EntryP import LabelP
from tkinter import simpledialog
import utilidades.generc as utl
   
    
class WinOperario(ttk.Frame):
    def __init__(self, root:ttk.Notebook, app):
        super().__init__(root)
        self.root = root
        self.app = app
        # Variables incluidas 
        self.var_nombre_op = tk.StringVar()
        self.var_fecha = tk.StringVar()
        self.var_hora = tk.StringVar()
        
        self.var_descrip_nombre = tk.StringVar()
        self.var_descrip_cod = tk.StringVar()
        self.var_descrip_precio = tk.IntVar()
        self.var_descrip_cantidad = tk.IntVar()
        
        self.var_buscar_nombre = tk.StringVar()
        self.var_buscar_cod = tk.StringVar()
        
        self.var_total = tk.IntVar()
        
        self.var_aporte_cliente = IntVar()
        self.var_saldo_cliente = IntVar()
        
        
        
        self.foco_frame = None
        
        self.create_widget()
        self.pack(fill="both", expand=True)
        
        
    def create_widget(self):
        # Frame que contiene el nombre del operario e información básica
        self.top_frame = ttk.LabelFrame(self)
        
        self.nameFrame = ttk.Label(self.top_frame, text="Operario: ", style="Custom.TLabel")
        self.nameFrame.grid(row=0, column=0)
        self.nombre_op = ttk.Label(self.top_frame, textvariable=self.var_nombre_op, style="Custom.TLabel")
        self.nombre_op.grid(row=0, column=1)
        
        self.lb_fecha = ttk.Label(self.top_frame, text="Fecha: ", style="Custom.TLabel")
        self.lb_fecha.grid(row=1,column=0)
        self.fecha = ttk.Label(self.top_frame, textvariable=self.var_fecha)
        self.fecha.grid(row=1, column=1)
        
        self.lb_hora = ttk.Label(self.top_frame, text="Hora: ", style="Custom.TLabel")
        self.lb_hora.grid(row=2, column=0)
        self.hora = ttk.Label(self.top_frame, textvariable=self.var_hora)
        self.hora.grid(row=2, column=1)
        
        self.top_frame.grid(row=0,column=0, sticky="nsew")
        
        # Cabecera de la cuenta
        self.frame_top_cuenta = ttk.LabelFrame(self)
        self.lb_cuenta = Label(self.frame_top_cuenta, text="Cuenta Cliente", style="Custom.TLabel")
        self.lb_cuenta.grid(row=0, column=0, padx=10, pady=15,columnspan=2)
        
        self.lb_total = ttk.Label(self.frame_top_cuenta, text="Total", style="Custom.TLabel")
        self.lb_total.grid(row=1, column=0, padx=10)
        
        self.out_total = LabelP(self.frame_top_cuenta, textvariable=self.var_total ,style="Custom.TLabel") # La salida del total
        self.out_total.grid(row=1,column=1,padx=10)
        
        
        self.frame_top_cuenta.grid(row=0, column=1, rowspan=2,sticky="nsew")
        self.expandir_widget(self.frame_top_cuenta)
        
        # Frame del buscar de datos
        self.ingreso_datos = ttk.LabelFrame(self)
        
        self.lb_codigo = ttk.Label(self.ingreso_datos, text="Código")
        self.lb_codigo.grid(row=0, column=0)
        self.entry_codigo = ttk.Entry(self.ingreso_datos, textvariable=self.var_buscar_cod)
        self.entry_codigo.grid(row=1, column=0,sticky="nsew")
        
        self.lb_nombre_producto = ttk.Label(self.ingreso_datos, text="Nombre")
        self.lb_nombre_producto.grid(row=0, column=1)
        self.entry_nombre_producto = ttk.Entry(self.ingreso_datos, textvariable=self.var_buscar_nombre)
        self.entry_nombre_producto.grid(row=1, column=1,sticky="nsew")
        
        self.btn_buscar = ttk.Button(self.ingreso_datos, text="Buscar", command=self.buscar_producto, width=40)
        self.btn_buscar.grid(row=1, column=2, sticky="nsew")
        
        self.expandir_widget(self.ingreso_datos, row=3)
        self.ingreso_datos.grid(row=1, column=0,sticky="nsew")
        
        # Frame botones de cálculo de cuenta y logeo-salir
        self.frame_calculo_cuenta = ttk.LabelFrame(self)
        
        vc = (self.register(utl.validar_numero), "%P")
        self.lb_aporte_cliente = ttk.Label(self.frame_calculo_cuenta, text="Pago Cliente", style="Custom.TLabel")
        self.lb_aporte_cliente.grid(row=0, column=0)
        self.aporte_cliente = ttk.Entry(self.frame_calculo_cuenta, textvariable=self.var_aporte_cliente, validate="key", validatecommand=vc)
        self.aporte_cliente.grid(row = 0, column=1)
        self.aporte_cliente.bind("<KeyRelease>", self.calcular_precio)
        
        
        self.lb_saldo_cliente = ttk.Label(self.frame_calculo_cuenta, text="Saldo Cliente", style="Custom.TLabel")
        self.lb_saldo_cliente.grid(row=1, column=0)
        self.saldo_cliente = LabelP(self.frame_calculo_cuenta, textvariable=self.var_saldo_cliente, style="Custom.TLabel")
        self.saldo_cliente.grid(row = 1, column=1)
        
        self.btn_vender  = ttk.Button(self.frame_calculo_cuenta, text="Vender",command=self.vender, style="Custom.TButton")
        self.btn_vender.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
        self.btn_salir  = ttk.Button(self.frame_calculo_cuenta, text="Salir",command=self.salir, style="CustomQuit.TButton")
        self.btn_salir.grid(row=4, column=0, columnspan=2,sticky="nsew")
        
        self.btn_log_out  = ttk.Button(self.frame_calculo_cuenta, text="Salir Cuenta",command=self.log_out, style="CustomQuit.TButton")
        self.btn_log_out.grid(row=3, column=0, columnspan=2,sticky="nsew")
        
        self.expandir_widget(self.frame_calculo_cuenta, row=5, colum=2)
        self.frame_calculo_cuenta.grid(row=2, column=1,sticky="nsew")
        
        # Frame lista de productos
        self.frame_lista_producto = ttk.LabelFrame(self)
        self.win_lista_producto = ListaProducto(self.frame_lista_producto, self,[Producto.codigo,Producto.nombre, Producto.precio, Producto.cantidad])
        self.frame_lista_producto.grid(row=2, column=0, sticky="nsew")
        
        ## Configurar el frame principal del operario
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(2, weight=3)
        
        # guardar foco del frame
        self.entry_codigo.bind("<FocusIn>", self.controlador_de_foco)
        self.entry_nombre_producto.bind("<FocusIn>", self.controlador_de_foco)
        
        # Agregar producto automaticamente 
        self.entry_codigo.bind("<Return>", self.agregar_automaticamente)
        self.entry_nombre_producto.bind("<Return>", self.agregar_automaticamente)
        
        
    def vender(self):
        str = self.win_lista_producto.retornar_productos().to_string(index=False, justify="right", line_width=40)
        print(str)
        resp = messagebox.askokcancel("SOFTRULLO SOLUCIONS", "Esta seguro que desea vender los anteriores productos?)")
        if resp:
            try:
                BD.sacar_productos(self.win_lista_producto.retornar_productos())
                messagebox.showinfo("SOFTRULLO SOLUCIONS", "Operacion Exitosa!")
                self.win_lista_producto.vaciar_productos()
                self.var_saldo_cliente.set(0)
                self.var_total.set(0)
                self.var_aporte_cliente.set(0)
                
                self.out_total.formatear_valor()
                self.saldo_cliente.formatear_valor()
                
            except:
                messagebox.showerror("SOFTRULLO SOLUCIONS", """Algo inesperado a ocurrido con la base de datos
                                     por favor comunicarse con el soporte técnico""")
    
    
    def calcular_precio(self, event):
        try:
            valor_aporte = self.var_aporte_cliente.get()
            saldo = valor_aporte - self.var_total.get()
            self.var_saldo_cliente.set(saldo)
            self.saldo_cliente.formatear_valor()
            if saldo < 0:
                # Estas dos funciones siempre van juntas cuando la clase es LabelP
                self.saldo_cliente.configure(style="CustomError.TLabel")
            else:
                self.saldo_cliente.configure(style="Custom.TLabel")
        except:
            pass
        
    
    def salir(self):
        self.app.on_close()
    
    def log_out(self):
        if messagebox.askokcancel("Log Out", "¿Estás seguro de que quieres terminar sesión?"):
            notebok_tabs= self.root.tabs()
            self.root.tab(notebok_tabs[2], state="disabled")
            self.root.tab(notebok_tabs[1], state="disabled")
            self.root.tab(notebok_tabs[0], state="normal")
            self.root.select(notebok_tabs[0])
    
    def controlador_de_foco(self, event):
       self.foco_frame = event.widget
    
    def agregar_automaticamente(self, event):
        self.buscar_producto()
    
    def eliminar_producto_auto(self, event):
        self.win_lista_producto.eliminar_producto()
        
    def buscar_producto(self):
        if self.foco_frame == self.entry_codigo or self.foco_frame == self.entry_nombre_producto:
            try:
                if self.foco_frame == self.entry_codigo:
                    values = BD.buscar_producto_cod(self.var_buscar_cod.get())   
                    self.var_descrip_cod.set(values[0])
                    self.var_descrip_nombre.set(values[1])
                    self.var_descrip_precio.set(values[2])
                    self.var_descrip_cantidad.set(1)
                    self.agregar_producto()
                    
                elif self.foco_frame == self.entry_nombre_producto:
                    values = BD.buscar_producto_nombre(self.var_buscar_nombre.get())
                    self.var_descrip_cod.set(values[0])
                    self.var_descrip_nombre.set(values[1])
                    self.var_descrip_precio.set(values[2])
                    self.var_descrip_cantidad.set(1)
                    self.agregar_producto()
                        
            except  ExcepBus as e:  
                messagebox.showwarning("SOFTRULLO SOLUCIONS", "Codigo o Nombre no encontrado. ¡Vaya al panel de administrador para agregarlo!")
                        
            self.var_buscar_cod.set("")
            self.var_buscar_nombre.set("")
    
    
    
    # Funciones de la visualización de los productos temporal
    def agregar_producto(self):
        self.win_lista_producto.agregar_producto(self.retornar_valores_producto())
        self.limpiar_variables()
        
        
    def eliminar_producto(self):
        self.win_lista_producto.eliminar_producto()

    def modificar_producto(self):   
        self.win_lista_producto.modificar_producto(self.retornar_valores_producto())
        self.limpiar_variables()
    
    def expandir_widget(self, frame:ttk.LabelFrame, row=2, colum=2):
        for i in range(row):
            frame.rowconfigure(i, weight=1)
        for i in range(colum):
            frame.columnconfigure(i, weight=1)
    
    def limpiar_variables(self):
        self.var_descrip_nombre.set("")
        self.var_descrip_cod.set("")
        self.var_descrip_precio.set(0)
        self.var_descrip_cantidad.set(0)
        
    def doble_click_producto_modificar(self,valores):
        self.var_descrip_cod.set(valores[0])
        self.var_descrip_nombre.set(valores[1])
        self.var_descrip_precio.set(valores[2])
        
        res = simpledialog.askinteger("SOFTRULLO SOLUCIONS", "Ingrese una cantidad")
        if res:
            self.var_descrip_cantidad.set(res)
            self.modificar_producto()
        
    def retornar_valores_producto(self):
        return {
            Producto.codigo: [self.var_descrip_cod.get()],
            Producto.nombre: [self.var_descrip_nombre.get()],
            Producto.precio: [self.var_descrip_precio.get()],
            Producto.cantidad: [self.var_descrip_cantidad.get()]
        }
        
    def actualizar_precio_total(self):
        # Calcular precio total 
        self.var_total.set(self.win_lista_producto.calcular_precio_productos())
        self.out_total.formatear_valor()
        
    def format_currency(self,value):
        return "${:,.2f}".format(value)



