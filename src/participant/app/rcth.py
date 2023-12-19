#Archivo rcth.py
from flask import Flask, request, jsonify

from cadena import Cadena

def rcth_():
    try:
        hash = request.form.get("Tbuscar")
        hash = hash.replace(" ","")
        blockchain = Cadena()
        result = blockchain.consulta_datos(hash)
        if result:
            firmas = blockchain.firmas_asociadas(hash)
            response = {'Respuesta': 'OK', 'diploma': result, 'firmas': firmas}
        else:
            response = {'Respuesta': 'NO'}
    except KeyError:
        response = {'Respuesta': 'ERROR', 'mensaje': 'La clave proporcionada no se encuentra en la cadena'}
    except TypeError:
        response = {'Respuesta': 'ERROR', 'mensaje': 'El tipo de dato proporcionado no es válido'}
    except:
        response = {'Respuesta': 'ERROR', 'mensaje': 'Ha ocurrido un error inesperado'}
    return jsonify(response)
