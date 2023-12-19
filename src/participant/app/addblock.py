from flask import Flask, request, jsonify
import json

from cadena import Cadena


def addblock_():
    try:
        block_data = request.form.get('addblock')
        if not block_data:
            return jsonify({'Respuesta': 'No', 'Mensaje': 'Falta el bloque en la solicitud'})

        block = json.loads(block_data)
        blockchain = Cadena()
        blockchain.añadir_bloque(block)
        return jsonify({'Respuesta': 'OK'})

    except Exception as e:
        return jsonify({'Respuesta': 'No', 'Mensaje': f'Error en el nodo receptor: {str(e)}'})
