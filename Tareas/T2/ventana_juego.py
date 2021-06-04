from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QEventLoop, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QMovie, QFont
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QLineEdit, QRadioButton, QSpinBox, QCheckBox, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
import sys
import parametros as p
from personajes import Personaje, Homero, Lisa, Moe, Gorgory, Krusty
from os import path
from random import randint
from PyQt5 import uic
import funciones as f
from ventana_postronda import VentanaPostRonda, LogicaVentanaPostRonda
from time import time
from collections import deque

nombre, padre = uic.loadUiType(p.DISENO_VENTANA_JUEGO)


class VentanaJuego(nombre, padre):

    senal_pausa_juego = pyqtSignal()
    senal_salir_juego = pyqtSignal()
    senal_tecla_presionada_mover = pyqtSignal(str)
    senal_tecla_presionada_cheat = pyqtSignal(str)
    senal_pedir_objeto = pyqtSignal()
    senal_pedir_crear_obstaculos = pyqtSignal()
    senal_objeto_tocado = pyqtSignal(int)
    senal_personaje_movido = pyqtSignal(tuple)
    senal_acabar_juego = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Atributos de la ventana
        self.tamano_ventana = (self.height, self.width)
        self.personaje = None
        self.rutas_personajes = p.RUTAS_PERSONAJES
        self.rutas_imagenes = p.RUTAS_IMAGENES_JUEGO
        self.__posicion_personaje = (0, 0)
        self.lista_objetos = []
        self.obstaculos = []
        self.rectangulo_mapa = p.RECTANGULO_TABLERO_JUEGO
        # Dar propiedades a la ventana
        self.setWindowTitle("Ventana de Juego")
        self.label_personaje = QLabel(self)
        self.label_gorgory = QLabel(self)
        self.label_gorgory.setScaledContents(True)

        self.init_gui()

    def init_gui(self):
        """
        Crea la interfaz de la ventana
        """
        # ---- Definicion de la barra superior ----
        
        # Logo superior izq
        pixeles = QPixmap(self.rutas_imagenes['logo'])
        self.label_logo.setPixmap(pixeles)
        self.label_logo.setScaledContents(True)
        #botones-------------------------------
        #Boton_pausar
        self.boton_pausar.clicked.connect(self.metodo_boton_pausar)
        #Boton_salir
        self.boton_salir.clicked.connect(self.metodo_boton_salir)
        

    # --------------------- Desde acá, se empieza a inicializar la ventana
    # --------------------- configurándola de acuerdo a cómo sea llamada
    
    def inicializar(self, edificio, personaje, n_ronda, dificultad, tiempo):
        '''
        Este método termina de inicializar la ventana cuando se llama,
        además, la muestra
        '''
        self.personaje = personaje
        self.edificio = edificio
        self.label_ronda.setText(str(n_ronda))
        self.dificultad = dificultad
        self.pausa = False
        self.label_items_buenos.setText("0")
        self.label_items_malos.setText("0")
        self.label_puntaje.setText("0")
        self.senal_pedir_crear_obstaculos.emit()
        self.cargar_datos(tiempo)
        self.label_gorgory.setGeometry(-300, -300, 30, 50)
        self.antepenultima_letra = "z"
        self.penultima_letra = "z"
        self.ultima_letra = "z"
    
    def cargar_datos(self, tiempo):
        #Mapa por el que se mueve el jugador
        self.label_mapa.setPixmap(QPixmap(self.rutas_imagenes[f"mapa_{self.edificio}"]))
        # Vida del personaje
        self.barra_vida.setValue(self.personaje.vida * 100)
        # Barra tiempo
        self.barra_tiempo.setRange(0, tiempo)
        self.barra_tiempo.setValue(tiempo)

        
    def crear_obstaculos(self, lista):
        for ruta, posicion in lista:
            label_obstaculo_n = QLabel(self)
            label_obstaculo_n.setPixmap(QPixmap(ruta))
            label_obstaculo_n.setScaledContents(True)
            label_obstaculo_n.setGeometry(*posicion, 30, 40)
            self.obstaculos.append(label_obstaculo_n)
        self.personaje.labels_obstaculos = self.obstaculos
        self.init_gui_objetos_y_personaje()

    def init_gui_objetos_y_personaje(self):
        #Personaje
        if self.personaje.nombre in self.rutas_personajes.keys():
            ruta_inicial = self.rutas_personajes[self.personaje.nombre]
            pixeles = QPixmap(path.join(ruta_inicial, "up_3.png"))
            self.label_personaje.setPixmap(pixeles)
            self.label_personaje.setGeometry(0, 0, 30, 50)
            self.label_personaje.setScaledContents(True)
            #label configurado, ahora vemos la posición
            puede_pasar = False
            r = self.rectangulo_mapa
            while not puede_pasar:
                nueva_pos = (randint(r[0], r[0] + r[2]), randint(r[1], r[1] + r[3]))
                self.posicion_personaje = nueva_pos
                obstaculizado = False
                lugar_personaje = self.label_personaje.geometry()
                for obstaculo in self.obstaculos:
                    lugar_obstaculo = obstaculo.geometry()
                    if lugar_obstaculo.intersects(lugar_personaje):
                        obstaculizado = True
                if not obstaculizado:
                    puede_pasar = True
            self.personaje.posicion = self.posicion_personaje
            self.personaje.label_personaje = self.label_personaje
            self.personaje.timer.start()
        else:
            raise ValueError("Este personaje no existe")
        self.conexiones()
        self.show()

    def conexiones(self):
        self.personaje.senal_actualizar_animacion.connect(self.actualizar_personaje)
        self.personaje.senal_mover_personaje.connect(self.mover_personaje)
        self.senal_tecla_presionada_mover.connect(self.personaje.recibidor_de_mover)

    # ----------------- Aquí termina la pseudo inicialización
    def esconder_ventana(self):
        self.hide()
        self.desconexiones()
        for obstaculo in self.obstaculos:
            obstaculo.hide()
        for objeto in self.lista_objetos:
            try:
                objeto.hide()
            except AttributeError:
                pass
        self.obstaculos = []
        self.lista_objetos = []
        
    def desconexiones(self):
        self.personaje.senal_actualizar_animacion.disconnect()
        self.personaje.senal_mover_personaje.disconnect()
        self.senal_tecla_presionada_mover.disconnect()

    @property
    def posicion_personaje(self):
        return self.__posicion_personaje

    @posicion_personaje.setter
    def posicion_personaje(self, lugar):
        '''
        Cambia la posición del personaje y revisa si topa con un objeto
        '''
        self.__posicion_personaje = lugar
        self.label_personaje.move(*lugar)
        self.senal_personaje_movido.emit(lugar)
        self.personaje.label_personaje = self.label_personaje
        rect_personaje = self.label_personaje.geometry()
        posicion_sacar = None
        
        for indice, objeto in enumerate(self.lista_objetos):
            if objeto is not None:
                rect_obj = objeto.geometry()
                if rect_personaje.intersects(rect_obj):
                    posicion_sacar = indice
                    objeto_sacado = objeto
                    break
        if posicion_sacar is not None:
            objeto_sacado.hide()
            self.lista_objetos[posicion_sacar] = None
            self.senal_objeto_tocado.emit(posicion_sacar)
        rect_gorgory = self.label_gorgory.geometry()
        if rect_personaje.intersects(rect_gorgory):
            self.senal_acabar_juego.emit()



    def mover_personaje(self, lugar):
        self.posicion_personaje = lugar

    def keyPressEvent(self, tecla):
        '''
        Envía señal a tecla_presionada
        '''
        movimiento = False
        self.antepenultima_letra = self.penultima_letra
        self.penultima_letra = self.ultima_letra
        if not self.pausa:
            if tecla.key() == Qt.Key_A:
                movimiento = True
                self.ultima_letra = "a"
            elif tecla.key() == Qt.Key_D:
                movimiento = True
                self.ultima_letra = "d"
            elif tecla.key() == Qt.Key_S:
                movimiento = True
                self.ultima_letra = "s"
            elif tecla.key() == Qt.Key_W:
                movimiento = True
                self.ultima_letra = "w"
        if movimiento:
            self.senal_tecla_presionada_mover.emit(self.ultima_letra)
        else:
            if tecla.key() == Qt.Key_V:
                self.ultima_letra = "v"
            elif tecla.key() == Qt.Key_I:
                self.ultima_letra = "i"
            elif tecla.key() == Qt.Key_D:
                self.ultima_letra = "d"
            elif tecla.key() == Qt.Key_N:
                self.ultima_letra = "n"
            elif tecla.key() == Qt.Key_P:
                self.ultima_letra = "p"
            else:
                self.ultima_letra = "z"
            if self.ultima_letra == "p":
                self.metodo_boton_pausar()
            else:
                combinacion = self.ultima_letra + self.penultima_letra + self.antepenultima_letra
                self.senal_tecla_presionada_cheat.emit(combinacion)

    def recibir_objeto(self, path_, posicion):
        objeto_auxiliar = QLabel(self)
        #print(path_)
        objeto_auxiliar.setPixmap(QPixmap(path_))
        objeto_auxiliar.setGeometry(*posicion, 30, 40)
        objeto_auxiliar.setScaledContents(True)
        objetos = set(filter(lambda x: x is not None, self.lista_objetos))
        rect_aux = objeto_auxiliar.geometry()
        algo_intersectado = False
        for cosa in (set(self.obstaculos) | objetos): # Reemplazar self.obstaculos con
            rect_cosa = cosa.geometry()
            if rect_aux.intersects(rect_cosa):
                algo_intersectado = True
                break
        if algo_intersectado:
            self.senal_pedir_objeto.emit()
        else:
            self.lista_objetos.append(objeto_auxiliar)
            #print("añadíiiii", path_, self.lista_objetos)
            objeto_auxiliar.show()

    def desaparecer_objeto(self, indice):
        objeto = self.lista_objetos[indice]
        self.lista_objetos[indice] = None
        objeto.hide()

    def actualizar_tablero(self, i_buenos, i_malos, vida, puntaje):
        '''
        este método actualiza los labels de 
        la partida cuando se llama
        '''
        self.label_items_buenos.setText(f"{i_buenos}")
        self.label_items_malos.setText(f"{i_malos}")
        self.label_puntaje.setText(f"{puntaje}")
        self.barra_vida.setValue(vida*100)

    def actualizar_personaje(self, path_dado):
        '''
        este método actualiza los labels de 
        personaje cuando se llama
        '''
        pixeles = QPixmap(path_dado)
        self.label_personaje.setPixmap(pixeles)
    
    def pasar_tiempo(self, tiempo):
        self.barra_tiempo.setValue(tiempo)

    def metodo_boton_pausar(self):
        '''
        Este método envía una señal a pausa_juego del backend
        '''
        self.senal_pausa_juego.emit()
        if not self.pausa:
            self.boton_pausar.setText("Reanudar")
            self.pausa = True
        else:
            self.boton_pausar.setText("Pausar")
            self.pausa = False

    def metodo_boton_salir(self):
        '''
        Este método envía una señal a salir_juego del backend
        '''
        self.senal_salir_juego.emit()
    
    def mover_gorgory(self, posicion):
        self.label_gorgory.move(*posicion)
        rect_personaje = self.label_personaje.geometry()
        rect_gorgory = self.label_gorgory.geometry()
        if rect_personaje.intersects(rect_gorgory):
            self.senal_acabar_juego.emit()
    
    def animacion_gorgory(self, path_dado):
        pixeles = QPixmap(path_dado)
        self.label_gorgory.setPixmap(pixeles)


