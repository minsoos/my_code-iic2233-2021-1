from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QEventLoop, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QMovie, QFont
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QLineEdit, QRadioButton, QSpinBox, QCheckBox, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
import sys
import parametros as p
from personajes import Homero, Lisa
from os import path
from random import randint

class VentanaJuego(QWidget):

    senal_pausa_juego = pyqtSignal()
    senal_salir_juego = pyqtSignal()
    senal_tecla_presionada = pyqtSignal(str, tuple)

    def __init__(self, personaje_ingresado=Lisa()):
        super().__init__()
        # Atributos de la ventana
        self.tamano_ventana = (500, 500)
        self.personaje = personaje_ingresado
        self.rutas_personajes = p.RUTAS_PERSONAJES
        self.rutas_imagenes = p.RUTAS_IMAGENES_JUEGO
        self.__posicion_personaje = (0,0)
        self.posiciones_obstaculos = set()
        self.generador_de_objetos = QTimer()
        self.generador_de_objetos.timeout.connect(self.generar_objeto)
        self.generador_de_objetos.setInterval()
        # Dar propiedades a la ventana
        self.size = (self.tamano_ventana)
        self.resize(*self.tamano_ventana)
        self.setWindowTitle("Ventana de Juego")
        #Label vida jugador
        #Label número de ronda
        #Label tiempo restante para finalizar ronda
        #Label ítems buenos atrapados
        #Label ítems malos atrapados
        #Label puntaje actual
        #QPushButton pausar el juego
        #QpushButton salir de juego
        #Label fondo
        #Labels de objetos

        self.init_gui()
        self.conexiones()
        self.show()

    @property
    def posicion_personaje(self):
        return self.__posicion_personaje

    @posicion_personaje.setter
    def posicion_personaje(self, lugar):
        '''
        Cambia la posición del personaje
        '''
        obstaculizado = False
        for obstaculo in self.posiciones_obstaculos:
            if obstaculo[0]-3 <= lugar[0] <= obstaculo[0]+15 or\
                obstaculo[1]-3 <= lugar[1] <= obstaculo[1]+15:
                obstaculizado = True
        if not obstaculizado:
            self.__posicion_personaje = lugar
            self.__label_personaje.move(*lugar)

    def generador_objeto(self):
        '''
        Este método genera un objeto cuando lo llama
        el QTimer
        '''

    def mover_personaje(self, lugar):
        self.posicion_personaje = lugar

    def keyPressEvent(self, tecla):
        '''
        Envía señal a tecla_presionada
        '''
        tecla = "w" if tecla.key() == Qt.Key_W else "s" if tecla.key() == Qt.Key_S else "d" if tecla.key() == Qt.Key_D  else "a" if tecla.key() == Qt.Key_A else "nada"
        self.senal_tecla_presionada.emit(tecla, self.posicion_personaje)
        
    def conexiones(self):
        self.personaje.senal_actualizar_animacion.connect(self.actualizar_personaje)


    def cargar_datos(self):
        '''
        A este método lo llama una señal del backend,
        y carga los datos que esta le entrega a los labels
        '''
    def actualizar_tablero(self):
        '''
        este método actualiza los labels de 
        la partida cuando se llama
        '''

    def actualizar_personaje(self, path_dado):
        '''
        este método actualiza los labels de 
        personaje cuando se llama
        '''
        pixeles = QPixmap(path_dado)
        pixeles = pixeles.scaled(self.tamano_ventana[0]/10, self.tamano_ventana[1]/10,\
                QtCore.Qt.KeepAspectRatio)
        self.__label_personaje.setPixmap(pixeles)
        

    def metodo_boton_pausar(self):
        '''
        Este método envía una señal a pausa_juego del backend
        '''
        self.senal_pausa_juego.emit()

    def metodo_boton_salir(self):
        '''
        Este método envía una señal a salir_juego del backend
        '''
        self.senal_salir_juego.emit()

    def init_gui(self):
        """
        Crea la interfaz de la ventana
        """
        # ---- Definicion de la barra superior ----
        
        # Logo superior izq
        self.label_logo = QLabel(self)
        pixeles = QPixmap(self.rutas_imagenes['logo'])
        pixeles = pixeles.scaled(self.tamano_ventana[0]/10, self.tamano_ventana[1]/10, QtCore.Qt.KeepAspectRatio)
        self.label_logo.setPixmap(pixeles)
        self.label_logo.setScaledContents(True)

        #Mapa por el que se mueve el jugador
        self.mapa = QLabel(self)
        pixeles = QPixmap(self.rutas_imagenes['mapa_planta'])
        pixeles = pixeles.scaled(self.tamano_ventana[0], self.tamano_ventana[1], QtCore.Qt.KeepAspectRatio)
        self.mapa.setPixmap(pixeles)
        self.mapa.setScaledContents(True)

        #INFO-------------------------------
        
        # vida
        self.label_vida = QLabel("Vida:", self)
        # Tiempo
        self.label_tiempo = QLabel("Tiempo", self)
        # items buenos
        self.label_items_buenos = QLabel("Ítems buenos", self)
        # items malos
        self.label_items_malos = QLabel("Ítems malos", self)
        # items buenos
        self.label_ronda = QLabel("Ronda:", self)
        # items malos
        self.label_puntaje = QLabel("Puntaje:", self)
        #Boton_pausar
        self.boton_pausar = QPushButton("Pausar", self)
        self.boton_pausar.clicked.connect(self.metodo_boton_pausar)
        #Boton_salir
        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.clicked.connect(self.metodo_boton_pausar)
        #Juntar layouts

        #
        layout_principal = QVBoxLayout()
        contenedor_info_y_logo = QHBoxLayout()  # Contenedor de la info superior
        contenedor_info = QVBoxLayout()
        contenedor_info_superior = QHBoxLayout()
        contenedor_info_inferior = QHBoxLayout()
        contenedor_info.addLayout(contenedor_info_superior)
        contenedor_info.addLayout(contenedor_info_inferior)
        contenedor_info_y_logo.addLayout(contenedor_info)

        #agregar datos
        contenedor_info_superior.addWidget(self.label_vida)
        contenedor_info_inferior.addWidget(self.label_tiempo)
        contenedor_info_superior.addWidget(self.label_items_buenos)
        contenedor_info_inferior.addWidget(self.label_items_malos)
        contenedor_info_superior.addWidget(self.label_ronda)
        contenedor_info_inferior.addWidget(self.label_puntaje)
        contenedor_info_superior.addWidget(self.boton_pausar)
        contenedor_info_inferior.addWidget(self.boton_salir)
        #Terminar layout superior (barra de progreso)
        contenedor_info_y_logo.addStretch()
        contenedor_info_y_logo.addWidget(self.label_logo)
        contenedor_info_y_logo.addLayout(contenedor_info)
        contenedor_info_y_logo.addStretch()
        #Terminar layout principal
        layout_principal.addStretch()
        layout_principal.addLayout(contenedor_info_y_logo)
        layout_principal.addWidget(self.mapa)
        layout_principal.addStretch()
        self.setLayout(layout_principal)
        self.init_gui_objetos_y_personaje()
    
    def init_gui_objetos_y_personaje(self):
        #Personaje
        self.__label_personaje = QLabel(self)
        if self.personaje.nombre in self.rutas_personajes.keys():
            ruta_inicial = self.rutas_personajes[self.personaje.nombre]
            pixeles = QPixmap(path.join(ruta_inicial, "up_3.png"))
            #pixeles = pixeles.scaled(self.tamano_ventana[0]/8, self.tamano_ventana[1]/8,\
                #QtCore.Qt.KeepAspectRatio)
            self.__label_personaje.setPixmap(pixeles)
            self.posicion_personaje = (80, 300)
            self.personaje.timer.start()
        else:
            raise ValueError("Este personaje no existe")
        # ------------------Obstaculos
        rutas_obstaculos = p.RUTAS_OBSTACULOS_PLANTA
        for _ in range(3):
            tupla = (randint(5, self.tamano_ventana[0]-5), randint(200, self.tamano_ventana[0]-5))
            self.posiciones_obstaculos.add(tupla)
        lista_posiciones_obstaculos = list(self.posiciones_obstaculos)
        self.label_obstaculo1 = QLabel(self)
        pixeles = QPixmap(rutas_obstaculos["1"])
        pixeles = pixeles.scaled(self.tamano_ventana[0]/100, self.tamano_ventana[1]/1000, QtCore.Qt.KeepAspectRatio)
        self.label_obstaculo1.setPixmap(pixeles)
        self.label_obstaculo1.setScaledContents(True)
        self.label_obstaculo1.move(*lista_posiciones_obstaculos[0])
        self.label_obstaculo2 = QLabel(self)
        pixeles = QPixmap(rutas_obstaculos["2"])
        pixeles = pixeles.scaled(self.tamano_ventana[0]/100, self.tamano_ventana[1]/100, QtCore.Qt.KeepAspectRatio)
        self.label_obstaculo2.setPixmap(pixeles)
        self.label_obstaculo2.setScaledContents(True)
        self.label_obstaculo2.move(*lista_posiciones_obstaculos[1])
        self.label_obstaculo3 = QLabel(self)
        pixeles = QPixmap(rutas_obstaculos["3"])
        pixeles = pixeles.scaled(self.tamano_ventana[0]/100, self.tamano_ventana[1]/100, QtCore.Qt.KeepAspectRatio)
        self.label_obstaculo3.setPixmap(pixeles)
        self.label_obstaculo3.setScaledContents(True)
        self.label_obstaculo3.move(*lista_posiciones_obstaculos[1])
        print(self.posiciones_obstaculos)
        # ----------------------
        # Label nombre jugador
        #self.label_nombre = QLabel()
        #font = QFont()
        #font.setPointSize(22)
        #font.setCapitalization(True)
        #font.setFamily("Fantasy")
        #self.label_nombre.setFont(font)
        #self.label_nombre.setStyleSheet("color: rgb(244, 223, 9)")
        ## Label icono jugador
        #self.label_icono = QLabel(self)
