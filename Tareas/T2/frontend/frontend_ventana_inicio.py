from PyQt5 import uic
import parametros as p
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
import parametros as p

nombre_inicio, padre_inicio = uic.loadUiType(p.DISENO_VENTANA_INICIO)
nombre_error, padre_error = uic.loadUiType(p.DISENO_VENTANA_ERROR)


class VentanaInicio(nombre_inicio, padre_inicio):

    senal_solicitar_partida = pyqtSignal(str)
    senal_abrir_ranking = pyqtSignal()

    def __init__(self):
        '''
        Front-end de la ventana en la cual el jugador inicia
        el programa y puede iniciar un nuevo juego, como también
        ingresar a la ventana de rankings
        '''
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ventana de inicio")
        self.setWindowIcon(QIcon(p.RUTA_LOGO_INICIO))
        self.boton_ver_ranking.clicked.connect(self.metodo_abrir_ranking)
        self.boton_iniciar_partida.clicked.connect(self.metodo_iniciar_partida)
        self.logo_dona.setPixmap(QPixmap(p.RUTA_LOGO_INICIO))
        self.show()
        #QLineEdit para ingresar el nombre del jugador
        #QPushButton para iniciar una nueva partida con el nombre del lineedit
        #QPushButton para entrar a la ventana de rankings
    
    def metodo_iniciar_partida(self):
        '''
        Método conectado al botón iniciar partida, manda la senal
        senal_solicitar_partida a requerimiento_ver_ranking de la lógica,
        '''
        self.senal_solicitar_partida.emit(self.nombre.text())

    def metodo_abrir_ranking(self):
        '''
        Método conectado al botón ver ranking, manda la senal
        senal_abrir_ranking a comprobar_alfanum de la lógica,
        enviando el text del QLineEdit
        '''
        self.senal_abrir_ranking.emit()
    
    def inicio_partida(self, nombre):
        '''
        Recibe la señal_inicio_partida del backend,
        y esconde la ventana
        '''
        self.hide()
    
    def mostrar(self):
        self.show()


class VentanaError(nombre_error, padre_error):
    def __init__(self):
        '''
        Ventana que contiene un mensaje de error, que puede cerrarse
        '''
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ventana de error")
        self.boton_volver.clicked.connect(self.cerrar)
        self.foto_homero.setPixmap(QPixmap(p.RUTA_CEREBRO_HOMERO))
        self.foto_homero.setScaledContents(True)

    def cerrar(self):
        self.hide()

    def mostrar(self):
        self.show()

