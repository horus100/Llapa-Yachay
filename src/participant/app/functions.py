#Archivo fuctions.py
from pathlib import Path
import subprocess
import json
import requests

from config import _blockchain,_credential, _configuration


def blockchain():
    if (Path(_blockchain).is_file()):
        return True
    else:
        return False
    
def credential():
    if (Path(_credential).is_file()):
        return True
    else:
        return False
    
import socket

def ip():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        return ip
    except socket.gaierror:
        return "No se pudo obtener la dirección IP"


class ConexionDataError(Exception):
    pass
def conexion_data(to_ip, puerto, enlace, metodo, data=None):
    url = f"http://{to_ip}:{puerto}/{enlace}"
    
    if metodo not in ["get", "post"]:
        raise ValueError(f"Método HTTP '{metodo}' no es válido.")
    
    try:
        if metodo == "get":
            res = requests.get(url, data=data)
        else:
            res = requests.post(url, data=data)
        
        res.raise_for_status()  

        return res.json()  

    except requests.exceptions.HTTPError as e:
        raise ConexionDataError(f"Solicitud HTTP fallida: {e}")
    except requests.exceptions.Timeout:
        raise ConexionDataError("Solicitud HTTP agotó el tiempo de espera")
    except requests.exceptions.RequestException as e:
        raise ConexionDataError(f"Error en la solicitud HTTP: {e}")


