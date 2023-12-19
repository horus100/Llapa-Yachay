from flask import Flask, request, jsonify
import json
from pathlib import Path

from config import _configuration
from bd import BD


def addnodo_():
    try:
        nodo_data = json.loads(request.form['nododata'])
        database = BD(_configuration)
        if not Path(_configuration).is_file():
            configuracion={
                'DNS':"ninguno",
                'Nombre':"ninguno",
                'estado':"0",
                'nodos':[]
            }
            database.guardar_archivo(configuracion)
        configuracion = database.abrir_archivo()
        configuracion['nodos'].append(nodo_data)
        database.guardar_archivo(configuracion)
        return jsonify({'Respuesta':'OK'})
    except Exception as e:
        return jsonify({'Respuesta':'No','Mensaje': str(e)})