class LogicaVentanaJuego(QObject):

    senal_enviar_actualizacion_tablero = pyqtSignal(int, int, float, int)
    senal_cargar_tablero = pyqtSignal()
    senal_cambiar_boton_pausa = pyqtSignal()
    senal_cambiar_pos_personaje = pyqtSignal(str)
    senal_generar_objeto = pyqtSignal(str, tuple)
    senal_inicializar_ventana = pyqtSignal(str, Personaje, int, str, int)
    senal_dar_obstaculos = pyqtSignal(list)
    senal_desaparecer_objeto = pyqtSignal(int)
    senal_pasar_tiempo = pyqtSignal(int)
    senal_esconder_ventana = pyqtSignal()
    senal_abrir_ventana_post_ronda = pyqtSignal(int, int, int, float)
    senal_mover_gorgory = pyqtSignal(tuple)
    senal_animacion_gorgory = pyqtSignal(str)
    #
    # senales_objetos

    def __init__(self) -> None:
        super().__init__()
        '''
        Este es el backend de la ventana juego, y se encarga de
        realizar los procesos de esta
        '''
        self.rectangulo_mapa = p.RECTANGULO_TABLERO_JUEGO

    def abrir_juego(self, edificio, personaje, numero_ronda, dificultad):
        '''
        Este método se encargará de leer el progreso de la partida
        cuando es llamado, y enviar la información al frontend 
        mediante la señal senal_enviar_actualizacion_tablero
        Además carga los objetos
        '''
        self.items_buenos = 0
        self.items_normales = 0
        self.items_malos = 0
        self.puntaje = 0
        self.edificio = edificio
        self.personaje = personaje
        self.gorgory = Gorgory(dificultad, self.personaje.nombre)
        self.objetos = []
        self.pausa = False
        self.horario_actual = time()
        self.terminado = False
        self.habilidad_especial_homero = False
        self.habilidad_homero_ultima_vez = 0
        # Tiempo que dura la ventana
        if dificultad == "intro":
            tiempo = p.DURACION_INTRO
        elif dificultad == "avanzada":
            tiempo = p.DURACION_AVANZADA
        self.tiempo = tiempo
        #
        # Posicion del personaje
        r = self.rectangulo_mapa
        pos = (randint(r[0], r[0] + r[2]), randint(r[1], r[1] + r[3]))
        self.personaje.inicializador_de_mapa("juego", self.rectangulo_mapa, pos, dificultad)
        self.gorgory.posicion = pos
        self.senal_inicializar_ventana.emit(edificio, personaje, numero_ronda, dificultad, tiempo)
        self.generador = f.Generador_de_objetos(self.personaje.nombre, dificultad)
        # Reloj de ventana
        self.tiempo_juego = QTimer()
        self.tiempo_juego.timeout.connect(self.pasar_tiempo)
        self.tiempo_juego.setInterval(1000*1)
        self.tiempo_juego.start()
        #
        self.conexiones()

    def conexiones(self):
        self.generador.senal_entregar_objeto.connect(self.recibir_objeto)
        self.personaje.senal_no_vida.connect(self.terminar_juego)
        self.gorgory.senal_animacion_gorgory.connect(self.animacion_gorgory)
        self.gorgory.senal_mover_gorgory.connect(self.mover_gorgory)
        self.gorgory.start()

    def recibir_objeto(self, objeto):
        self.objetos.append(objeto)
        objeto.aparecer(len(self.objetos) - 1)
        objeto.senal_desaparecer.connect(self.desaparecer_objeto)
        self.generar_objeto()

    def generar_objeto(self):
        '''
        Este método busca una posicion para el objeto si lo llama
        recibir objeto del backend. En caso de que no se haya podido poner,
        lo llama recibir objeto, pero del frontend
        '''
        r = self.rectangulo_mapa
        posicion = (randint(r[0], r[0] + r[2]), randint(r[1], r[1] + r[3]))
        path_objeto = self.objetos[-1].obtener_path()
        #print(path_objeto)
        self.senal_generar_objeto.emit(path_objeto, posicion)
    
    def desaparecer_objeto(self, indice):
        self.objetos[indice].senal_desaparecer.disconnect()
        self.senal_desaparecer_objeto.emit(indice)

    def generar_obstaculos(self):
        self.posiciones_obstaculos = list()
        for _ in range(3):
            misma_posicion = True
            while misma_posicion:
                misma_posicion = False
                r = self.rectangulo_mapa
                nuevo_obstaculo = (randint(r[0], r[0] + r[2]), randint(r[1] + 5, r[1] + r[3] + 5))
                # Se hace un ajuste de +5, ya que los límites están hecho de acuerdo a donde se
                # puede mover el personaje, y como los obstáculos son más pequeños, sus patas
                # no alcanzan a estar dentro del mapa
                for obstaculo in self.posiciones_obstaculos:
                    if (obstaculo[0] - nuevo_obstaculo[0])**2 <= 160**2 and\
                        (obstaculo[1] - nuevo_obstaculo[1])**2 <= 160**2:
                        misma_posicion = True
            self.posiciones_obstaculos.append(nuevo_obstaculo)
        dict_rutas = p.RUTAS_OBSTACULOS[self.edificio]
        lista_rutas = list()
        for ruta in dict_rutas:
            lista_rutas.append(dict_rutas[ruta])
        lista_final = list(zip(lista_rutas, self.posiciones_obstaculos))
        self.senal_dar_obstaculos.emit(lista_final)
    
    def objeto_tocado(self, indice):
        objeto = self.objetos[indice]
        objeto.senal_desaparecer.disconnect()
        que_hacer = objeto.dar_efecto()
        if objeto.tipo == "peligroso":
            self.items_malos += 1
        elif objeto.tipo == "x2" or objeto.tipo == "vida":
            self.items_buenos += 1
        else:
            self.items_normales += 1
        if que_hacer[0] == "vida":
            self.personaje.vida += que_hacer[1]
        elif que_hacer[0] == "puntaje":
            self.puntaje += que_hacer[1]
        else:
            raise ValueError("error al sumar objeto")
        if self.personaje.nombre == "homero" and self.items_normales % 10 == 0:
            if self.items_normales != 0 and self.items_normales != self.habilidad_homero_ultima_vez:
                self.habilidad_homero_ultima_vez = self.items_normales
                self.habilidad_especial_homero = True
                self.personaje.vida += p.PONDERADOR_VIDA_HOMERO
        if self.habilidad_especial_homero and objeto.tipo == "peligroso":
            self.habilidad_especial_homero = False
            self.items_malos = 0
        elif self.habilidad_especial_homero and (objeto.tipo == "x2" or objeto.tipo == "vida"):
            self.habilidad_especial_homero = False
            self.items_buenos -= 1

        self.enviar_actualizacion_tablero()

    def enviar_actualizacion_tablero(self):
        '''
        Este método se encargará de leer el progreso de la partida
        cuando es llamado y enviar la información al frontend 
        mediante la señal senal_enviar_actualizacion_tablero.
        '''
        a = self.items_buenos
        b = self.items_malos
        c = self.personaje.vida
        d = self.puntaje
            
        self.senal_enviar_actualizacion_tablero.emit(a, b, c, d)
    
    def pasar_tiempo(self):
        '''
        Este método es llamado por el QTimer que cambia el tiempo de juego
        '''
        self.tiempo -= 1
        if self.tiempo > 0:
            self.senal_pasar_tiempo.emit(self.tiempo)
        else:
            self.terminar_juego()

    def pausa_juego(self):
        '''
        Este método se encarga de, cuando es llamado,
        reanudar el juego si está pausado y pausarlo si no 
        mediante la señal senal_enviar_actualizacion_tablero.
        Además cambia el botón de pausa
        '''
        if not self.pausa:
            self.tiempo_juego.stop()
            self.generador.parar()
            self.personaje.timer.stop()
            for objeto in self.objetos:
                objeto.pausar()
            self.pausa = True
            self.gorgory.pausar()
        else:
            self.tiempo_juego.start()
            self.generador.iniciar()
            self.personaje.timer.start()
            for objeto in self.objetos:
                objeto.reanudar()
            self.pausa = False
            self.gorgory.pausar()

    def gorgory_intersectado(self):
        self.personaje.vida = 0
        self.terminar_juego()

    def terminar_juego(self):
        '''
        Este método se encarga de, cuando es llamado,
        salir del juego y llevar a la ventana post ronda
        '''
        if not self.terminado:
            self.terminado = True
            self.tiempo_juego.stop()
            self.generador.parar()
            self.personaje.timer.stop()
            self.gorgory.timer.stop()
            self.gorgory.senal_animacion_gorgory.disconnect()
            self.gorgory.senal_mover_gorgory.disconnect()

            for objeto in self.objetos:
                objeto.pausar()
            self.pausa = True
            self.senal_esconder_ventana.emit()
            #
            a = self.puntaje * self.personaje.vida
            b = self.items_buenos
            c = self.items_malos
            d = self.personaje.vida
            self.senal_abrir_ventana_post_ronda.emit(a, b, c, d)
        else:
            print("traté de terminar el juego, pero no se pudo")

    def salir_juego(self):
        '''
        Este método cierra el programa por el botón
        '''
        QApplication.quit()


    def cheats(self, combinacion):
        '''
        Comprueba si se ejecutó algún cheat, y los ejecuta
        '''
        if "v" in combinacion and "i" in combinacion and "d" in combinacion:
            self.personaje.vida += p.VIDA_TRAMPA
            self.enviar_actualizacion_tablero()
        elif "v" in combinacion and "i" in combinacion and "n" in combinacion:
            self.terminar_juego()

    # -------------------- Lo de aquí en adelante es para Gorgory

    def guardar_posicion_personaje(self, posicion):
        self.gorgory.recibir_posicion(posicion)

    def animacion_gorgory(self, path_dado):
        self.senal_animacion_gorgory.emit(path_dado)

    def mover_gorgory(self, posicion):
        self.senal_mover_gorgory.emit(posicion)

if __name__ == "__main__":
    app = QApplication([])
    ventana_juego = VentanaJuego()
    logica_juego = LogicaVentanaJuego()
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
    ventana_juego.senal_personaje_movido.connect(logica_juego.guardar_posicion_personaje)
    logica_juego.abrir_juego("bar", Moe(), 1, "intro")
    ########
    ventana_post_ronda = VentanaPostRonda()
    logica_post_ronda = LogicaVentanaPostRonda()
    logica_juego.senal_abrir_ventana_post_ronda.connect(logica_post_ronda.inicializar_ventana)
    logica_post_ronda.senal_inicializar.connect(ventana_post_ronda.inicializar_ventana)
    ventana_post_ronda.senal_continuar.connect(logica_post_ronda.continuar_juego)
    ventana_post_ronda.senal_salir.connect(logica_post_ronda.salir)
    ventana_post_ronda.senal_salir_inicio.connect(logica_post_ronda.salir_a_inicio)
    ####
    sys.exit(app.exec())