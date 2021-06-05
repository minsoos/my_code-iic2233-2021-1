from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
import parametros as p
from PyQt5 import uic

nombre, padre = uic.loadUiType(p.DISENO_VENTANA_POSTRONDA)


class VentanaPostRonda(nombre, padre):

    senal_salir = pyqtSignal()
    senal_continuar = pyqtSignal()
    senal_salir_inicio = pyqtSignal()


    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ventana de preparación")
        self.setWindowIcon(QIcon(p.RUTA_LOGO_INICIO))
        '''
        Esta ventana contendrá la información del juego que acaba
        de ocurrir, podrá elegir salir a la ventana de inicio o
        continuar jugando, e ir a la ventana de preparación
        '''
        self.label_foto.setPixmap(QPixmap(p.RUTA_FOTO_POSTRONDA))
        self.boton_salir.clicked.connect(self.metodo_salir)
        self.boton_salir_inicio.clicked.connect(self.metodo_salir_inicio)
        self.boton_continuar.clicked.connect(self.metodo_continuar)
    
    def inicializar_ventana(self, puntaje, i_buenos, i_malos, vida, perdio):
        self.label_puntaje.setText(f"{puntaje}")
        self.label_items_buenos.setText(f"{i_buenos}")
        self.label_items_malos.setText(f"{i_malos}")
        self.label_vida.setText(f"{vida}")
        self.boton_continuar.setEnabled(not perdio)
        if perdio:
            self.label_perdio.show()
            self.label_no_perdio.hide()
        else:
            self.label_no_perdio.show()
            self.label_perdio.hide()
        self.show()
    
    def metodo_salir(self):
        self.hide()
        self.senal_salir.emit()
    
    def metodo_salir_inicio(self):
        self.hide()
        self.senal_salir_inicio.emit()
    
    def metodo_continuar(self):
        self.hide()
        self.senal_continuar.emit()