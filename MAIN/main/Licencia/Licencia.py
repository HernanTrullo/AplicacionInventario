import json
import datetime


class ModLic():
    clave = "clave"
    state = "state"
    time = "time"
    date_ini = "date_ini"
    date_fin = "date_fin"
    
    
class Licencia():
    nombre_ar = "./Licencia/licencia.json"
    @classmethod
    def from_json(cls):
        with open(cls.nombre_ar, 'r') as archivo:
            return json.load(archivo)
    @classmethod
    def to_json(cls, data):
        with open(cls.nombre_ar, 'w') as archivo:
            json.dump(data, archivo, indent=4)
    
    @classmethod
    def es_valida_clave(cls, clave):
        resp = False
        lic = cls.from_json()
        if (lic[ModLic.clave] == clave):
            resp = True    
        return resp
    
    @classmethod
    def set_clave(cls, clave):
        lic = cls.from_json()
        lic[ModLic.clave] = clave
        cls.to_json()
    
    @classmethod
    def es_activa_clave(cls):
        return cls.from_json()[ModLic.state]
    
    @classmethod
    def set_date_ini(cls, date):
        lic = cls.from_json()
        lic[ModLic.date_ini] = date
        cls.to_json(lic)
    @classmethod
    def set_date_fin(cls, date):
        lic = cls.from_json()
        lic[ModLic.date_fin] = date
        cls.to_json()
    @classmethod
    def set_state_lic(cls, state):
        lic = cls.from_json()
        lic[ModLic.state] = state
        cls.to_json(lic)
    
    @classmethod
    def set_lic(cls, clave, state, date_ini, date_fin):
        lic={
            ModLic.clave:clave,
            ModLic.state:state,
            ModLic.date_ini:date_ini,
            ModLic.date_fin: date_fin
        }
        cls.to_json(lic)
        
    @classmethod
    def get_licencia(cls):
        lic = cls.from_json()
        return (lic[ModLic.clave], lic[ModLic.state], lic[ModLic.date_ini], lic[ModLic.date_fin])
        
    
    
    