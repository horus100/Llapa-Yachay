from flask import Flask, request, jsonify

import json

from bd import BD
from cadena import Cadena

def ccp_():
    if request.method=='GET':
        try:
            data = json.loads(request.form["data"])
            credential=data["credentialnode"]
            #credential=json.loads(credential) #Credencial del nodo solicitante
            hash=data["signblock"]
            #Verificar firma
            blockchain = Cadena()
            decision=blockchain.verificar_firma(credential,hash)
            resultado={"Mensaje":decision}
            return  jsonify(resultado)
        except Exception as e:
            return jsonify({'Respuesta':'No','Mensaje': str(e)+" ccp"})