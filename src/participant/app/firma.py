#Archivo firma.py
from flask import Flask, request,  redirect, url_for, render_template, jsonify

import json

from config import _credential
from functions import blockchain, credential
from cadena import Cadena

def firma_():
    if not blockchain():
        return redirect(url_for('scb'))
    if not credential():
        return redirect(url_for('newnodo'))
    blockchain_ = Cadena()
    signlist=blockchain_.bd_listfirma()
    #return jsonify(signlist[::-1])
    return render_template('listafirma.html', datablockf=signlist[::-1])