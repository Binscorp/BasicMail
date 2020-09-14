import smtplib, getpass, os, sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QDialog,QLineEdit, QTreeWidgetItem, QCheckBox
from PyQt5 import uic
from PyQt5.QtGui import QFont
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64 
import ctypes #GetSystemMetrics
from PrototypeSearch import Dialogo
from CheckMail import CheckMail
from SaveMail import generateFileEncrypt, openFileEncrypt
import copy


class WindowEMail(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("vistas/viewmain.ui", self)
        if not os.path.exists(os.getcwd() + "\\keepConnect.gen"):
            self.ArchivosAdjuntos = []
            self.DisableElements(True)
            
            self.Password.setEchoMode(QLineEdit.Password)
            self.Login.clicked.connect(self.validar_formulario)
            self
            self.Logout.clicked.connect(self.Logout_)
            self.Adjunt.clicked.connect(self.Adjuntar)
            self.Enviador.clicked.connect(self.SendMail)
            self.Delete.clicked.connect(self.DelList)
            self.Validacion_correcta = False
            self.Explorador = Dialogo(self)
        else:
            user, password = openFileEncrypt()
            self.User.setText(user)
            self.Password.setText(password)
            self.ArchivosAdjuntos = []
            self.DisableElements(False)
            
            self.Password.setEchoMode(QLineEdit.Password)
            self.Login.clicked.connect(self.validar_formulario)

            self.Mantener.setCheckState(2)
            self.Logout.clicked.connect(self.Logout_)
            self.Adjunt.clicked.connect(self.Adjuntar)
            self.Enviador.clicked.connect(self.SendMail)
            self.Delete.clicked.connect(self.DelList)
            self.Validacion_correcta = False
            self.Explorador = Dialogo(self)
            self.validar_formulario()
        self.show()

    


    #Abrir explorador de archivos
    def Adjuntar(self):
        self.Explorador.show()
        
        
    def showEvent(self,event):
        self.Warnings.setStyleSheet("font-size: 14px;")
        self.Warnings.setText("Ingresa a tu correo....")

    def closeEvent(self, event):
        if not self.Validacion_correcta:
            resultado = QMessageBox.question(self, "Salir","¿Seguro quiere salir de la aplicacion?",
            QMessageBox.Yes | QMessageBox.No)
            if resultado == QMessageBox.Yes:
                self.Explorador.CloseAll()
                event.accept

            else:
                event.ignore()

    def validar_formulario(self):
        try:
            user = self.User.text()
            password = self.Password.text()

            if not password == "" and not user == "":
                self.Mail = CheckMail(user, password) # Usar el scrip para validar los diferentes dominios para el correo

                if not self.Mail.eMail == None:
                    self.Warnings.setText("Logeado")
                    self.Validacion_correcta = True
                    self.DisableElements(False)
                    if self.Mantener.checkState() == 2:
                        generateFileEncrypt(user, password)
            else:
                self.Warnings.setStyleSheet("font-size: 15px;")
                self.Warnings.setText("No dejes campos vacios")

        except Exception as e: 
            error = type(e).__name__
            if error == "SMTPAuthenticationError":
                self.Warnings.setStyleSheet("font-size: 13px;")
                self.Warnings.setText("Contraseña erronea")
            elif error == "TypeError" or error == "AttributeError":
                self.Warnings.setStyleSheet("font-size: 15px;")
                self.Warnings.setText("Correo no existe o contraseña\nerronea")
            elif error == "TimeoutError":
                self.Warnings.setStyleSheet("font-size: 15px;")
                self.Warnings.setText("Error conexion")                

            else:
                print(type(e).__name__)

        
    def Logout_(self):
        resultado = QMessageBox.question(self, "Logout","¿Quiere cerrar sesion?", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes:
            self.Validacion_correcta = False
            self.Mail.eMail.quit()
            self.Warnings.setText("Ingresa a tu correo....")
            if os.path.exists(os.getcwd() + "\\keepConnect.gen"):
                os.remove("keepConnect.gen")
            self.DisableElements(True)

    #Metodo para codificiar los archivos en el mensaje
    def EncondeArchives(self,header):
        if not self.ArchivosAdjuntos == []:
            for _ in range(len(self.ArchivosAdjuntos)):
                Archivo = self.ArchivosAdjuntos[_][1]
                if (os.path.isfile(Archivo)):
                    adjunto = MIMEBase('application', 'octet-stream')
                    adjunto.set_payload(open(Archivo, "rb").read())
                    encode_base64(adjunto)
                    adjunto.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(Archivo))
                    header.attach(adjunto)

    #Metodo para enviar el mensaje y construirlo
    def SendMail(self):
        resultado = QMessageBox.question(self, "Confirmacion","¿Quieres enviar este mensaje?",
        QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes:   
            Destinario = self.Destino.text()
            Asunto = self.SubjectLine.text()
            Mensaje = self.MensajeCuerpo2.toPlainText()
            print(Mensaje)
            header = MIMEMultipart()
            header['Subject'] = Asunto
            header['From'] = self.User.text()
            header['To'] = Destinario
            Mensaje = MIMEText(Mensaje, 'plain')
            header.attach(Mensaje)
            self.EncondeArchives(header)
            self.Mail.eMail.sendmail(self.User.text(), Destinario, header.as_string())

    #Desactiva elementos o activa elementos dependiendo del estado
    def DisableElements(self, Activador):

        if Activador:
            self.Estado.setStyleSheet("color:rgb(175, 0, 0);")
            self.Estado.setText("Desconectado")
            #Poner en blanco los espacios**
            self.Destino.setText("")
            self.SubjectLine.setText("")
            self.MensajeCuerpo2.setText("")
            #Eliminar elementos y limpiar la lista de archivos
            self.ArchivosAdjuntos = []
            self.ListAd.clear()
            self.Password.setText("")
            self.Password.setEchoMode(QLineEdit.Password)
            self.Mantener.setCheckState(False)
        else:
            self.Estado.setStyleSheet("color:rgb(69, 208, 0);")
            self.Estado.setText("Conectado")

        # **

        # Activar y desactivar elementos
        self.Enviador.setEnabled(not Activador)
        self.Destino.setEnabled(not Activador)
        self.SubjectLine.setEnabled(not Activador)
        self.MensajeCuerpo2.setEnabled(not Activador)
        self.Logout.setEnabled(not Activador)

        self.ListAd.setEnabled(not Activador)
        self.Delete.setEnabled(not Activador)
        self.Adjunt.setEnabled(not Activador)

        
        self.Mantener.setEnabled(Activador)
        self.Login.setEnabled(Activador)
        self.User.setEnabled(Activador)
        self.Password.setEnabled(Activador)
        



    #Añadir elementos en la lista de archivos para enviar
    def AddList(self):
        self.ListAd.clear()
        for _ in range(len(self.ArchivosAdjuntos)):
            self.ListAd.insertTopLevelItems(0,[QTreeWidgetItem(self.ListAd, self.ArchivosAdjuntos[_])])

    #Eliminar elementos en la lista de archivos para enviar
    def DelList(self):
        try:
            item = self.ListAd.currentItem().text(0)
            aux = []
            for _ in range(len(self.ArchivosAdjuntos)):
                if not item == self.ArchivosAdjuntos[_][0]:
                    aux.append(self.ArchivosAdjuntos[_])

            self.ArchivosAdjuntos = copy.copy(aux)
            self.AddList()
            self.Explorador.UpdateAr(self.ArchivosAdjuntos)
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Ventana = WindowEMail()
    Ventana.show()
    app.exec_()