#
        ## Barras de vida
        #self.barra_vida_enemigo = QProgressBar()
        #self.barra_vida_enemigo.setTextVisible(False)
        #self.barra_vida_enemigo.setStyleSheet('QProgressBar{background-color: rgb(255, 0, 0);'
        #                                      'border-style:solid;}')
        #self.barra_vida_enemigo.setValue(100)
        #self.barra_vida_jugador = QProgressBar()
        #self.barra_vida_jugador.setTextVisible(False)
        #self.barra_vida_jugador.setStyleSheet('QProgressBar{background-color: rgb(255, 0, 0);'
        #                                      'border-style:solid;}')
        #self.barra_vida_jugador.setValue(100)
#
        ## Contenedor horizontal del icono y el nombre
        #hbox_superior = QHBoxLayout()
        #hbox_superior.addWidget(self.label_icono)
        #hbox_superior.addWidget(self.label_nombre)
        #contenedor_info.addLayout(hbox_superior)
#
        ## Contenedor horizontal de las barras de vida
        #hbox_vidas = QHBoxLayout()
        #hbox_vidas.addWidget(self.barra_vida_jugador)
        #hbox_vidas.addWidget(self.barra_vida_enemigo)
        #contenedor_info.addLayout(hbox_vidas)
#
        #self.layout_principal.addLayout(contenedor_info)
        #self.layout_principal.addStretch()
