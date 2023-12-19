#Archivo sendmail.py
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os
from config import _mailPwd, _mailUname, _fromEmail
correo_Asunto = "Creacion Hash del Titulo Profesional"

class Correo():
    def __init__(self,dest,hash,archivo=None,asunto=correo_Asunto,title=False):
        self.smtpHost="smtp.gmail.com"
        self.smtpPort=587
        self.mailUname = _mailUname
        self.mailPwd = _mailPwd
        self.fromEmail = _fromEmail
        self.asunto=asunto
        self.hash=hash
        if title:
            self.msgtexto=f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: 'Times New Roman', serif;
                            background-color: #fdfdfd;
                            color: #333;
                            line-height: 1.6;
                        }}
                        .container {{
                            max-width: 700px;
                            margin: 30px auto;
                            padding: 30px;
                            background: #fff;
                            border: 2px solid #007bff;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        }}
                        .header {{
                            text-align: center;
                            margin-bottom: 40px;
                        }}
                        .header img {{
                            width: 100px;
                            height: auto;
                        }}
                        .header h1 {{
                            margin: 10px 0;
                            color: #007bff;
                        }}
                        .certificate-code {{
                            background-color: #f2f2f2;
                            padding: 15px;
                            margin-top: 20px;
                            text-align: center;
                            font-weight: bold;
                            border: 1px dashed #007bff;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>National University</h1>
                        </div>
                        <p>Dear,</p>
                        <p>We are thrilled to inform you that your university degree has been officially issued and is now ready for download.</p>
                        <p>Your degree is a testament to your hard work and dedication. We are proud to count you among our alumni.</p>
                        <div class="certificate-code">Degree Code: {hash}</div>
                        <p>Best regards,</p>
                        <p>National University</p>
                    </div>
                </body>
            </html>
            """
        else:
            self.msgtexto=f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            color: #333;
                            line-height: 1.6;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 20px auto;
                            padding: 20px;
                            background: #fff;
                            border: 1px solid #ddd;
                        }}
                        .hash-code {{
                            background-color: #e7e7e7;
                            padding: 10px;
                            margin-top: 15px;
                            text-align: center;
                            font-weight: bold;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <p>Dear,</p>
                        <p>In this message, we send you the hash code to consult your Professional Title and your signed progress:</p>
                        <div class="hash-code">{hash}</div>
                        <p>You can use this code on our website to make your enquiry.</p>
                        <p>Kind regards,</p>
                        <p>National University</p>
                    </div>
                </body>
            </html>
            """

        self.destinatario=dest
        self.archivo=archivo

    def sendEmail(self):
        # create message object
        msg = MIMEMultipart()
        msg['From'] = self.fromEmail
        msg['To'] = self.destinatario
        msg['Subject'] = self.asunto
        # msg.attach(MIMEText(mailContentText, 'plain'))
        msg.attach(MIMEText(self.msgtexto, 'html'))

        # create file attachments
        if not self.archivo is None:
            # check if file exists
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(self.archivo, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{0}"'.format(os.path.basename(self.archivo)))
            msg.attach(part)
        
        # Send message object as email using smptplib
        s = smtplib.SMTP(self.smtpHost, self.smtpPort)
        s.starttls()
        s.login(self.mailUname, self.mailPwd)
        msgText = msg.as_string()
        sendErrs = s.sendmail(self.fromEmail, self.destinatario, msgText)
        s.quit()

        # check if errors occured and handle them accordingly
        if not len(sendErrs.keys()) == 0:
            raise Exception("Errors occurred while sending email", sendErrs)
        return