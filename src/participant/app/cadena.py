import json
import cryptografy
from pathlib import Path
import bd
import contrato
import json
import datetime
from config import _blockchain, _credential


class Cadena():
    def __init__(self):
        if self.okchain() is True:
            url = str(_blockchain)
            with open(url) as f:
                jblock = json.load(f)
            self.chain = jblock
        else:
            self.chain = []

    def okchain(self):
        url = _blockchain
        if (Path(url).is_file()):
            return True
        else:
            return False

    def okcredencial(self):
        url = '/home/nodo/BD/Blockchain/credencial.json'
        if (Path(url).is_file()):
            return True
        else:
            return False

    def cadena(self):
        return self.chain

    def crear_bloque(self, hash_anterior, contract, registro, credencial, totalbloques, clave=None):
        # se puede agregar las caracteristicas que se quiera en el bloque
        Crypto = cryptografy.Crypto(credencial['Role'], clave)
        metadata = {'index': totalbloques+1,
                    'state': str(1),
                    'timestamp': str(datetime.datetime.now()),
                    'CA': Crypto.hash(credencial),
                    'previous_hash': hash_anterior,
                    'hash_Data': Crypto.hash(registro)}  # HASH
        block = {
            'metadata': metadata,
            'smartcontract': contract,
            'register': registro
        }
        hashblock = Crypto.hash(block)
        if credencial['Role'] != "System":
            firmahash = Crypto.firmar(hashblock)  
        else:
            firmahash = "system"
        metablock = {
            'hash0': firmahash,
            'hash1': hashblock,
            'actor': credencial['Role'],
            'block': {  
                'metadata': metadata,
                'smartcontract': contract,
                'register': registro}
        }
        return metablock

    def crear_genesis(self, config):
        BD = bd.BD(_blockchain)
        contrato = {
            'leading actor': 'none',
            'role actor': 'none',
            'writing': 'is a genesis block'
        }
        credencial = {'Name': 'Genesis', 'LastName': 'System',
                      'CitizenID': 'none', 'Role': 'System'}
        registro = config
        block = Cadena.crear_bloque('0', contrato, registro, credencial, 0)
        self.añadir_bloque(block.crear_bloque())
        return BD.guardar_archivo(self.chain)

    def previo_bloque(self):
        block = self.chain[-1]
        return block['block']

    def anterior_hash(self):
        block = self.chain[-1]
        return block['hash1']

    def añadir_bloque(self, block):
        BD = bd.BD(_blockchain)
        self.chain.append(block)
        BD.guardar_archivo(self.chain)

    def verificar_cadena(self):
        chain = self.chain
        previous_block = chain[0]
        previous_block = previous_block['block']
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            nombre = block['actor']
            firma = block['hash0']
            hashb = block['hash1']
            Crypto = cryptografy.Crypto(nombre, None, firma)
            if Crypto.autenticar(hashb) is True:
                if block['block']['metadata']['previous_hash'] != Crypto.hash(previous_block):
                    return False
            else:
                return False
            previous_block = block['block']
            block_index += 1
        return True

    def verificar_credencial(self, a1):
        try:
            verify = False
            blocks = len(self.chain)
            cadenatemporal = self.chain
            for i in range(blocks):
                leer = cadenatemporal[i]
                data = leer['block']['register']
                if 'CitizenID' in data and 'Role' in data:
                    if (leer['block']['register']['CitizenID'] == a1['CitizenID'] and leer['block']['register']['Role'] == a1['Role']):
                        verify = True
                        break
            return verify
        except Exception as e:
            return {'Respuesta': 'No', 'Mensaje': str(e)+" ccp"}

    def verificar_duplicado(self, CitizenID):
        chain = self.chain
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            data = block['block']['register']
            if "CitizenID" in data:
                if block['block']['register']['CitizenID'] == CitizenID:
                    return True
            block_index += 1
        return False

    def verificar_rol_duplicado(self, registro):
        chain = self.chain
        block_index = 0
        while block_index < len(chain):
            block = chain[block_index]
            data = block['block']['register']
            if "Role" in data:
                if block['block']['register']['Role'] == registro['Role']:
                    return True
            block_index += 1
        return False

    def firmas_asociadas(self, hashdato, role=""):
        chain = self.chain
        firmas = []
        block_index = 0
        firma=False
        while block_index < len(chain):
            block = chain[block_index]
            data = block['block']['register']
            if "Card" in data:
                if block['block']['register']['Card'] == hashdato:
                    firmas.append(block)
                    firma = role == block['block']['register']['RoleSign']
            block_index += 1
        if role != "":
            return firmas, firma
        return firmas

    def verificar_firma(self, credencial, hashdato):
        is_valid_credential = self.verificar_credencial(credencial)
        is_valid_chain = self.verificar_cadena()
        existe_tarjeta = self.consulta(hashdato)
        if is_valid_chain and is_valid_credential and existe_tarjeta:
            return True
        return False

    def consulta(self, hashdato):
        chain = self.chain
        block_index = 1
        result = False
        for block_index in range(len(chain)):
            block = chain[block_index]
            if block['block']['metadata']['hash_Data'] == hashdato:
                result = True
                break
        return result

    def consulta_datos(self, hashdato):
        chain = self.chain
        block_index = 1
        result = False
        for block_index in range(len(chain)):
            block = chain[block_index]
            if block['block']['metadata']['hash_Data'] == hashdato:
                result = block
                break
        return result

    def bd_listfirma(self):
        bc = self.cadena()
        bd_lf = []
        block_index = 0
        while block_index < len(bc):
            block = bc[block_index]
            data = block['block']['register']
            if "Role" in data:

                if block['block']['register']['Role'] == "Graduate":
                    #   sign=self.firmas_asociadas(block['block']['metadata']['hash_Data'])
                    dbase = bd.BD(_credential)
                    nodo = dbase.abrir_archivo()
                    del dbase
                    sign = self.firmas_asociadas(
                        block['block']['metadata']['hash_Data'], nodo["Role"])
                    fbd = {
                        'index': block['block']['metadata']['index'],
                        'Name': block['block']['register']['Name'],
                        'CitizenID': block['block']['register']['CitizenID'],
                        'CP': block['block']['register']['Professional Career'],
                        'Degree': block['block']['register']['Degree'],
                        'YearE': block['block']['register']['Year of Graduation'],
                        'hash_Data': block['block']['metadata']['hash_Data'],
                        'cantf': str(len(sign[0])),
                        'firma': sign[1],
                    }
                    bd_lf.append(fbd)
            block_index += 1
        return bd_lf
