from functions import blockchain, credential
from flask import Flask, jsonify,request
import json

from config import _configuration
from functions import conexion_data
from bd import BD   

def consensofirma_():
    if request.method=='GET': 
        try:
            data = json.loads(request.form['data'])
            credential=data['credencial'] 
            signhash=data['hash']
            ipsend=data['ipenvio']
            database=BD(_configuration)
            listN=database.abrir_archivo()["nodos"]#

            if len(listN)>=2:
                votacion=[]
                for ip in listN:
                    if ip['ip']!=ipsend and ip["hostname"]!="Nodo Publico":
                        elements={'signblock':signhash,'credentialnode':credential}
                        package={"data":json.dumps(elements)}
                        respuesta=conexion_data(ip['ip'],"5000","ccp","get",package)
                        votacion.append(respuesta) 
                vc=0
  
                for cont in votacion:
                    if cont["Mensaje"] is False:
                        vc+=1
                if len(listN)>=((3*vc)+1):
                    resultado={"Respuesta":"SI"}
                    return jsonify(resultado)
                else:
                    resultado={"Respuesta":"No"}
                    return jsonify(resultado)
            else:
                resultado={"Respuesta":"SI"}
                return jsonify(resultado)
        except Exception as e:
            return jsonify({'Respuesta':'No','Mensaje': str(e)})