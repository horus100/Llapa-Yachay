import os
import pathlib
from pathlib import Path
import requests
from flask import Flask, session, abort, redirect, request, render_template, jsonify, url_for, flash

from recurso import ip, almacenar
import json


app=Flask(__name__)

developer = True

@app.route("/")
def index():

    if not os.path.exists('config'):
        os.makedirs('config')

    if not os.path.exists('biblioteca'):
        os.makedirs('biblioteca')
        
    if not os.path.exists('bd'):
        os.makedirs('bd')

    url = 'config/listN.json'
    if os.path.isfile(url):
        url = 'bd/blockchain.json'
        if os.path.isfile(url):
            with open(url, 'r') as f:
                datablock = json.load(f)
            return render_template('index.html', datablock=datablock[::-1])
        else:
            registro = []
            with open(url, 'w') as f:
                jblock = json.dump(registro, f)
            return render_template('index.html')
    else:
        registro = []
        with open(url, 'w') as f:
            json.dump(registro, f)
        return redirect(url_for('scl'))


@app.route('/scl')  # Las siglas significan send de consulta lista
def scl():
    if developer:
        return redirect(url_for('index'))
    i = 2
    encontrobc = False
    myip =str(ip())
    nodoname = "Nodo Publico"
    infonodo = {'hostname': nodoname, 'ip': myip}
    url = 'bd/blockchain.json'
    if not os.path.isfile(url):
        while i < 10 and encontrobc is False:
            ih = "http://172.17.0." + str(i)
            if ip() != ih:
                # Las siglas rcb significan reciben consulta lista
                url = str(ih+":5000/rcl")
                try:
                    respuesta = requests.get(url, data=infonodo)
                    if respuesta.status_code == 200:
                        respuesta = json.loads(respuesta.text)
                        if respuesta['Respuesta'] == "OK":
                            almacenar(json.loads(respuesta['listN']), 'listN')
                            i += 1
                            encontrobc = True
                        else:
                            i += 1
                    else:
                        i += 1
                except requests.exceptions.RequestException:
                    break
            else:
                i += 1

    # Abrir archivo listN.json y obtener lista de nodos
    with open('config/listN.json', 'r') as f:
        nodos = json.load(f)

    for nodo in nodos:
        # Hacer consulta al nodo
        url = f'http://{nodo["ip"]}:5000/rcb'
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.json()['Respuesta'] == 'OK':
                # Actualizar listN con la respuesta del nodo
                with open('config/listN.json', 'w') as f:
                    f.write(response.json()['config'])

                # Guardar BC en blockchain.json
                with open('bd/blockchain.json', 'w') as f:
                    f.write(response.json()['BC'])

                # Salir del loop si se actualizó satisfactoriamente
                break
        except:
            # Continuar con el siguiente nodo si hubo error de conexión
            continue
    if encontrobc is True :
        return redirect(url_for('index'))
    else:
        return jsonify(nodos)


# Las siglas significan recep de consulta blockchain#
@app.route('/rcb', methods=['GET'])
def rcb():
    respuesta = {'Respuesta': 'NO'}
    return jsonify(respuesta)


@app.route('/addblock', methods=['GET'])
def addblock():
    try:
        block = json.loads(request.form['addblock'])
        url = 'bd/blockchain.json'
        if os.path.isfile(url):
            with open(url, 'r') as f:
                blockchain = json.load(f)
        blockchain.append(block)
        with open(url, 'w') as f:
            json.dump(blockchain, f)
        return jsonify({'Respuesta': 'OK'})
    except Exception as e:
        return jsonify({'Respuesta': 'No', 'Mensaje': str(e)})


@app.route('/addnodo', methods=['POST'])
def addnodo():
    nodo = request.form['nododata']
    nodo = json.loads(nodo)
    almacenar(nodo, 'listN')
    return jsonify({'Respuesta': 'OK'})


# Las siglas significan send de consulta lista
@app.route('/consulta', methods=["POST"])
@app.route('/search/<hash>', methods=["GET"])
def consulta(hash=None):
    if request.method == 'POST':
        i = 2
        encontrobc = False
        search = request.form["Tbuscar"]
        paq = {"Tbuscar": search}
        listares = []
                
        # Abrir archivo listN.json y obtener lista de nodos
        with open('config/listN.json', 'r') as f:
            nodos = json.load(f)["nodos"]
        # return jsonify(nodos)
        for nodo in nodos:
        # Hacer consulta al nodo
            if ip() != nodo["ip"]:
                # Las siglas rcb significan reciben consulta lista
                url = f'http://{nodo["ip"]}:5000/rcth'
                try:
                    respuesta = requests.post(url, data=paq)
                    if isinstance(respuesta, requests.Response):
                        if respuesta.status_code == 200:
                            respuesta = json.loads(respuesta.text)
                            listares.append(respuesta)
                            if respuesta['Respuesta'] == "OK":
                                if "diploma" in respuesta:
                                    diploma = respuesta['diploma']
                                    firma = respuesta['firmas']
                                    encontrobc = True
                                break
                        elif str(respuesta.status_code) == "404":
                            continue
                        else:
                            mensaje_error = f"Error al realizar la solicitud  codigo a {url}. Código de respuesta: {respuesta.status_code}"
                            return "error " + mensaje_error + "  "+str(url)+"  "+str(nodo["ip"])+"  "+str(listares)+str(paq)+ip()
                    else:
                        mensaje_error = f"Error al realizar la solicitud a {url}. Respuesta no válida: {respuesta}"
                        return "error " + mensaje_error + "  "+str(url)+"  "+str(nodo["ip"])+"  "+str(listares)+str(paq)+ip()
                except requests.exceptions.RequestException as e:
                    mensaje_error = f"Error al realizar la solicitud a {url}. Excepción: {str(e)}"
                    return "error " + mensaje_error + "  "+str(url)+"  "+str(nodo["ip"])+"  "+str(listares)+str(paq)+ip()
        if encontrobc is True:
            return render_template("diploma.html", data=diploma, firmas=firma)
        else:
            return "No existe blockchain o titulo"
    if request.method == 'GET':
        i = 2
        encontrobc = False
        search = hash
        paq = {"Tbuscar": search}
        listares = []
        while i < 10 and encontrobc == False:
            ih = "http://172.17.0." + str(i)
            if ip() != ih:
                # Las siglas rcb significan reciben consulta lista
                url = str(ih+":5000/rcth")
                try:
                    respuesta = requests.post(url, data=paq)
                    if respuesta.status_code == 200:
                        respuesta = json.loads(respuesta.text)
                        listares.append(respuesta)
                        if respuesta['Respuesta'] == "OK":
                            diploma = json.loads(respuesta['diploma'])
                            firma = respuesta['firmas']
                            encontrobc = True
                        else:
                            i += 1
                    else:
                        return "error http" + str(respuesta)+"  "+str(url)+"  "+str(ih)+"  "+str(listares)+str(paq)+ip()
                except requests.exceptions.RequestException:
                    break
            else:
                i += 1
        if encontrobc is True:
            return render_template("diploma.html", data=diploma, firmas=firma)
        else:
            return "No existe blockchain  "


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
