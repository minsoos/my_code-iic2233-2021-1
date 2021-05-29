from PyQt5 import uic
import parametros as p
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QEventLoop, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QMovie, QFont
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QLineEdit, QRadioButton, QSpinBox, QCheckBox, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
import sys
import parametros as p
from personajes import Gorgory, Homero, Lisa, Moe, Krusty, Personaje
from os import path
from random import randint

nombre, padre = uic.loadUiType(p.DISENO_VENTANA_PREPARACION)


class VentanaPreparacion(nombre, padre):

    senal_iniciar_nueva_partida = pyqtSignal()
    senal_solicitud_cambiar_personaje = pyqtSignal(str)
    senal_tecla_presionada_mover = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        '''
        Front end de la ventana donde el jugador puede elegir
        su personaje (por defecto viene homero), además de su
        dificultad. Además puede ver cómo va el avance de su
        juego en curso, ver su vida, puntaje, items buenos y
        malos recogidos y rondas superadas.
        En este mismo, el jugador se puede mover a lo largo
        del mapa, donde cada personaje, si se desplaza hacia
        su tablero, entrará a la ventana de juego
        '''
        #QLabel logo
        #QSpinBox para dificultad
        #QLabel para número de ronda
        #Qlabel para puntaje
        #QLabel para ítems malos
        #QLabel para ítems buenos
        #QLabel para vida, intentando crear una barra
        #QPixmap con fondo de imagen de springfield
        #QLabel del personaje
        #QPushButton salir del juego
        self.tamano_ventana = (self.height(), self.width())
        # Configuración de labels del archivo ui
        self.dic_paths = p.RUTAS_VENTANA_PREPARACION
        self.label_boton_lisa.setPixmap(QPixmap(self.dic_paths["lisa"]))
        self.label_boton_homero.setPixmap(QPixmap(self.dic_paths["homero"]))
        self.label_boton_moe.setPixmap(QPixmap(self.dic_paths["moe"]))
        self.label_boton_krusty.setPixmap(QPixmap(self.dic_paths["krusty"]))
        self.label_logo.setPixmap(QPixmap(self.dic_paths["logo"]))
        self.label_fondo.setPixmap(QPixmap(self.dic_paths["fondo"]))
        # Label personaje
        self.label_personaje = QLabel(self)
        self.label_personaje.setGeometry(*p.POSICION_INICIAL_VENTANA_PREPARACION, 20, 40)
        self.label_personaje.setScaledContents(True)
        self.label_personaje.show()
        #
        self.cargar_edificios()
        self.configuracion_radio_buttons()
        
    
    def cargar_edificios(self):
        self.edificios = dict()
        x = 50
        y = 430
        for i in ("planta", "primaria", "bar", "krustyland"):
            label = QLabel(self)
            label.setPixmap(QPixmap(self.dic_paths[i]))
            label.setScaledContents(True)
            label.setGeometry(0, 0, 130, 100)
            label.move(x, y)
            x += 230
            self.edificios[i] = label

    def configuracion_radio_buttons(self):
        self.boton_homero.toggled.connect(self.solicitud_cambiar_personaje)
        self.boton_lisa.toggled.connect(self.solicitud_cambiar_personaje)
        self.boton_moe.toggled.connect(self.solicitud_cambiar_personaje)
        self.boton_krusty.toggled.connect(self.solicitud_cambiar_personaje)

    # -------------------- Hasta aquí llega la inicialización

    def actualizar_info(self, ronda, puntaje, i_buenos, i_malos, vida):
        '''
        Actualiza los parámetros cada vez que es llamado
        '''
        self.label_puntaje.setText(f"{puntaje}")
        self.label_ronda.setText(f"{ronda}")
        self.label_items_buenos.setText(f"{i_buenos}")
        self.label_items_malos.setText(f"{i_malos}")
        self.barra_vida.setValue(vida)
        self.show()

    # ------------------- Desde aquí se trabaja el cambio de personaje

    def solicitud_cambiar_personaje(self):
        if self.boton_homero.isChecked():
            self.senal_solicitud_cambiar_personaje.emit("homero")
        elif self.boton_lisa.isChecked():
            self.senal_solicitud_cambiar_personaje.emit("lisa")
        elif self.boton_moe.isChecked():
            self.senal_solicitud_cambiar_personaje.emit("moe")
        elif self.boton_krusty.isChecked():
            self.senal_solicitud_cambiar_personaje.emit("krusty")
        else:
            raise ValueError("el boton apretado no ta")
    
    # ------------------ Desde aquí se trabajan las señales recibidas para
    # ------------------ la actualización del label de personaje

    def keyPressEvent(self, tecla):
        '''
        Envía señal a tecla_presionada
        '''
        if tecla.key() == Qt.Key_A:
            tecla = "a"
        elif tecla.key() == Qt.Key_D:
            tecla = "d"
        elif tecla.key() == Qt.Key_S:
            tecla = "s"
        elif tecla.key() == Qt.Key_W:
            tecla = "w"
        if tecla in "asdw":
            self.senal_tecla_presionada_mover.emit(tecla)

    def actualizar_movimiento_personaje(self, posicion):
        self.label_personaje.move(*posicion)


    def actualizar_animacion_personaje(self, path_dado):
        print("está actualizando")
        pixeles = QPixmap(path_dado)
        self.label_personaje.setPixmap(pixeles)
    
    

    def entrar_a_juego(self):
        '''
        Este método se llama cuando el personaje está en un
        lugar de juego. Si está en el que le corresponde, debe
        avanzar a la ventana de juego. De lo contrario, un label
        debe avisar que ese lugar no le corresponde
        '''
        pass


