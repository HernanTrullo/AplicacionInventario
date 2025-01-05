from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from BaseDatos.control_bd_socios import UsuarioDB as SOCIO


class Listausuario(ttk.Treeview):
    def __init__(self, root, win,col):
        self.df = pd.DataFrame()
        for column in col:
            self.df[column] = None
        
        super().__init__(root, columns=list(self.df.columns), show="headings")
        self.win = win
        # Configuración de los nombres de las columnas
        i = 0
        for column in self.df.columns:
            self.heading(column, text=column)
            if i<2:
                self.column(column, anchor="w")
                
            else:
                self.column(column, anchor="center", width=150)
            i +=1
                
        self.pack(side="left",fill=BOTH, expand=True, padx=5, pady=15)
        
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.yview)
        self.scrollbar.pack(fill="y", side="right",padx=5, pady=15)
        
        # Configurar la Treeview para que utilice la Scrollbar
        self.configure(yscrollcommand=self.scrollbar.set)
        
        
    def agregar_usuario(self, user):
        # la construccion del data es necesaria pues a la inicialización
        # De pd.DataFrame se requiere ese formato para ser añadido
        data = {
            SOCIO.cedula:           [user[SOCIO.cedula]],
            SOCIO.nombre:           [user[SOCIO.nombre]],
            SOCIO.total_cartera:    [user[SOCIO.total_cartera]],
            SOCIO.total_comprado:   [user[SOCIO.total_comprado]]
        }
        res = self.df.loc[self.df[SOCIO.cedula] == data[SOCIO.cedula][0]]
        if (res.empty):
            self.df = pd.concat([self.df, pd.DataFrame(data)], ignore_index=True)
        self.actualizar()    
            
            
    def modificar_saldo_usuario(self, user):
        data = {
            SOCIO.cedula:           user[SOCIO.cedula],
            SOCIO.nombre:           user[SOCIO.nombre],
            SOCIO.total_cartera:    user[SOCIO.total_cartera],
            SOCIO.total_comprado:   user[SOCIO.total_comprado]
        }
        
        self.df.loc[self.df[SOCIO.cedula] == data[SOCIO.total_cartera][0], SOCIO.total_cartera] = data[SOCIO.total_cartera]
        self.df.loc[self.df[SOCIO.cedula] == data[SOCIO.total_comprado][0], SOCIO.total_comprado] = data[SOCIO.total_comprado]
        self.actualizar()
    
    def abonar_cartera(self, abono):
        selection = self.selection()
        if (len(selection) == 1):
            values = self.item(selection, "values")
            total_cartera =  self.df.loc[self.df[SOCIO.cedula] == values[0], SOCIO.total_cartera].values[0] - abono
            if (total_cartera >=0):
                self.df.loc[self.df[SOCIO.cedula] == values[0], SOCIO.total_cartera] = total_cartera
            else:
                messagebox.showwarning("LMH SOLUTIONS","Va a abonar mas de lo que debe!")
        else:
            messagebox.showwarning("LMH SOLUTIONS","Debe seleccionar solamente uno de los usuarios")
        self.actualizar()
        
    def eliminar_usuario(self):
        selected_item = self.selection()
        if selected_item:
            res = messagebox.askokcancel("LMH SOLUTIONS", "Está seguro que desea eliminar el usuario")
            if res:
                for s_item in selected_item:
                    self.df.drop(self.index(s_item),inplace=True)  
                
                self.df.reset_index(drop=True, inplace=True)         
        else:
            messagebox.showwarning("LMH SOLUTIONS", "!No ha seleccionado ningún producto¡")   
        
        self.actualizar()
        
    def actualizar(self):
        # Borrar todos
        for item in self.get_children():
            self.delete(item)
            
        # Insertar datos en la tabla
        for i,row in self.df.iterrows():
            self.insert('', 'end', values= list(row)) 
            
    
    def vaciar_productos(self):
        # Borrar todos
        for item in self.get_children():
            self.delete(item)
            
        self.df = self.df.drop(self.df.index)
        
    def retornar_productos(self):
        return self.df
    
    