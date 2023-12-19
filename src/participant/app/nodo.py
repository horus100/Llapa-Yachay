#Archivo nodo.py
import cadena
import ips

import cryptografy
import bd
import contrato
import datetime

class Nodo():
    def __init__(self,credencial):
        self.clase_ip=ips.Ip()
        self.credencial=credencial
        self.private_ip=self.clase_ip.ip()
        self.rol=self.credencial['Role']
        
    def registrar_credencial0(self,pw):
        Cadena=cadena.Cadena()
        duplicado= Cadena.verificar_duplicado(self.credencial['CitizenID'])
        if duplicado is False:
            self.registrar_credencial1(pw,'Create New Node Credential')
            return True
        else:
            return False
        
    def registrar_credencial1(self,pw,escritura):
        Cadena=cadena.Cadena()
        hash_anterior=Cadena.anterior_hash()
        contract={
              'timesello':str(datetime.datetime.now()),
              'leading actor':str(self.credencial['Name']+" "+self.credencial['LastName']),
              'role actor':str(self.credencial['Role']),
              'writing':str(escritura)
          }
        Cadena.añadir_bloque(Cadena.crear_bloque(hash_anterior,contract,self.credencial,self.credencial,len(Cadena.cadena()),pw))


    def crear_titulo(self,registro,pw):
        Cadena=cadena.Cadena()
        duplicado= Cadena.verificar_duplicado(registro['CitizenID'])
        contract=contrato.Contrato(self.credencial)
        accion=contract.smartcontract()
        if accion[0] is True and duplicado is False:
            sc=accion[1]
            hash_anterior=Cadena.anterior_hash()
            
            block=Cadena.crear_bloque(hash_anterior,sc,registro,self.credencial,len(Cadena.cadena()),pw)
            Cadena.añadir_bloque(block)
            return block['block']['metadata']['hash_Data']
        elif duplicado is True:
            return "Duplicate"
        else:
            return accion
    
    def firmar(self, hashdato, passw):
        try:
            # Validar la entrada
            if not hashdato or not passw:
                raise ValueError("Hashdato y passw son campos requeridos")

            Cadena_ = cadena.Cadena()
            Crypto = cryptografy.Crypto(None)
            Contract = contrato.Contrato(self.credencial)
            accion = Contract.smartcontract()
            existe_tarjeta = Cadena_.consulta(hashdato)

            if accion[0] is True and existe_tarjeta is True:
                sc = accion[1]
                hash_anterior = Cadena_.anterior_hash()
                registro = {'Card': hashdato, 'Sign': Crypto.hash(self.credencial), 'RoleSign': self.credencial['Role']}
                block = Cadena_.crear_bloque(hash_anterior, sc, registro, self.credencial, len(cadena.Cadena().chain), passw)
                Cadena_.añadir_bloque(block)
                return True, block
            else:
                raise Exception("The card does not exist or something went wrong")

        except ValueError as ve:
            raise Exception(f"Error de validación: {str(ve)}")
        except Exception as e:
            raise Exception(f"Error al firmar en funcion firmar de nodo : {str(e)}")

    def crear_llaves(self,pw):
        bdatos=bd.BD(None)
        bdatos.crear_carpeta("keys")
        crypto=cryptografy.Crypto(self.credencial['Role'],pw)
        crypto.generarkeys()
    
