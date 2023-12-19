#archivo cryptografy.py
import io
import os
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from hashlib import sha256
import json
import config

class Crypto():
    def __init__(self,nombre,clave=None,data=None):
        self.nombre=nombre
        self.clave=clave
        self.data=data
        
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return sha256(encoded_block).hexdigest()
        
    ###############################################
    ## CREAR LLAVES ###############################
    ###############################################

    def generarkeys(self):
        key = RSA.generate(2048)
        private_key = key.export_key(passphrase=self.clave)
        private_key_path = os.path.join(config._key_dir, f"{self.nombre}-private.pem")
        with open(private_key_path, "wb") as f:
            f.write(private_key)
        public_key = key.publickey().export_key()
        public_key_path = os.path.join(config._key_dir, f"{self.nombre}-public.pem")
        with open(public_key_path, "wb") as f:
            f.write(public_key)
    ###############################################
    ## Archivo ####################################
    ###############################################




    ###############################################
    ## CIFRADO ####################################
    ###############################################

    def encriptar(self):
        bin_data = self.data.encode("utf-8")
        with open(os.path.join(config._key_dir, self.nombre+"-public.pem"), "rb") as f:
            recipient_key = f.read()
            key = RSA.importKey(recipient_key)
        cipher_rsa = PKCS1_OAEP.new(key)
        aes_key = get_random_bytes(16)
        enc_aes_key = cipher_rsa.encrypt(aes_key)
        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(bin_data)
        enc_data = b"".join((enc_aes_key, cipher_aes.nonce, tag, ciphertext))
        return enc_data

    def decifrar(self):
        data_file = io.BytesIO(self.data)
        with open(os.path.join(config._key_dir, self.nombre+"-private.pem"), "rb") as f:
            recipient_key = f.read()
        key = RSA.importKey(recipient_key, passphrase=self.clave)
        cipher_rsa = PKCS1_OAEP.new(key)
        enc_aes_key, nonce, tag, ciphertext = (data_file.read(c) for c in (key.size_in_bytes(), 16, 16, -1))
        aes_key = cipher_rsa.decrypt(enc_aes_key)
        cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        cadena = data.decode("utf-8")
        print(cadena)

    #############################################
    ## FIRMA ####################################
    #############################################

    def firmar(self, data_firmar):
        with open(os.path.join(config._key_dir, self.nombre+"-private.pem"), "rb") as f:
            recipient_key_data = f.read()

        try:

            recipient_key = RSA.import_key(recipient_key_data, passphrase=self.clave)
            h = SHA256.new(data_firmar.encode('utf-8'))
            # Firmar el resumen del mensaje con la clave privada
            signature = pkcs1_15.new(recipient_key).sign(h)
            signature_hex = signature.hex()

            return signature_hex

        except Exception as e:
            # En caso de cualquier error, emitir una alerta
            print(f"Error al firmar: {str(e)}")
            return None

    def autenticar(self, aut_block):
        route = os.path.join(config._key_dir, self.nombre + "-public.pem")
        
        with open(route, "rb") as f:
            recipient_key = f.read()
        
        keyp = RSA.importKey(recipient_key)
        block = aut_block.encode('utf-8')
        h = SHA256.new(block)
        signature_bytes = bytes.fromhex(self.data)  # Asegúrate de que self.data sea la firma en formato hexadecimal.

        try:
            pkcs1_15.new(keyp).verify(h, signature_bytes)  # Usar solo 'h' en lugar de SHA256.new(h)
            print("La firma es válida.")
            return True
        except (ValueError, TypeError, Crypto.Signature.pkcs1_15.VerificationError) as e:
            print(f"La firma no es válida. Error: {str(e)}")
            return False
