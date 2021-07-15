from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from utils import cargar_parametros, normalizar_ruta

parametros = cargar_parametros()
path_ventana_inicio = parametros["RUTAS"]["VENTANA_INICIO"]
path_ventana_inicio = normalizar_ruta(path_ventana_inicio)
nombre, padre = uic.loadUiType(path_ventana_inicio)


class VentanaInicio(nombre, padre):

    senal_intentar_ingreso = pyqtSignal(str)

    def __init__(self, ruta_logo, ruta_nubes) -> None:
        super().__init__()
        self.setupUi(self)
        #
        self.label_dron.setPixmap(QPixmap(ruta_logo))
        self.label_fondo.setPixmap(QPixmap(ruta_nubes))
        self.boton_ingresar.clicked.connect(self.intentar_ingreso)
        self.mostrar()
    
    def mostrar(self):
        self.show()
    
    def esconder(self):
        self.hide()

    def intentar_ingreso(self):
        nombre = self.edit_nombre.text()
        self.senal_intentar_ingreso.emit(nombre)

    def tramitar_ingreso(self, bool_, razon):
        if bool_:
            self.hide()
        elif not bool_:
            if razon == "cupos":
                self.edit_nombre.clear()
                self.edit_nombre.setPlaceholderText("No hay cupos en el servidor")
            elif razon == "nombre":
                self.edit_nombre.clear()
                self.edit_nombre.setPlaceholderText("Nombre inválido")
        else:
            raise TypeError("No entregaste un bool a tramitar ingreso")

