#Archivo newnodo.py
from config import _credential, _configuration, _path, _key_dir
from functions import credential, ip, conexion_data, blockchain

from flask import Flask, redirect, url_for, request, render_template, flash, jsonify
import json

from cadena import Cadena
from bd import BD
from cryptografy import Crypto
from nodo import Nodo
import os
import re
def newnodo_():
    if not blockchain():
        return redirect(url_for('scb'))
    if credential():
        return redirect(url_for('inicio'))
    if request.method == "GET":
        blockchain_ = Cadena()
        node_config = blockchain_.chain[0]
        del blockchain_
        return render_template('newcredencial.html', data=node_config['block']['register'])
    if request.method == "POST":
        datas = request.form.to_dict()
        blockchain_ = Cadena()
        search_rol = blockchain_.verificar_rol_duplicado(datas)
        del blockchain_
        if search_rol is True:
            flash("Unregistered, there is a node registered with the same Peer Node")
            return redirect(request.url)
        password = datas['password']
        database = BD(_credential)
        datas.pop("password")
        datas.pop("password1")
        datas["Role"] = re.sub(r'\s+', '-', datas["Role"])
        database.guardar_archivo(datas)
        keys = Crypto(datas["Role"], password)
        keys.generarkeys()
        del database
        # Se verifica que no se esten registrando datos duplicados antes de registrar el nodo
        blockchain_ = Cadena()
        duplicate = blockchain_.verificar_duplicado(datas['CitizenID'])
        if duplicate:
            flash("Not registered, there is already a registered user with the data you entered.")
            return redirect(request.url)
        node = Nodo(datas)
        node.registrar_credencial1(password, 'Create New Node Credential')
        del blockchain_
        del node
        # Después de los filtros, registrar el nodo en la lista de nodos de la configuración
        database = BD(_configuration)
        config = database.abrir_archivo()  # Lista de nodos ["nodos"]
        myip = ip()
        nododata = {'hostname': datas["Role"], 'ip': myip}
        config["nodos"].append(nododata)
        database.guardar_archivo(config)
        resp = []
        # Replica el registro del nodo a los demás nodos de la red
        if len(config["nodos"]) > 1:
            replicas = 1  # Se inicia en 1 porque cuenta el registro del propio nodo
            package = {'nododata': json.dumps(nododata)}
            for node in config["nodos"]:
                if node['ip'] == myip:
                    continue
                response = conexion_data(node['ip'], "5000", "addnodo", "post", data=package)
                if response['Respuesta'] == "OK":
                    replicas += 1  # contabiliza los nodos que registraron el nodo correctamente
            if replicas == len(config["nodos"]):  # Si el total de nodos registraron sin problemas al nuevo nodo
                blockchain_ = Cadena()
                block = blockchain_.chain[-1]
                package = {'addblock': json.dumps(block)}
                replicas = 1
                for node in config["nodos"]:
                    if node['ip'] != ip():
                        response = conexion_data(node['ip'], "5000", "addblock", "get", package)
                        if response['Respuesta'] == 'OK':
                            replicas += 1
                if replicas == len(config["nodos"]):
                    with open(os.path.join(_key_dir, f'{datas["Role"]}-public.pem'), "r") as f:
                        public = f.read()

                    package = {'kp': public, 'nk': datas["Role"]}  # kp es key public y nk es nodo key
                    # Intercambio de llaves, donde se envía la llave pública y se recepciona las llaves públicas de los nodos
                    for node in config["nodos"]:
                        key_public = conexion_data(node['ip'], "5000", "exchangekey", "get", package)
                        with open(os.path.join(_key_dir, f"{key_public['name']}-public.pem"), "w") as f:
                            f.write(key_public['public'])
                    return redirect(url_for("inicio"))
                return "Se replicó el registro del nodo, pero hubo un problema con la réplica del bloque del registro"
            if replicas < len(config["nodos"]):
                return "algunos nodos no recibieron la información"
            return "ningún nodo recibió información"
        return redirect(url_for("inicio"))
