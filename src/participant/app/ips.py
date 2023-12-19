#Archivo ips.py
import subprocess
import random
import platform  # Importa la biblioteca platform
import socket  # Importa el módulo socket

class Ip():
    def __init__(self, lista=None):
        self.iplista = lista

    def ip(self):
        output = subprocess.check_output("hostname -i", shell=True)
        output=output.splitlines()
        output=output[0].decode("utf-8")
        return output

    def excepcion(self):
        if not self.iplista is None:
            ipublic = "0"
            for nodoiip in self.iplista:
                if nodoiip['hostname'] == "Nodo Publico":
                    ipublic = nodoiip['ip']
                    return ipublic
            return ipublic
        return "0"

    def sort_node_consesous(self):
        ips = []
        for address in self.iplista:
            ip_nodo = address["ip"]
            if ip_nodo != self.ip() and ip_nodo != self.excepcion():
                ips.append(ip_nodo)
        aleatorio = random.choice(ips)
        return aleatorio

    def list_nodos(self):
        ips = []
        for ping in range(2, 10):  # DEBE COMENZAR DE 2
            address = "172.17.0." + str(ping)
            if address != self.ip():
                res = subprocess.call(['fping', '-t10', address])  # cambiar comandos
                if res == 0:
                    ips.append(address)
        print(ips)
        return ips

