from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from App import App
from Licencia.Licencia import Licencia
from tkinter import messagebox
from datetime import datetime as dt


def main():
    lic = Licencia().get_licencia()
    date_actual = dt.today()
    date_final_lic = dt.strptime(lic[3], "%Y-%m-%d") # Fecha final de la licencia
    
    delta_date = date_final_lic-date_actual 
    delta_date = delta_date.days + 1
    
    if (lic[1] and delta_date>1):    
        root = Tk()
        app = App(root, delta_date)
        app.mainloop()
    else:
        messagebox.showerror("SOFTRULLO SOLUCIONS", "La licencia no ha sido activada o ha expirado")

if __name__ == "__main__":
    main()
    


