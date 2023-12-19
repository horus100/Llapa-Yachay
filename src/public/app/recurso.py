import json
import subprocess
 
def almacenar (archivo,nombre):
  with open('config/'+nombre+'.json', 'w') as f:
    jblock=json.dump(archivo,f)
  return jblock

import platform

def ip():
    if platform.system() == "Windows":
        # Comando para obtener la dirección IP en Windows
        output = subprocess.check_output("ipconfig", shell=True)
        # Procesa la salida para encontrar la dirección IPv4
        output = output.decode("utf-8")
        lines = output.splitlines()
        for line in lines:
            if "IPv4 Address" in line:
                ip_address = line.split(":")[1].strip()
                return ip_address
    else:
        # Comando para obtener la dirección IP en Linux
        output = subprocess.check_output("hostname -i", shell=True)
        output = output.splitlines()
        output = output[0].decode("utf-8")
        return output


