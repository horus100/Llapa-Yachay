from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

#biblioteca/titulos/config/letra.otf
class Titulo():
    def __init__(self,codigo,nombre,grado,hash,host, letra="/home/nodo/app/biblioteca/titulos/config/letra.otf"):
        self.alumno=nombre
        self.grado=grado
        self.hash=hash
        self.host=host
        self.codigo=codigo
        self.letra=letra

    def qr(self):
        input ="http://"+self.host+":5005/search/"+self.hash
        qr=qrcode.QRCode(version=1,box_size=10,border=1)
        qr.add_data(input)
        qr.make(fit=True)
        img=qr.make_image(fill='black',back_color='white')
        return img
    
    def escritura(self, image_width, constructor, escritura, letra, tamañodeletra, coordenadaY):
        color_texto = (0, 137, 209)
        tipo_letra = ImageFont.truetype(letra, tamañodeletra)
        text_bbox = constructor.textbbox((0, 0), escritura, font=tipo_letra)
        text_width = text_bbox[2] - text_bbox[0]
        coordenadas = ((image_width - text_width) / 2, coordenadaY)
        constructor.text(coordenadas, escritura, fill=color_texto, font=tipo_letra)

        
    def construir1(self):
        modelo_ruta = "/home/nodo/app/biblioteca/titulos/config/modelo.jpg"
        if not os.path.exists(modelo_ruta):
            print(f"No se pudo encontrar la imagen del modelo en {modelo_ruta}")
            return False
        certificado = Image.open(modelo_ruta, mode='r')
        qr = self.qr()
        new_qr = qr.resize((204, 204))
        image_width = certificado.width
        constructor = ImageDraw.Draw(certificado)
        self.escritura(image_width, constructor, self.grado, self.letra, 35, 660)
        self.escritura(image_width, constructor, self.alumno, self.letra, 45, 480)
        certificado.paste(new_qr, (780, 860))
        ruta_certificado = "/home/nodo/app/biblioteca/titulos/" + self.codigo + ".pdf"
        certificado.save(ruta_certificado)
        return ruta_certificado

