import json

nombre_archivo = "./BaseDatos/bd_logeo.json"

class BD_Usuario:
    def __init__(self):
        self.list_user = []
        
    def add_user(self,user,password,es_admin):
        usuario_log = {
            BD_Usuario_Mod.user:user,
            BD_Usuario_Mod.password:password,
            BD_Usuario_Mod.es_admin:es_admin
        }
        self.list_user.append(usuario_log)
        self.save_data(nombre_archivo)
        
    def to_json(self):
        return {
            BD_Usuario_Mod.list_user: self.list_user
        }

    @classmethod
    def from_json(cls, json_data):
        bd_usuario = cls()
        for usuario_log in json_data[BD_Usuario_Mod.list_user]:
            bd_usuario.add_user(usuario_log[BD_Usuario_Mod.user], 
                                usuario_log[BD_Usuario_Mod.password], 
                                usuario_log[BD_Usuario_Mod.es_admin])
        return bd_usuario
    
    def save_data(self, archivo):
        with open(archivo, "w") as file:
            json.dump(self.to_json(), file, indent=4)

    @classmethod
    def load_data(cls, archivo):
        with open(archivo, "r") as file:
            json_data = json.load(file)
        return cls.from_json(json_data)
    
    
    
    def es_user_valido(self, user, password):
        es_valido = False
        bd = self.load_data(nombre_archivo)
        for us in bd.list_user:
            if us[BD_Usuario_Mod.user] == user and us[BD_Usuario_Mod.password] == password:
                es_valido = True
        return es_valido
    
    def es_admin(self,user, password):
        es_admin=False
        bd = self.load_data(nombre_archivo)
        for us in bd.list_user:
            if us[BD_Usuario_Mod.user] == user and us[BD_Usuario_Mod.password] == password:
                es_admin = us[BD_Usuario_Mod.es_admin]
        return es_admin
        
    def retornar_usuarios(self):
        return self.load_data(nombre_archivo)

class BD_Usuario_Mod:
    user="user"
    password="password"
    es_admin = "es_admin"
    list_user = "list_user"
    nombre = "nombre"
    apellido = "apellido"
    

