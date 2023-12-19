#Archivo inicio.py
from functions import blockchain, credential
from flask import Flask, redirect, url_for

def inicio_():
    if not blockchain():
        return redirect(url_for('scb'))
    if not credential():
        return redirect(url_for('newnodo'))
    return redirect(url_for('registro'))
    