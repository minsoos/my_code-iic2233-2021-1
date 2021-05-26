from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QEventLoop, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QMovie, QFont
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QLineEdit, QRadioButton, QSpinBox, QCheckBox, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
import sys
import parametros as p
from personajes import Homero, Lisa, Moe, Krusty
from os import path
from random import randint

class VentanaJuego(QWidget):

    senal_pausa_juego = pyqtSignal()
    senal_salir_juego = pyqtSignal()
    senal_tecla_presionada_mover = pyqtSignal(str)
    senal_tecla_presionada_cheat = pyqtSignal(str)
    senal_pedir_objeto = pyqtSignal()

    def __init__(self, personaje_ingresado=Krusty()):
        super().__init__()
        # Atributos de la ventana
        self.tamano_ventana = (900, 700)
        self.personaje = personaje_ingresado
        self.rutas_personajes = p.RUTAS_PERSONAJES
        self.rutas_imagenes = p.RUTAS_IMAGENES_JUEGO
        self.__posicion_personaje = (0, 0)
        self.orientacion_personaje = "up"
        self.posiciones_obstaculos = set()
        self.lista_objetos = []
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
        Cambia la posición del personaje y revisa si topa con un objeto
        '''
        self.__posicion_personaje = lugar
        self.__label_personaje.move(*lugar)
        self.personaje.label_personaje = self.__label_personaje
        rect_personaje = self.__label_personaje.geometry()
        posicion_sacar = None
        for indice, objeto in enumerate(self.lista_objetos):
            rect_obj = objeto.geometry()
            if rect_personaje.intersects(rect_obj):
                posicion_sacar = indice
                objeto_sacado = objeto
        if not posicion_sacar is None:
            self.lista_objetos.pop(posicion_sacar)
            objeto_sacado.hide()
            print("EEEEEEH SUMASTE UN PUNTO")



    def mover_personaje(self, lugar):
        self.posicion_personaje = lugar

    def keyPressEvent(self, tecla):
        '''
        Envía señal a tecla_presionada
        '''
        tecla = "w" if tecla.key() == Qt.Key_W else "s" if tecla.key() == Qt.Key_S \
            else "d" if tecla.key() == Qt.Key_D  else "a" if tecla.key() == Qt.Key_A else "nada"
        if tecla in "asdw":
            if tecla == "a":
                self.orientacion_personaje = "left"
            elif tecla == "d":
                self.orientacion_personaje = "right"
            elif tecla == "s":
                self.orientacion_personaje = "down"
            elif tecla == "w":
                self.orientacion_personaje = "right"
            self.senal_tecla_presionada_mover.emit(tecla)
        else:
            self.senal_tecla_presionada_cheat.emit(tecla)

    def conexiones(self):
        self.personaje.senal_actualizar_animacion.connect(self.actualizar_personaje)
        self.personaje.senal_mover_personaje.connect(self.mover_personaje)
        self.senal_tecla_presionada_mover.connect(self.personaje.recibidor_de_mover)

    def recibir_objeto(self, path_, posicion):
        objeto_auxiliar = QLabel(self)
        print(path_)
        objeto_auxiliar.setPixmap(QPixmap(path_))
        objeto_auxiliar.setGeometry(*posicion, 30, 40)
        objeto_auxiliar.setScaledContents(True)
        rect_aux = objeto_auxiliar.geometry()
        algo_intersectado = False
        for cosa in (self.obstaculos + self.lista_objetos):
            rect_cosa = cosa.geometry()
            if rect_aux.intersects(rect_cosa):
                algo_intersectado = True
                break
        if algo_intersectado:
            self.senal_pedir_objeto.emit()
        else:
            self.lista_objetos.append(objeto_auxiliar)
            print("añadíiiii", path_, self.lista_objetos)
            objeto_auxiliar.show()

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

        #agregar datos
        contenedor_info_superior.addStretch()
        contenedor_info_inferior.addStretch()
        contenedor_info_superior.addWidget(self.label_vida)
        contenedor_info_superior.addStretch()
        contenedor_info_inferior.addWidget(self.label_tiempo)
        contenedor_info_inferior.addStretch()
        contenedor_info_superior.addWidget(self.label_items_buenos)
        contenedor_info_superior.addStretch()
        contenedor_info_inferior.addWidget(self.label_items_malos)
        contenedor_info_inferior.addStretch()
        contenedor_info_superior.addWidget(self.label_ronda)
        contenedor_info_superior.addStretch()
        contenedor_info_inferior.addWidget(self.label_puntaje)
        contenedor_info_inferior.addStretch()
        contenedor_info_superior.addWidget(self.boton_pausar)
        contenedor_info_superior.addStretch()
        contenedor_info_inferior.addWidget(self.boton_salir)
        contenedor_info_inferior.addStretch()
        contenedor_info_superior.addStretch()
        #Terminar layout superior (barra de progreso)
        #Añadimos el layout
        contenedor_info.addLayout(contenedor_info_superior)
        contenedor_info.addLayout(contenedor_info_inferior)
        #ks
        contenedor_info_y_logo.addWidget(self.label_logo)
        contenedor_info_y_logo.addLayout(contenedor_info)
        #Terminar layout principal
        layout_principal.addStretch()
        layout_principal.addLayout(contenedor_info_y_logo)
        layout_principal.addWidget(self.mapa)
        layout_principal.addStretch()
        self.setLayout(layout_principal)
        #Esto le da al personaje los bordes del mapa
        #self.personaje.rectangulo_juego = self.mapa.geometry()
        #print(self.mapa.geometry())
        #print("jaja",self.mapa.x())
        #
        self.init_gui_objetos_y_personaje()
    
    def init_gui_objetos_y_personaje(self):
        self.crear_obstaculos()
        #Personaje
        self.__label_personaje = QLabel(self)
        if self.personaje.nombre in self.rutas_personajes.keys():
            ruta_inicial = self.rutas_personajes[self.personaje.nombre]
            pixeles = QPixmap(path.join(ruta_inicial, "up_3.png"))
            self.__label_personaje.setPixmap(pixeles)
            self.__label_personaje.setGeometry(0,0,30,50)
            self.__label_personaje.setScaledContents(True)
            puede_pasar = False
            while not puede_pasar:
                nueva_pos = (randint(0,self.tamano_ventana[0]),\
                    randint(300, self.tamano_ventana[1]))
                self.posicion_personaje = nueva_pos
                obstaculizado = False
                lugar_personaje = self.__label_personaje.geometry()
                for obstaculo in self.obstaculos:
                    lugar_obstaculo = obstaculo.geometry()
                    if lugar_obstaculo.intersects(lugar_personaje):
                        obstaculizado = True
                if not obstaculizado:
                    puede_pasar = True
            self.personaje.posicion = self.posicion_personaje
            self.personaje.label_personaje = self.__label_personaje
            self.personaje.timer.start()
        else:
            raise ValueError("Este personaje no existe")
        
    def crear_obstaculos(self):
        # ------------------Obstaculos
        rutas_obstaculos = p.RUTAS_OBSTACULOS_PLANTA
        self.obstaculos = list()
        for i in range(3):
            misma_posicion = True
            while misma_posicion:
                misma_posicion = False
                posicion_i = (randint(10, 860), randint(290, 290+460))
                for obstaculo_comparativo in self.obstaculos:
                    if (obstaculo_comparativo.x()-posicion_i[0])**2 <= 160**2 and\
                        (obstaculo_comparativo.y()-posicion_i[1])**2 <= 160**2:
                        misma_posicion = True
            label_obstaculon = QLabel(self)
            pixeles = QPixmap(rutas_obstaculos[str(i+1)])
            print(rutas_obstaculos[str(i+1)])
            label_obstaculon.setPixmap(pixeles)
            label_obstaculon.setScaledContents(True)
            label_obstaculon.setGeometry(*posicion_i, 30, 40)
            self.obstaculos.append(label_obstaculon)
        self.personaje.labels_obstaculos = self.obstaculos

class LogicaVentanaJuego(QObject):

    senal_enviar_actualizacion_tablero = pyqtSignal()
    senal_cargar_tablero = pyqtSignal()
    senal_cambiar_boton_pausa = pyqtSignal()
    senal_cambiar_pos_personaje = pyqtSignal(str)
    senal_generar_objeto = pyqtSignal(str, tuple)
    # Generador de objetos
    def __init__(self, rectangulo_mapa = (10,290,850,460)) -> None:
        super().__init__()
        '''
        Este es el backend de la ventana juego, y se encarga de
        realizar los procesos de esta
        '''
        self.generador_de_objetos = QTimer()
        self.generador_de_objetos.timeout.connect(self.generar_objeto)
        self.generador_de_objetos.setInterval(1000*10)
        self.generador_de_objetos.start()
        self.ruta_objetos = p.RUTAS_OBJETOS_PLANTA
        self.rectangulo_mapa = rectangulo_mapa

    def cargar_juego(self):
        '''
        Este método se encargará de leer el progreso de la partida
        cuando es llamado, y enviar la información al frontend 
        mediante la señal senal_enviar_actualizacion_tablero
        Además carga los objetos
        '''

    def generar_objeto(self):
        '''
        Este método genera un objeto cuando lo llama
        el QTimer o el frontend
        '''
        x = randint(self.rectangulo_mapa[0], self.rectangulo_mapa[0] + self.rectangulo_mapa[2])
        y = randint(self.rectangulo_mapa[1], self.rectangulo_mapa[1] + self.rectangulo_mapa[3])
        path_objeto = self.ruta_objetos["dona"]
        print(path_objeto)
        self.senal_generar_objeto.emit(path_objeto, (x, y))


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
        pass

if __name__ == "__main__":
    app = QApplication([])
    ventana_juego = VentanaJuego()
    logica_juego = LogicaVentanaJuego()
    ventana_juego.senal_pausa_juego.connect(logica_juego.pausa_juego)
    ventana_juego.senal_salir_juego.connect(logica_juego.salir_juego)
    logica_juego.senal_cambiar_pos_personaje.connect(ventana_juego.personaje.moverse)
    ventana_juego.senal_tecla_presionada_cheat.connect(logica_juego.cheats)
    logica_juego.senal_generar_objeto.connect(ventana_juego.recibir_objeto)
    ventana_juego.senal_pedir_objeto.connect(logica_juego.generar_objeto)
    sys.exit(app.exec())