#Archivo scb.py
from flask import  redirect, url_for

import json

from config import _blockchain, _configuration
from functions import conexion_data
from bd import BD
from ips import Ip

def scb_():
    network = Ip()
    # WINDOWS DEVELOPER
    is_developer = True  # Cambia a False si no eres desarrollador

    if is_developer:
        listN = network.list_nodos()  # Verifica los nodos activos de la red.
    else:
        listN = []  # De lo contrario, mantener la lista vacía
    del network  # Termino la instancia Ip
    i = 0
    while i < len(listN):
        respuesta = conexion_data(listN[i], "5000", "rcb", "get")
        # respuesta.raise_for_status()  # raises exception when not a 2xx response
        if respuesta['Respuesta'] == "OK":
            # Guardar Blockchain recibida
            bdatos = BD(_blockchain)
            blockchain = json.loads(respuesta['BC'])
            bdatos.guardar_archivo(blockchain)
            del bdatos
            # Guardar Configuracion recibida
            bdatos = BD(_configuration)
            configuracion = json.loads(respuesta['config'])
            bdatos.guardar_archivo(configuracion)
            del bdatos
            return redirect(url_for('newnodo')) #Verificar si es correcto usar return dentro while
        else:
            i += 1
    return redirect(url_for('setup'))
