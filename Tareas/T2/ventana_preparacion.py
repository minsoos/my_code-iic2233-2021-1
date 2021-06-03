from PyQt5 import uic
import parametros as p
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar, QMessageBox
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
from time import time
from ventana_juego import VentanaJuego, LogicaVentanaJuego

nombre_preparacion, padre_preparacion = uic.loadUiType(p.DISENO_VENTANA_PREPARACION)
nombre_error, padre_error = uic.loadUiType(p.DISENO_VENTANA_MAPA_ERRADO)


class VentanaPreparacion(nombre_preparacion, padre_preparacion):

    senal_iniciar_nueva_partida = pyqtSignal()
    senal_solicitud_cambiar_personaje = pyqtSignal(str)
    senal_tecla_presionada_mover = pyqtSignal(str)
    senal_solicitud_entrar_edificio = pyqtSignal(str, str)

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
        self.tamano_ventana = (self.height(), self.width())
        # Configuración de labels del archivo ui
        self.dic_paths = p.RUTAS_VENTANA_PREPARACION
        self.label_boton_lisa.setPixmap(QPixmap(self.dic_paths["lisa"]))
        self.label_boton_homero.setPixmap(QPixmap(self.dic_paths["homero"]))
        self.label_boton_moe.setPixmap(QPixmap(self.dic_paths["moe"]))
        self.label_boton_krusty.setPixmap(QPixmap(self.dic_paths["krusty"]))
        self.label_logo.setPixmap(QPixmap(self.dic_paths["logo"]))
        self.label_fondo.setPixmap(QPixmap(self.dic_paths["fondo"]))
        self.cargar_edificios()
        # Label personaje
        self.label_personaje = QLabel(self)
        self.label_personaje.setGeometry(*p.POSICION_INICIAL_VENTANA_PREPARACION, 20, 40)
        self.label_personaje.setScaledContents(True)
        self.nombre_personaje = None
        #nombre personaje
        self.label_personaje.show()
        #
        self.configuracion_radio_buttons()
        #
        self.setFocusPolicy(Qt.StrongFocus)
        # Fuente: https://programtalk.com/python-examples/PyQt5.QtCore.Qt.StrongFocus/

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
        print("solicitaste cambiar el personaje")
        self.label_personaje.show()
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
    
    # ------------------ Desde aquí se trabajan las señales recibidas y dadas
    # ------------------ para la actualización del label de personaje

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
        try:
            if tecla in "asdw":
                self.senal_tecla_presionada_mover.emit(tecla)
        except TypeError:
            pass

    def actualizar_movimiento_personaje(self, posicion):
        self.label_personaje.move(*posicion)
        self.posibilidad_entrar_a_juego()

    def actualizar_animacion_personaje(self, path_dado):
        pixeles = QPixmap(path_dado)
        self.label_personaje.setPixmap(pixeles)

    def posibilidad_entrar_a_juego(self):
        '''
        Este método se llama cuando el personaje está en un
        lugar de juego. Si está en el que le corresponde, debe
        avanzar a la ventana de juego. De lo contrario, un label
        debe avisar que ese lugar no le corresponde
        '''
        for edificio in self.edificios:
            rect_pers = self.label_personaje.geometry()
            rect_edif = self.edificios[edificio].geometry()
            if rect_pers.intersects(rect_edif):
                a = str(self.dificultad.currentText()).lower()
                print(a)
                self.senal_solicitud_entrar_edificio.emit(edificio, a)
    
    def ocultar_ventana(self, respuesta):
        if respuesta:
            self.hide()
            self.label_personaje.move(*p.POSICION_INICIAL_VENTANA_PREPARACION)

    def mostrar_ventana(self):
        self.show()


class VentanaMapaErrado(nombre_error, padre_error):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Mapa errado")
        self.label_estrangulacion.setPixmap(QPixmap(p.RUTA_ESTRANGULACION))
        self.boton_volver.clicked.connect(self.metodo_volver)
        self.tiempo_antiguo = time()

    def mostrar(self):
        tiempo_nuevo = time()
        if tiempo_nuevo - self.tiempo_antiguo > 5:
            self.tiempo_antiguo = tiempo_nuevo
            self.show()
    
    def metodo_volver(self):
        self.hide()


