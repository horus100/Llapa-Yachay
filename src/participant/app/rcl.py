#Archivo rcl.py
from flask import Flask, request, jsonify, redirect, url_for

import json
import os
from config import  _configuration
from ips import Ip
from bd import BD

def rcl_(): 
    if os.path.isfile(_configuration):
        infonodo=request.form.to_dict()
        #Registra nodo en la lista de nodos de la configuracion
        blockchain = BD(_configuration)
        config=blockchain.abrir_archivo()
        config['nodos'].append(infonodo)
        blockchain.guardar_archivo(config)
        #Comparto lista de nodos
        lista=json.dumps(config['nodos'])
        respuesta={'Respuesta':'OK','listN':lista} 
        del blockchain
        return jsonify(respuesta)
    respuesta={'Respuesta':'No'} 
    return jsonify(respuesta)