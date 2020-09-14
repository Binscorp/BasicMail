import sys, time, os
from PyQt5.QtWidgets import QApplication, QDialog, QTreeWidgetItem, QMessageBox
from PyQt5 import uic
from os import listdir, path, stat,startfile
from mimetypes import MimeTypes

class Dialogo(QDialog):
    def __init__(self,MainWin):
        QDialog.__init__(self)
        
        uic.loadUi("vistas/viewsearch.ui",self)
        self.Buscar.clicked.connect(self.getDir)
        self.Directorio.itemDoubleClicked.connect(self.OpenElement)
        self.Adds.clicked.connect(self.SaveElement)
        self.Atras.clicked.connect(self.backDir)
        self.Rutas.setText(os.getcwd()) # Obtener ruta actual del programa donde abrio
        self.MainWin = MainWin
        self.Archivos = self.MainWin.ArchivosAdjuntos
        self.getDir()

    #Metodo para regresar al directorio anterior    
    def backDir(self):
        if self.Rutas.text() == "C:\\Users" or self.Rutas.text() == "C:\\":
            self.Rutas.setText("C:\\")

        else:
            aux = self.Rutas.text()
            aux = aux.split("\\")
            aux.pop()
            aux = "\\".join(aux)
            self.Rutas.setText(aux)
            self.getDir()

        
        print(self.Rutas.text())
        self.getDir()

    def getDir(self):
        #Eliminar todas las filas de la busqueda anterior
        self.Directorio.clear()
        #Ruta indicada por el usuario
        dir = self.Rutas.text()
        #Si es un directorio
        if path.isdir(dir):
            #Recorrer sus elementos
            for element in listdir(dir):
                name = element
                pathinfo = dir + "\\" + name
                informacion = stat(pathinfo)
                #Si es un directorio
                if path.isdir(pathinfo):
                    type = "Carpeta de archivos"
                    size = ""
                    
                else:
                    mime = MimeTypes()
                    type = mime.guess_type(pathinfo)[0]
                    size = str(informacion.st_size) + "bytes"
                #Fecha de modificación
                date = str(time.ctime(informacion.st_mtime))
                # Crear un array para crear la fila con los items
                row = [name,date,type,size]
                #Insertar la fila
                self.Directorio.insertTopLevelItems(0,[QTreeWidgetItem(self.Directorio, row)])

    def OpenElement(self):
        #Obtener el item seleccionado por el usuario
        item = self.Directorio.currentItem()
        #Crear la ruta accediendo al nombre del elemento(archivo o carpeta)
        elemento = self.Rutas.text() + "\\" + item.text(0)
        #Si es un directorio navegar a su directorio
        if path.isdir(elemento):
            self.Rutas.setText(elemento)
            self.getDir()
        else: #Si es un archivo abrirlo
            startfile(elemento)

    def SaveElement(self):

        item = self.Directorio.currentItem()
        equal = False

        try:
            NombreElemento = item.text(0)
            RutaElemento = self.Rutas.text() + "\\" + NombreElemento
            #Guardar elementos en la lista
            if not path.isdir(RutaElemento):
                #Verificar si el archivo no esta repatido
                for n in range(len(self.Archivos)):

                    if RutaElemento in self.Archivos[n]:
                        equal = True
                    if equal:
                        break

                if not equal:    
                    self.ElementsLoad(Nombre_ = NombreElemento, Ruta_ = RutaElemento)
        #Si no hay item seleccionado al momento de agregar            
        except: 
            pass

        self.MainWin.AddList()
    #Carga las rutas de los elementos
    def ElementsLoad(self,Nombre_,Ruta_):
        self.Archivos.append([Nombre_,Ruta_])

    #Mantiene actilizado la lista de rutas
    def UpdateAr(self,archivo):
        self.Archivos = archivo

    def CloseAll(self): # Cerrar todo el proceso y la ventana cuando se cierra la ventana principal
        self.destroy()
        sys.exit()



