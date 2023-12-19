developer=False
import os
#rutas
# _path = "C:/Users/User/"
_path = "/home/nodo"

_blockchain = os.path.join(_path, 'BD', 'blockchain.json')
_credential = os.path.join(_path, 'BD', 'credencial.json')
_configuration = os.path.join(_path, 'BD', 'config.json')
_solicitudes = os.path.join('app', 'biblioteca', 'solicitudes.json')
_key_dir = os.path.join(_path, 'keys')

_mailUname =  'email@test'
_mailPwd = 'password'
_fromEmail = 'email@test'