class LogicaVentanaPreparacion(QObject):

    senal_actualizar_info_ventana = pyqtSignal(int, int, int, int, int)
    # Se envía número de ronda, puntaje acumulado, ítems buenos, malos y vida; en ese orden
    senal_actualizar_animacion_personaje = pyqtSignal(str)
    senal_actualizar_movimiento_personaje = pyqtSignal(tuple)
    senal_ocultar_ventana = pyqtSignal(bool)
    senal_abrir_ventana_juego = pyqtSignal(str, Personaje, int, str)
    # Se envía edificio, personaje, número de ronda y dificultad; en ese orden
    senal_abrir_ventana_error = pyqtSignal()
    senal_mostrar_ventana = pyqtSignal()

    def __init__(self) -> None:
        '''
        Backend de VentanaPreparacion. Aquí se cargan los
        valores de los parámetros correspondientes, además,
        maneja la entrada y salida de esta ventana
        '''
        super().__init__()
        self.dificultad = "intro"

    def iniciar_nueva_partida(self, nombre):
        self.nombre_de_usuario = nombre
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

    # --------------------------- Aquí termina la inicialización
    # --------------------------- Aquí empieza la actualización de info y parámetros

    def actualizar_info_ventana(self):
        a = self.numero_de_ronda
        b = self.puntaje_acumulado
        c = self.items_buenos
        d = self.items_malos
        e = self.personaje_actual.vida*100
        self.senal_actualizar_info_ventana.emit(a, b, c, d, e)

    def cambiar_personaje(self, personaje):
        personaje = self.personajes[personaje]
        if not self.personaje_actual is None:
            # Acá paramos el QTimer del personaje anterior
            self.personaje_actual.timer.stop()
        self.personaje_actual = personaje
        self.inicializar_mapa_en_personaje()
        self.actualizar_info_ventana()
        self.personaje_actual.timer.start()
    
    def inicializar_mapa_en_personaje(self):
        '''
        Le da los argumentos del mapa a personaje
        '''
        a = p.RECTANGULO_TABLERO_PREPARACION
        b = self.posicion_personaje
        c = self.dificultad
        self.personaje_actual.inicializador_de_mapa("preparacion", a, b, c)

    # ------------------------------------ Desde acá se actualiza al label (moverse/animación)

    def movimiento_de_personaje_solicitado(self, tecla):
        # --------------------acoplado
        if self.personaje_actual is not None:
            self.personaje_actual.recibidor_de_mover(tecla)

    def animacion_de_personaje(self, path_dado):
        self.senal_actualizar_animacion_personaje.emit(path_dado)

    def movimiento_de_personaje(self, posicion_nueva):
        self.posicion_personaje = posicion_nueva
        self.senal_actualizar_movimiento_personaje.emit(posicion_nueva)

    # ----------------------------------- Desde acá se revisa la entrada a edificios

    def revision_solicitud_entrada_a_edificio(self, edificio, dificultad):
        if edificio == "primaria" and self.personaje_actual.nombre == "lisa" or\
            edificio == "planta" and self.personaje_actual.nombre == "homero" or\
            edificio == "bar" and self.personaje_actual.nombre == "moe" or\
            edificio == "krustyland" and self.personaje_actual.nombre == "krusty":
            puede = True
        else:
            puede = False
        if puede:
            self.entrar_a_juego(edificio, dificultad)
        else:
            self.senal_abrir_ventana_error.emit()

    def entrar_a_juego(self, edificio, dificultad):
        self.senal_ocultar_ventana.emit(True)
        for personaje in self.personajes:
            persona = self.personajes[personaje]
            persona.senal_mover_personaje.disconnect()
            persona.senal_actualizar_animacion.disconnect()
        a = edificio
        b = self.personaje_actual
        c = self.numero_de_ronda
        d = dificultad
        self.senal_abrir_ventana_juego.emit(a, b, c, d)
    
    # ----------------------------------- Otros

    def cheat_aumentar_vida(self, teclas):
        '''
        Comprueba si se ejecutó el cheat de aumentar vida
        y lo ejecuta
        '''
    # ---------------------------------- Volver a ventana
    def volver_a_ventana(self, puntaje, i_buenos, i_malos):
        self.numero_de_ronda += 1
        self.puntaje_acumulado += puntaje
        self.items_buenos += i_buenos
        self.items_malos += i_malos
        self.posicion_personaje = p.POSICION_INICIAL_VENTANA_PREPARACION
        self.inicializar_mapa_en_personaje()
        #
        a = self.numero_de_ronda
        b = self.puntaje_acumulado
        c = self.items_buenos
        d = self.items_malos
        e = self.personaje_actual.vida * 100
        self.senal_actualizar_info_ventana.emit(a, b, c, d, e)
        # Esto es para "iniciar al personaje" artificialmente, se mueve un espacio hacia arriba
        self.movimiento_de_personaje_solicitado("w")
        self.senal_mostrar_ventana.emit()
        self.conexiones()
    
    def guardar_y_salir(self, puntaje, i_buenos, i_malos):
        self.volver_a_ventana(puntaje, i_buenos, i_malos)
        self.senal_ocultar_ventana.emit(True)
        self.escribir_ranking()
    
    def escribir_ranking(self):
        with open(p.RUTA_RANKING, "a", encoding="UTF-8") as archivo:
            archivo.write(f"\n{self.nombre_de_usuario},{self.puntaje_acumulado}")