class LogicaVentanaPreparacion(QObject):

    senal_actualizar_info_ventana = pyqtSignal(int, int, int, int, int)
    # Se envía número de ronda, puntaje acumulado, ítems buenos, malos y vida; en ese orden
    senal_actualizar_animacion_personaje = pyqtSignal(str)
    senal_actualizar_movimiento_personaje = pyqtSignal(tuple)

    def __init__(self) -> None:
        '''
        Backend de VentanaPreparacion. Aquí se cargan los
        valores de los parámetros correspondientes, además,
        maneja la entrada y salida de esta ventana
        '''
        super().__init__()

    def iniciar_nueva_partida(self):
        self.numero_de_ronda = 1
        self.puntaje_acumulado = 0
        self.items_buenos = 0
        self.items_malos = 0
        self.personaje_actual = None
        self.posicion_personaje = p.POSICION_INICIAL_VENTANA_PREPARACION
        self.personajes = {
            "homero": Homero(),
            "lisa": Lisa(),
            "moe": Moe(),
            "krusty": Krusty()
        }
        self.senal_actualizar_info_ventana.emit(1, 0, 0, 0, 0)
        self.conexiones()
    
    def conexiones(self):
        for personaje in self.personajes:
            persona = self.personajes[personaje]
            persona.senal_mover_personaje.connect(self.movimiento_de_personaje)
            persona.senal_actualizar_animacion.connect(self.animacion_de_personaje)

    def actualizar_info_ventana(self):
        a = self.numero_de_ronda
        b = self.puntaje_acumulado
        c = self.items_buenos
        d = self.items_malos
        e = self.personaje_actual.vida
        self.senal_actualizar_info_ventana.emit(a, b, c, d, e)

    def cheat_aumentar_vida(self, teclas):
        '''
        Comprueba si se ejecutó el cheat de aumentar vida
        y lo ejecuta
        '''
    
    def cambiar_personaje(self, personaje):
        personaje = self.personajes[personaje]
        if not self.personaje_actual is None:
            self.personaje_actual.timer.stop()
        self.personaje_actual = personaje
        self.personaje_actual.posicion = self.posicion_personaje
        self.actualizar_info_ventana()
        self.personaje_actual.timer.start()
    
    def movimiento_de_personaje_solicitado(self, tecla):
        # --------------------acoplado
        self.personaje_actual.recibidor_de_mover(tecla)

    def animacion_de_personaje(self, path_dado):
        self.senal_actualizar_animacion_personaje.emit(path_dado)

    def movimiento_de_personaje(self, posicion_nueva):
        print("backend intentando mover")
        print(posicion_nueva)
        self.posicion_personaje = posicion_nueva
        self.senal_actualizar_movimiento_personaje.emit(posicion_nueva)

def hook(type_error, traceback):
    print(type_error)
    print(traceback)

open("ranking.txt", "a")

if __name__ == "__main__":
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    ventana_preparacion = VentanaPreparacion()
    logica_ventana_preparacion = LogicaVentanaPreparacion()
    # Señales
    conexion_n = logica_ventana_preparacion.iniciar_nueva_partida
    conexion_n = ventana_preparacion.actualizar_info
    logica_ventana_preparacion.senal_actualizar_info_ventana.connect(conexion_n)
    conexion_n = logica_ventana_preparacion.cambiar_personaje
    ventana_preparacion.senal_solicitud_cambiar_personaje.connect(conexion_n)
    conexion_n = ventana_preparacion.actualizar_animacion_personaje
    logica_ventana_preparacion.senal_actualizar_animacion_personaje.connect(conexion_n)
    conexion_n = ventana_preparacion.actualizar_movimiento_personaje
    logica_ventana_preparacion.senal_actualizar_movimiento_personaje.connect(conexion_n)
    conexion_n = logica_ventana_preparacion.movimiento_de_personaje_solicitado
    ventana_preparacion.senal_tecla_presionada_mover.connect(conexion_n)
    logica_ventana_preparacion.iniciar_nueva_partida()

    sys.exit(app.exec())