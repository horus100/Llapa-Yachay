#Archivo exchagekey.py
from flask import Flask, request, jsonify, redirect, url_for
from functions import blockchain, credential
from config import _path, _credential

from cadena import Cadena
from bd import BD

def exchangekey_():
    if not blockchain():
        return redirect(url_for('scb'))
    if not credential():
        return redirect(url_for('newnodo'))
    public=request.form['kp']
    name=request.form['nk']           
    with open(_path+"/keys/"+name+"-public.pem", "w") as f:
        f.write(public)
    bdatos=BD(_credential)
    bdatos.abrir_archivo()
    name=bdatos.abrir_archivo()["Role"]
    with open(_path+"/keys/"+name+"-public.pem", "r") as f:
        public = f.read()
    data={'name':name,'public':public}
    return jsonify(data)