def hook(type_error, traceback):
    print(type_error)
    print(traceback)

open("ranking.txt", "a")

if __name__ == "__main__":
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    ventana_preparacion = VentanaPreparacion()
    logica_ventana_preparacion = LogicaVentanaPreparacion()
    ventana_mapa_errado = VentanaMapaErrado()
    # Señales
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
    conexion_n = ventana_preparacion.ocultar_ventana
    logica_ventana_preparacion.senal_ocultar_ventana.connect(conexion_n)
    conexion_n = logica_ventana_preparacion.revision_solicitud_entrada_a_edificio
    ventana_preparacion.senal_solicitud_entrar_edificio.connect(conexion_n)
    logica_ventana_preparacion.senal_abrir_ventana_error.connect(ventana_mapa_errado.mostrar)
    logica_ventana_preparacion.senal_mostrar_ventana.connect(ventana_preparacion.mostrar_ventana)
    # ---------------------------- Ventana juego
    ventana_juego = VentanaJuego()
    logica_juego = LogicaVentanaJuego()
    logica_ventana_preparacion.senal_abrir_ventana_juego.connect(logica_juego.abrir_juego)
    ventana_juego.senal_pausa_juego.connect(logica_juego.pausa_juego)
    ventana_juego.senal_salir_juego.connect(logica_juego.salir_juego)
    ventana_juego.senal_tecla_presionada_cheat.connect(logica_juego.cheats)
    logica_juego.senal_generar_objeto.connect(ventana_juego.recibir_objeto)
    ventana_juego.senal_pedir_objeto.connect(logica_juego.generar_objeto)
    #Esto lo hice hoy, 29/05/21
    logica_juego.senal_inicializar_ventana.connect(ventana_juego.inicializar)
    logica_juego.senal_dar_obstaculos.connect(ventana_juego.crear_obstaculos)
    ventana_juego.senal_pedir_crear_obstaculos.connect(logica_juego.generar_obstaculos)
    ventana_juego.senal_objeto_tocado.connect(logica_juego.objeto_tocado)
    logica_juego.senal_desaparecer_objeto.connect(ventana_juego.desaparecer_objeto)
    logica_juego.senal_enviar_actualizacion_tablero.connect(ventana_juego.actualizar_tablero)
    logica_juego.senal_pasar_tiempo.connect(ventana_juego.pasar_tiempo)
    logica_juego.senal_esconder_ventana.connect(ventana_juego.esconder_ventana)

    logica_ventana_preparacion.iniciar_nueva_partida()

    sys.exit(app.exec())