from flask import Flask, redirect, url_for



from inicio import inicio_
from setup import setup_
from newnodo import newnodo_
from rcth import rcth_
from blockchain1 import systemblockchain_
from exchagekey import exchangekey_
from addnodo import addnodo_
from addblock import addblock_
from concensofirma import consensofirma_
from ccp import ccp_
from scb import scb_
from rcb import rcb_
from rcl import rcl_
from registro import registro_
from firma import firma_
from processfirma import Processfirma_
from config import developer

app=Flask(__name__)

#######################################################################################################################
###########################    CODIGO GENERAL                             #############################################
#######################################################################################################################

@app.route('/')
def inicio():
    return inicio_()

@app.route('/setup', methods=['POST','GET'])
def setup():
    return setup_()

@app.route('/newnodo', methods=['POST','GET'])
def newnodo():
    return newnodo_()

@app.route('/rcth', methods=['POST']) # Recepcion de Consulta Titulo Hash
def rcth():
    return rcth_()

@app.route('/blockchain')
def blockchain():
    return systemblockchain_()

@app.route('/exchangekey', methods=['GET'])
def exchangekey():
    return exchangekey_()

@app.route('/addnodo', methods=['POST'])
def addnodo():
    return addnodo_()

@app.route('/addblock', methods=['GET'])
def addblock():
    return addblock_()

@app.route('/consensofirma', methods=['GET'])
def consensofirma():
    return consensofirma_()

@app.route('/ccp', methods=['GET'])
def ccp():
    return ccp_()

@app.route('/scb') # Las siglas significan send de consulta blockchain
def scb():
    if developer:
        return redirect(url_for('setup'))
    return scb_()

@app.route('/rcb', methods=['GET']) # Las siglas significan recepcion de consulta blockchain
def rcb():
    return rcb_()
       
@app.route('/rcl',methods=['GET'])
def rcl():
    return rcl_()
    

########################################################################################################################
############################    REGISTRO                                   #############################################
########################################################################################################################

@app.route('/registro', methods=['POST','GET'])
def registro():
    return registro_()



########################################################################################################################
############################    FIRMA                                      #############################################
########################################################################################################################

@app.route('/firma')
def firma():
    return firma_()
    
@app.route('/Processfirma', methods=['POST'])
def processfirma():
    return Processfirma_()


########################################################################################################################
############################    BD DETALLES                                #############################################
########################################################################################################################
 
# ########################################################################################################################
# ############################    CONFIGURACION FINAL                        #############################################
# ########################################################################################################################
app.secret_key = 'the random string'
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
 

  



