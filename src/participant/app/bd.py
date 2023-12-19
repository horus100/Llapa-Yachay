import os
import json
from pathlib import Path

from config import _path

class BD ():
    def __init__(self, archivo_:str=""):
        if not os.path.exists(archivo_) and archivo_ != "":
          with open((archivo_), 'w') as f:
              json.dump([], f)
        self.archivo=archivo_
    @staticmethod
    def crear_carpeta(self,carpeta):
        if not (Path(_path+carpeta).is_dir()):
            os.mkdir(_path+carpeta)
 
    def guardar_archivo(self,datos):
        with open(self.archivo, 'w') as f:
            jblock=json.dump(datos,f)
        return jblock

    def abrir_archivo(self):
        url=self.archivo
        with open(url) as f:
            jblock=json.load(f)
        return jblock
  
    def almacenarsolicitud (self,solicitud):
      with open('app/biblioteca/solicitudes.json', 'w') as f:
        jblock=json.dump(solicitud,f)
      return jblock

    def abrirsolicitud(self):
      url=str('app/biblioteca/solicitudes.json')  
      with open(url) as f:
        jblock=json.load(f)
      return jblock