#
        ## ---- Definicion del area de combate ----
        ## Imagenes jugadores
        #self.jugador = QLabel(self)
        #self.jugador.setFixedSize(91.75 * 1.1, 187.5 * 1.1)
        #self.gif_jugador = QMovie(self.RUTASs['jugador'])
        #self.jugador.setMovie(self.gif_jugador)
        #self.jugador.setScaledContents(True)
        #self.gif_jugador.start()
        #self.jugador.move(60, 270)
#
        #self.enemigo = QLabel(self)
        #self.enemigo.setFixedSize(91.75 * 1.1, 187.5 * 1.1)
        #self.enemigo.setPixmap(QPixmap(self.RUTASs['enemigo']))
        #self.enemigo.setScaledContents(True)
#
        #self.enemigo.move(540, 270)
#
        ## ---- Definicion de los controles inferiores ----
        ## Contenedor horizontal de los controles
        #contenedor_controles = QHBoxLayout()
        ## Agregamos los botones al layout
        #contenedor_controles.addWidget(self.boton_patada)
        #contenedor_controles.addWidget(self.boton_frio)
        #contenedor_controles.addWidget(self.boton_defender)
        ## Definimos el estilo de los botones
        #self.boton_patada.setStyleSheet(self.estilo_botones)
        #self.boton_frio.setStyleSheet(self.estilo_botones)
        #self.boton_defender.setStyleSheet(self.estilo_botones)
        ## Apretamos los botones hacia la izquierda y agregamos el contenedor a la ventana principal
        #contenedor_controles.addStretch()
        #self.layout_principal.addLayout(contenedor_controles)
        ## Llamamos al método que tienen que implementar
        #self.conectar_botones()
        #self.repaint()


