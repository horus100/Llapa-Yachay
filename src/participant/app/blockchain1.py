from flask import Flask, redirect, url_for, render_template
from functions import blockchain, credential

from cadena import Cadena

def systemblockchain_():
    if not blockchain():
        return redirect(url_for('scb'))
    if not credential():
        return redirect(url_for('newnodo'))
    databc = Cadena()
    data = databc.chain
    return render_template('blockchain.html', datablock=data[::-1])
