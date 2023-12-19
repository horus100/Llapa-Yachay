import cadena
import datetime
class Contrato():
    def __init__(self,credencial):
        self.card=credencial
    def smartcontract(self):
        Cadena=cadena.Cadena()
        req1= Cadena.verificar_credencial(self.card)
        req2= Cadena.verificar_cadena()
        if not req1:
            return req1, "Credential Verification Failed"
        if not req2:
            return req2,"Blockchain Verification Failed"
        return True,self.generar_contrato(self.card,'Certificate generated')

    # Funcion generar contrato
    def generar_contrato(self,a1,escritura):
        smartcontract= {
                'timesello':str(datetime.datetime.now()),
                'leading actor':str(a1['Name']+" "+a1['LastName']),
                'role actor':str(a1['Role']),
                'writing':escritura}
        return smartcontract
    # Funcion cancelar proceso
    def cancelar_proceso(self):
        return "It is not possible to execute process" 