class LogicaVentanaJuego(QObject):

    senal_enviar_actualizacion_tablero = pyqtSignal()
    senal_cargar_tablero = pyqtSignal()
    senal_cambiar_boton_pausa = pyqtSignal()
    senal_cambiar_pos_personaje = pyqtSignal(tuple)
    senal_orientacion_personaje = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        '''
        Este es el backend de la ventana juego, y se encarga de
        realizar los procesos de esta
        '''

    def cargar_juego(self):
        '''
        Este método se encargará de leer el progreso de la partida
        cuando es llamado, y enviar la información al frontend 
        mediante la señal senal_enviar_actualizacion_tablero
        Además carga los objetos
        '''

    def tecla_presionada(self, tecla, pos_actual):
        if tecla in "wsad":
            if tecla == "w":
                label_personaje = "up"
                nueva_pos = (pos_actual[0], pos_actual[1] - 1)
            elif tecla == "s":
                label_personaje = "down"
                nueva_pos = (pos_actual[0], pos_actual[1] + 1)
            elif tecla == "a":
                label_personaje = "left"
                nueva_pos = (pos_actual[0] - 1, pos_actual[1])
            elif tecla == "d":
                label_personaje = "right"
                nueva_pos = (pos_actual[0] + 1, pos_actual[1])
            self.senal_cambiar_pos_personaje.emit(nueva_pos)
            self.senal_orientacion_personaje.emit(label_personaje)        

    def enviar_actualizacion_tablero(self):
        '''
        Este método se encargará de leer el progreso de la partida
        cuando es llamado y enviar la información al frontend 
        mediante la señal senal_enviar_actualizacion_tablero.
        A diferencia de cargar tablero, este sólo cambia lo que varía
        dentro del juego
        '''

    def pausa_juego(self):
        '''
        Este método se encarga de, cuando es llamado,
        reanudar el juego si está pausado y pausarlo si no 
        mediante la señal senal_enviar_actualizacion_tablero.
        Además cambia el botón de pausa
        '''
        

    def salir_juego(self):
        '''
        Este método se encarga de, cuando es llamado,
        salir del juego y llevar a la ventana post ronda
        '''

    def cheats(self, teclas):
        '''
        Comprueba si se ejecutó algún cheat, y los ejecuta
        '''

if __name__ == "__main__":
    app = QApplication([])
    ventana_juego = VentanaJuego()
    logica_juego = LogicaVentanaJuego()
    ventana_juego.senal_pausa_juego.connect(logica_juego.pausa_juego)
    ventana_juego.senal_salir_juego.connect(logica_juego.salir_juego)
    ventana_juego.senal_tecla_presionada.connect(logica_juego.tecla_presionada)
    logica_juego.senal_cambiar_pos_personaje.connect(ventana_juego.mover_personaje)
    logica_juego.senal_orientacion_personaje.connect(ventana_juego.personaje.recibidor_de_mover)
    sys.exit(app.exec())