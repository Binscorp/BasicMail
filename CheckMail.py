import re
import smtplib, getpass, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64 

emailRegex = re.compile(r'''(
	[a-zA-Z0-9._%+-]+ 			# username
	@ 							# @ symbol
	[a-zA-Z0-9.-]+ 				# domain name
	(\.[a-zA-Z]{2,4}) 			# dot-something
	)''', re.VERBOSE)

class CheckMail():
	def __init__(self,Mail,Password):
		self.domainName = ""
		self.Mail = Mail
		self.Password = Password
		self.getDomainName()
		self.getHostPort(self.domainName)

	#Detectar el nombre del dominio del correo
	def getDomainName(self):
		domainName = emailRegex.search(self.Mail).group(0)
		domainName = domainName.split("@")
		domainName.pop(0)
		domainName = "".join(domainName)
		domainName = domainName.split(".")
		domainName = domainName.pop(0)
		self.domainName = domainName
		
	#Asignar el host,puerto SMTP y protocolo de cifrafo de datos por el nombre del dominio
	def getHostPort(self, DomainName):
		domainName = DomainName
		if domainName == "gmail":
			self.eMail = smtplib.SMTP('smtp.gmail.com', 587)
			self.eMail.starttls()
			self.eMail.login(self.Mail, self.Password)

		elif domainName == "outlook" or domainName == "toluca":
			self.eMail = smtplib.SMTP('smtp.office365.com', 587)
			self.eMail.starttls()
			self.eMail.login(self.Mail, self.Password)

		elif domainName == "yahoo":
			self.eMail = smtplib.SMTP('smtp.mail.yahoo.com', 25)
			self.eMail.starttls()
			self.eMail.login(self.Mail, self.Password)

		else:
			self.eMail = None


if __name__ == '__main__':

	print("Enviar email")

	user = input("Cuenta Correo: ")
	password = getpass.getpass("Password: ")

	#Cabeceras
	Remitente = user
	Destinario = input("To: ")
	Asunto = input("Subject: ")
	Mensaje = input("Menssage: ")
	#Host y puerto SMTP de GMAIL
	Mail = CheckMail(user,password)


	#Muestra la depuracion de la operacion de envio 1=True

	header = MIMEMultipart()
	header['Subject'] = Asunto
	header['From'] = Remitente
	header['To'] = Destinario
	Mensaje = MIMEText(Mensaje, 'plain')
	header.attach(Mensaje)

	#Enviar email
	Mail.eMail.sendmail(Remitente, Destinario, header.as_string())

	#Cerrar la conexion SMTP
	Mail.eMail.quit()