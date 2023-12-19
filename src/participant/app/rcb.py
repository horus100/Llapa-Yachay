#Archivo rcb.py
from flask import Flask, request, jsonify, redirect, url_for

import json

from config import _blockchain, _configuration
from functions import conexion_data, credential, blockchain
from bd import BD
from cadena import Cadena


def rcb_():                                                                              #
    if request.method=='GET':
        if not blockchain():
            respuesta={'Respuesta':'NO'}
            return jsonify(respuesta)
        blockchain_ =  Cadena() # Obtener toda la blockchain
        data = blockchain_.chain
        database = BD(_configuration)
        config = database.abrir_archivo()# Obtener el archivo de configuracion
        respuesta={'Respuesta':'OK','BC':json.dumps(data),'config':json.dumps(config)}       
        return jsonify(respuesta)                                                                             
                                                                             
            