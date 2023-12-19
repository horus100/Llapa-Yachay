from flask import request, redirect, url_for, flash, jsonify
import json
from config import _credential, _configuration, developer
from functions import conexion_data,ConexionDataError
from bd import BD
from cadena import Cadena
from ips import Ip
from nodo import Nodo
from sendmail import Correo
from titulo import Titulo
import traceback


def Processfirma_():
    try:
        mensaje = None 

        if request.method == 'POST':
            # Obtener la credencial
            credential = BD(_credential).abrir_archivo()
            signhash = request.form['hash']  # Hash del bloque a firmar
            password = request.form['passw']
            data = {'credencial': credential, 'hash': signhash}

            if not developer:  # Si no está en modo desarrollo
                blockchain = Cadena()
                config = BD(_configuration).abrir_archivo()
                listN = config.get("nodos", [])  # Lista de nodos
                solicitud = "SI"

                if len(listN) > 1:
                    ip = Ip(listN)
                    data['ipenvio'] = ip.ip()
                    package = {"data": json.dumps(data)}
                    ip_elegido = ip.sort_node_consesous()
                    
                    try:
                        solicitud = conexion_data(ip_elegido, "5000", "consensofirma", "get", package)
                    except ConexionDataError as e:
                        flash(f"Error en la función conexion_data: {e}")
                        return redirect(url_for('firma'))
                    
                    solicitud = solicitud["Respuesta"]

                if solicitud != "SI":
                    raise Exception("Error en el consenso")

            node = Nodo(credential)
            try:
                result, block = node.firmar(signhash, password)
                if result:
                    if developer:  # Si está en modo desarrollo
                        mensaje = "Se firmó correctamente el registro y se envió el título"
                    else:
                        data = {'addblock': json.dumps(block)}
                        cant = 1
                        error_message = ''

                        if len(listN) > 1:
                            for node in listN:
                                if node['ip'] != ip.ip():
                                    response = conexion_data(node['ip'], "5000", "addblock", "get", data)
                                    if response['Respuesta'] == 'OK':
                                        cant += 1
                                    else:
                                        error_message += response['Respuesta']+'-'

                        if cant == len(listN):
                            del blockchain
                            blockchain = Cadena()
                            signhash = block['block']['register']['Card']
                            totalsign = blockchain.firmas_asociadas(signhash)
                            mensaje = f"Se firmó correctamente el registro. Firmas asociadas: {len(totalsign)} firmas de {config.get('qty', 0)} nodos"

                            if int(len(totalsign)) == int(config.get("qty", 0)):
                                registro = blockchain.consulta_datos(signhash)
                                email = registro['block']['register']['email']
                                CitizenID = registro['block']['register']['CitizenID']
                                nombre = registro['block']['register']["Name"]
                                grado = registro['block']['register']["Degree"]
                                host = config["DNS"]
                                titulo = Titulo(CitizenID, nombre, grado, signhash, host)
                                archivo = titulo.construir1()
                                if archivo:
                                    print("Este es la ruta del articulo generado "+archivo)
                                asunto="Sending of professional title"
                                mail = Correo(email, signhash, archivo,asunto,True)
                                mail.sendEmail()
                                mensaje = "Se firmó correctamente el registro y se envió el título"
                else:
                    raise Exception(f"No se firmo el bloque : {block}")
            except Exception as e:
                error_traceback = traceback.format_exc()
                raise Exception(f"Ocurrió un error en el proceso: {e}\nDetalle del error:\n{error_traceback}")
            if mensaje:
                flash(mensaje)
            else:
                raise Exception(f"El consenso denegó la solicitud. Nodo concensuador: {block}"+ error_message)

    except Exception as e:
        flash(f"Error: {str(e)}")
    finally:
        return redirect(url_for('firma'))


