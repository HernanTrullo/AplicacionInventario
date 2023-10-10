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
import datetime

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
        self.var_descrip_precio = tk.IntVar()
        self.var_descrip_precio_entra = tk.IntVar()
        self.var_descrip_cantidad = tk.IntVar()
        
        self.var_buscar_nombre = tk.StringVar()
        self.var_buscar_cod = tk.StringVar()
        
        self.var_total = tk.StringVar()
        self.var_total_vendido = tk.StringVar()
        
        self.foco_frame = None
        
        self.app = app
        
        self.create_widget()
        self.pack(fill="both", expand=True)
        
        
    def create_widget(self):
        # Frame que contiene el nombre del operario e información básica
        self.top_frame = ttk.LabelFrame(self)
        
        self.nameFrame = ttk.Label(self.top_frame, text="Bienvenido: ", style="Custom.TLabel")
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
        self.lb_cuenta = Label(self.frame_top_cuenta, text="Total_PV", style="Custom13.TLabel")
        self.lb_cuenta.grid(row=0, column=0, padx=10)
        self.out_total_vendido = LabelP(self.frame_top_cuenta, textvariable=self.var_total_vendido ,style="Custom13.TLabel") # La salida del total
        self.out_total_vendido.grid(row=0,column=1,padx=10)
        
        
        self.lb_total = ttk.Label(self.frame_top_cuenta, text="Total_PC", style="Custom13.TLabel")
        self.lb_total.grid(row=1, column=0, padx=10)
        self.out_total = LabelP(self.frame_top_cuenta, textvariable=self.var_total ,style="Custom13.TLabel") # La salida del total
        self.out_total.grid(row=1,column=1,padx=10)
        
        
        self.frame_top_cuenta.grid(row=0, column=1, rowspan=2,sticky="nsew")
        self.expandir_widget(self.frame_top_cuenta)
        
        # Bóton para cargar los datos al inventario, salir y log out
        self.frame_inventario = ttk.LabelFrame(self)
        
        self.btn_cargar_inventario = ttk.Button(self.frame_inventario, text="Cargar al inventario", command=self.cargar_inventario,style="CustomOperacion.TButton")
        self.btn_cargar_inventario.grid(row=0,column=0, sticky="nsew")
        
        self.btn_salir  = ttk.Button(self.frame_inventario, text="Salir",command=self.salir, style="CustomQuit.TButton")
        self.btn_salir.grid(row=2, column=0,sticky="nsew")
        
        self.btn_log_out  = ttk.Button(self.frame_inventario, text="Salir Cuenta",command=self.log_out, style="CustomQuit.TButton")
        self.btn_log_out.grid(row=1, column=0,sticky="nsew")
        
        self.expandir_widget(self.frame_inventario, row=3, colum=1)
        self.frame_inventario.grid(row=2, column=1, rowspan=3, sticky="nsew")
        
        
        # Frame del buscar de datos
        self.ingreso_datos = ttk.LabelFrame(self)
        
        self.lb_codigo = ttk.Label(self.ingreso_datos, text="Código")
        self.lb_codigo.grid(row=0, column=0)
        self.entry_codigo = ttk.Entry(self.ingreso_datos, textvariable=self.var_buscar_cod)
        self.entry_codigo.grid(row=1, column=0,sticky="nsew")
        
        self.lb_nombre_producto = ttk.Label(self.ingreso_datos, text="Nombre")
        self.lb_nombre_producto.grid(row=0, column=1)
        self.entry_nombre_producto = ttk.Combobox(self.ingreso_datos, textvariable=self.var_buscar_nombre)
        self.entry_nombre_producto.grid(row=1, column=1,sticky="nsew")
        self.entry_nombre_producto.bind("<KeyRelease>", self.actualizar_nombre_productos)
        
        self.expandir_widget(self.ingreso_datos, colum=3)
        self.ingreso_datos.grid(row=1, column=0,sticky="nsew")
        
        # Frame descripción del producto (Compra)
        self.frame_descrip_producto = ttk.LabelFrame(self)
        
        self.lb_cod_descrp_producto = ttk.Label(self.frame_descrip_producto, text="Código")
        self.lb_cod_descrp_producto.grid(row=0, column=0,sticky="nsew")
        self.entry_cod_descrp_producto = ttk.Entry(self.frame_descrip_producto, textvariable=self.var_descrip_cod)
        self.entry_cod_descrp_producto.grid(row=1, column=0,sticky="nsew")
        
        self.lb_nombre_descrp_producto = ttk.Label(self.frame_descrip_producto, text="Nombre")
        self.lb_nombre_descrp_producto.grid(row=0, column=1,sticky="nsew")
        # Widget descripción del producto
        self.entry_nombre_descrp_producto = ttk.Entry(self.frame_descrip_producto, textvariable=self.var_descrip_nombre)
        self.entry_nombre_descrp_producto.grid(row=1, column=1,sticky="nsew") # Entry
        
        
        self.lb_precio_decrip_producto = ttk.Label(self.frame_descrip_producto, text="Precio")
        self.lb_precio_decrip_producto.grid(row=0,column=2,sticky="nsew")
        # Widget precio del producto
        self.entry_precio_decrip_producto = ttk.Entry(self.frame_descrip_producto, textvariable=self.var_descrip_precio)
        self.entry_precio_decrip_producto.grid(row=1,column=2,sticky="nsew")
        
        self.lb_precioe_decrip_producto = ttk.Label(self.frame_descrip_producto, text="Precio Entrada")
        self.lb_precioe_decrip_producto.grid(row=0,column=3,sticky="nsew")
        # Widget precio entrada del producto
        self.entry_precioe_decrip_producto = ttk.Entry(self.frame_descrip_producto, textvariable=self.var_descrip_precio_entra)
        self.entry_precioe_decrip_producto.grid(row=1,column=3,sticky="nsew")
        
        
        self.lb_cantidad_decrip_producto = ttk.Label(self.frame_descrip_producto, text="Cantidad", width=20)
        self.lb_cantidad_decrip_producto.grid(row=0,column=4,sticky="nsew")
        # Widget canitidad del producto
        self.entry_cantidad_decrip_producto = ttk.Entry(self.frame_descrip_producto, textvariable=self.var_descrip_cantidad,width=20)
        self.entry_cantidad_decrip_producto.grid(row=1,column=4,sticky="nsew")
        
        self.cambiar_widget()
        self.frame_descrip_producto.grid(row=2, column=0,sticky="nsew")
        self.expandir_widget(self.frame_descrip_producto, colum=4)
        
        # Frame lista de productos
        self.frame_lista_producto = ttk.LabelFrame(self)
        self.win_lista_producto = ListaProducto(self.frame_lista_producto, self,[Producto.codigo,Producto.nombre, Producto.precio, Producto.precio_entrada,Producto.cantidad])
        self.frame_lista_producto.grid(row=4, column=0, sticky="nsew")
        
        # Frame Botones
        self.frame_botones = ttk.LabelFrame(self)
        
        self.btn_agregar = ttk.Button(self.frame_botones, text="Agregar", command=self.agregar_producto)
        self.btn_agregar.grid(row=0, column=3,sticky="nsew")  
        self.btn_modificar = ttk.Button(self.frame_botones, text="Modificar", command=self.modificar_producto)
        self.btn_modificar.grid(row=0, column=2,sticky="nsew")
        
        self.expandir_widget(self.frame_botones, row=1,colum=4)
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
    
    def actualizar_nombre_productos(self, event):
        try:
            self.entry_nombre_producto['values']=BD.retornar_nombres_productos(self.var_buscar_nombre.get())     
        except:
            self.entry_nombre_producto['values'] = [""]
    
    def actualizar_hora(self):
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        self.var_hora.set(hora_actual)
        self.after(1000, self.actualizar_hora)
        
        
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
        
    def buscar_producto(self):
        if self.foco_frame == self.entry_codigo or self.foco_frame == self.entry_nombre_producto:
            try:
                if self.foco_frame == self.entry_codigo:
                    values = BD.buscar_producto_cod(self.var_buscar_cod.get())   
                    self.var_descrip_cod.set(values[0])
                    self.var_descrip_nombre.set(values[1])
                    self.var_descrip_precio.set(values[2])
                    self.var_descrip_precio_entra.set(values[3])
                    self.var_descrip_cantidad.set(1)
                    
                elif self.foco_frame == self.entry_nombre_producto:
                    values = BD.buscar_producto_nombre(self.var_buscar_nombre.get())
                    self.var_descrip_cod.set(values[0])
                    self.var_descrip_nombre.set(values[1])
                    self.var_descrip_precio.set(values[2])
                    self.var_descrip_precio_entra.set(values[3])
                    self.var_descrip_cantidad.set(1)
                        
            except  ExcepBus as e:  
                respuesta=messagebox.askokcancel("SOFTRULLO SOLUCIONS", "Codigo o Nombre no encontrado. ¿Desea agregar uno?")
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
        resp = messagebox.askokcancel("SOFTRULLO SOLUCIONS", "Esta seguro que desea agregar los productos al inventario?")
        if resp:
            try:
                BD.cargar_inventario(self.win_lista_producto.retornar_productos())
                messagebox.showinfo("SOFTRULLO SOLUCIONS", "Productos agregados correctamente")
                self.win_lista_producto.vaciar_productos()
                
                self.var_total.set(0)
                self.out_total.formatear_valor()
                
            except:
                messagebox.showerror("SOFTRULLO SOLUCIONS", """Algo inesperado a ocurrido con la base de datos
                                    por favor comunicarse con el soporte técnico""")
                
        self.entry_codigo.focus()
            
            
    def agregar_producto(self):
        self.win_lista_producto.agregar_producto(self.retornar_valores_producto())
        self.limpiar_variables()
        self.cambiar_widget()
        self.actualizar_precio_total()
        
        self.entry_codigo.focus()
        
    def eliminar_producto(self):
        self.win_lista_producto.eliminar_producto()
        self.cambiar_widget()
        self.limpiar_variables()
        self.actualizar_precio_total()
        self.entry_codigo.focus()

    def modificar_producto(self):
        res = messagebox.askokcancel("SOFTRULLO SOLUCIONS", "Está seguro de que desea modificar los parámetros del producto?")
        if res:
            self.win_lista_producto.modificar_producto(self.retornar_valores_producto())
            self.cambiar_widget()
            self.limpiar_variables()
            messagebox.showinfo("SOFTRULLO SOLUCIONS", "Producto modificado correctamente")
            
        self.bloquear_botones(False)
        self.actualizar_precio_total()
        self.entry_codigo.focus()
    
    
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
            Producto.nombre: [self.var_descrip_nombre.get()],
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
        
            
