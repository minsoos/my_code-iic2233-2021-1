from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QIcon
import parametros as p
from os import path
from random import randint
from PyQt5 import uic

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
        self.setWindowTitle("Ventana de Juego")
        self.setWindowIcon(QIcon(p.RUTA_LOGO_INICIO))
        # Atributos de la ventana
        self.personaje = None
        self.rutas_personajes = p.RUTAS_PERSONAJES
        self.rutas_imagenes = p.RUTAS_IMAGENES_JUEGO
        self.__posicion_personaje = (p.POSICION_DESAPARECER_PERSONAJE)
        self.lista_objetos = []
        self.obstaculos = []
        self.rectangulo_mapa = p.RECTANGULO_TABLERO_JUEGO
        # Dar propiedades a la ventana
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
        # botones-------------------------------
        # Boton_pausar
        self.boton_pausar.clicked.connect(self.metodo_boton_pausar)
        # Boton_salir
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
        self.dificultad = dificultad
        self.pausa = False # Estado de la pausa del juego

        self.label_ronda.setText(str(n_ronda))
        self.label_items_buenos.setText("0")
        self.label_items_malos.setText("0")
        self.label_puntaje.setText("0")

        self.senal_pedir_crear_obstaculos.emit()
        #Mapa por el que se mueve el jugador
        self.label_mapa.setPixmap(QPixmap(self.rutas_imagenes[f"mapa_{self.edificio}"]))
        self.barra_vida.setValue(self.personaje.vida * 100) # Vida del personaje
        self.barra_tiempo.setRange(0, tiempo) # Barra tiempo
        self.barra_tiempo.setValue(tiempo)

        posicion = p.POSICION_DESAPARECER_PERSONAJE
        tamano = p.TAMANO_PERSONAJES_JUEGO
        self.label_gorgory.setGeometry(*posicion, *tamano)


        # Seteamos las letras como una que no nos sirva para nada
        self.antepenultima_letra = "z"
        self.penultima_letra = "z"
        self.ultima_letra = "z"        

    def crear_obstaculos(self, lista):
        for ruta, posicion in lista:
            label_obstaculo_n = QLabel(self)
            label_obstaculo_n.setPixmap(QPixmap(ruta))
            label_obstaculo_n.setScaledContents(True)
            label_obstaculo_n.setGeometry(*posicion, *p.TAMANO_OBSTACULOS)
            self.obstaculos.append(label_obstaculo_n)
        self.personaje.labels_obstaculos = self.obstaculos
        self.init_gui_personaje()

    def init_gui_personaje(self):
        #Personaje
        if self.personaje.nombre in self.rutas_personajes.keys():
            ruta_inicial = self.rutas_personajes[self.personaje.nombre]
            pixeles = QPixmap(path.join(ruta_inicial, "up_3.png"))
            self.label_personaje.setPixmap(pixeles)
            posicion = p.POSICION_DESAPARECER_PERSONAJE
            tamano = p.TAMANO_PERSONAJES_JUEGO
            self.label_personaje.setGeometry(*posicion, *tamano)
            self.label_personaje.setScaledContents(True)
            #label configurado, ahora vemos la posición
            # ---------------Revisa que no tope con los obstáculos
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
            # -------------------------
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
    # ----------------- Mover el personaje

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
        # ----------------------- Revisa si topa con algún objeto para sacarlo
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
        # --------------------- Revisa si topa con Gorgory
        rect_gorgory = self.label_gorgory.geometry()
        if rect_personaje.intersects(rect_gorgory):
            self.senal_acabar_juego.emit()

    def mover_personaje(self, lugar):
        self.posicion_personaje = lugar

    # ------------------ Evento de tecla presionada

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
                combinacion = self.ultima_letra + self.penultima_letra + self.antepenultima_letra
                self.senal_tecla_presionada_cheat.emit(combinacion)
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
    
    # ------------------------ objetos

    def recibir_objeto(self, path_, posicion):
        '''
        Crea el objeto
        '''
        objeto_auxiliar = QLabel(self)
        #print(path_)
        objeto_auxiliar.setPixmap(QPixmap(path_))
        objeto_auxiliar.setGeometry(*posicion, *p.TAMANO_OBJETOS)
        objeto_auxiliar.setScaledContents(True)
        objetos = set(filter(lambda x: x is not None, self.lista_objetos))

        # ------------- Revisa si el objeto topa, si lo hace, pide otra pos. al backend

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

    # ---------------------------- Actualización de datos

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
        personaje cuando se llama, crea el efecto
        de animación
        '''
        pixeles = QPixmap(path_dado)
        self.label_personaje.setPixmap(pixeles)
    
    def pasar_tiempo(self, tiempo):
        self.barra_tiempo.setValue(tiempo)
    
    # ---------------------- Pausa

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

    # ---------------------- Gorgory
    
    def mover_gorgory(self, posicion):
        self.label_gorgory.move(*posicion)
        rect_personaje = self.label_personaje.geometry()
        rect_gorgory = self.label_gorgory.geometry()
        if rect_personaje.intersects(rect_gorgory):
            self.senal_acabar_juego.emit()
    
    def animacion_gorgory(self, path_dado):
        pixeles = QPixmap(path_dado)
        self.label_gorgory.setPixmap(pixeles)
    
    # ------------------------ Para salir del juego

    def metodo_boton_salir(self):
        '''
        Este método envía una señal a salir_juego del backend
        '''
        self.senal_salir_juego.emit()

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
