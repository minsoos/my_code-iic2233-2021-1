from PyQt5 import uic
import parametros as p
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import parametros as p
from time import time
from frontend.labels_drag_drop import DragLabel, DropLabel

nombre_preparacion, padre_preparacion = uic.loadUiType(p.DISENO_VENTANA_PREPARACION)
nombre_error, padre_error = uic.loadUiType(p.DISENO_VENTANA_MAPA_ERRADO)


class VentanaPreparacion(nombre_preparacion, padre_preparacion):

    senal_iniciar_nueva_partida = pyqtSignal()
    senal_solicitud_cambiar_personaje = pyqtSignal(str, tuple)
    senal_tecla_presionada_mover = pyqtSignal(str)
    senal_solicitud_entrar_edificio = pyqtSignal(str, str)
    senal_boton_salir = pyqtSignal()
    senal_cheat = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ventana de preparación")
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
        # Configuración de labels del archivo ui
        self.dic_paths = p.RUTAS_VENTANA_PREPARACION
        self.label_logo.setPixmap(QPixmap(self.dic_paths["logo"]))
        self.cargar_edificios()
        self.create_drag_and_drop()

        # ----------------------- Label personaje

        self.label_personaje = QLabel(self)
        posicion = p.POSICION_DESAPARECER_PERSONAJE
        tamano = p.TAMANO_PERSONAJES_PREPARACION
        self.label_personaje.setGeometry(*posicion, *tamano)
        self.label_personaje.setScaledContents(True)
        self.label_personaje.show()

        # ----------------- Otros
        self.conexiones()
        self.antepenultima_letra = "z"
        self.penultima_letra = "z"
        self.ultima_letra = "z"

        # Esto permite que cada vez que se clickea dentro de la pantalla, el programa
        # se "fije" en ella, pasa que cuando se clickea en otra parte, como una QComboBox
        # el programa pierde el foco, y no se puede seguir moviendo el personaje
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

    def create_drag_and_drop(self):
        #### ------------------------- Labels con drag
        # Transparencia sacado de fuente:
        # https://stackoverflow.com/questions/9952553/transpaprent-qlabel/10038177
        # No se usó transparencia porque se producía un error en los labels al arrastrarlos
        # De todas maneras se puede implementar descomentando
        self.diccionario_labels_personajes = dict()
        for personaje in ("lisa", "homero", "krusty", "moe"):
            self.label_n = DragLabel(self, personaje)
            # self.label_n.setAttribute(Qt.WA_TranslucentBackground, True)
            self.label_n.setPixmap(QPixmap(self.dic_paths[personaje]))
            self.label_n.setScaledContents(True)
            self.label_n.setMaximumSize(60, 70)
            self.diccionario_labels_personajes[personaje] = self.label_n
        self.layout_lisa.addWidget(self.diccionario_labels_personajes["lisa"])
        self.layout_homero.addWidget(self.diccionario_labels_personajes["homero"])
        self.layout_moe.addWidget(self.diccionario_labels_personajes["moe"])
        self.layout_krusty.addWidget(self.diccionario_labels_personajes["krusty"])

        # ------------------ Fondo con drop

        self.label_fondo = DropLabel("", self)
        self.label_fondo.setPixmap(QPixmap(self.dic_paths["fondo"]))
        self.label_fondo.setMinimumHeight(416)
        self.label_fondo.setMaximumHeight(416)
        self.label_fondo.setScaledContents(True)
        self.layout_principal.addWidget(self.label_fondo)

    def conexiones(self):
        self.boton_salir.clicked.connect(self.metodo_boton_salir)
        self.label_fondo.senal_poner_personaje.connect(self.solicitud_cambiar_personaje)

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

    def solicitud_cambiar_personaje(self, nombre, posicion):
        if nombre in ("homero, lisa, krusty, moe"):
            print("solicitaste cambiar el personaje")
            self.label_personaje.show()
            self.senal_solicitud_cambiar_personaje.emit(nombre, posicion)
        else:
            raise ValueError("el boton apretado no ta")

    # ------------------ Desde aquí se trabajan las señales recibidas y dadas
    # ------------------ para la actualización del label de personaje

    def keyPressEvent(self, tecla):
        '''
        Envía señal a tecla_presionada
        '''
        self.antepenultima_letra = self.penultima_letra
        self.penultima_letra = self.ultima_letra
        if tecla.key() == Qt.Key_A:
            self.ultima_letra = "a"
        elif tecla.key() == Qt.Key_D:
            self.ultima_letra = "d"
        elif tecla.key() == Qt.Key_S:
            self.ultima_letra = "s"
        elif tecla.key() == Qt.Key_W:
            self.ultima_letra = "w"
        elif tecla.key() == Qt.Key_V:
            self.ultima_letra = "v"
        elif tecla.key() == Qt.Key_I:
            self.ultima_letra = "i"
        elif tecla.key() == Qt.Key_D:
            self.ultima_letra = "d"
        else:
            self.ultima_letra = "z"

        if self.ultima_letra in "asdw":
            self.senal_tecla_presionada_mover.emit(self.ultima_letra)
        else:
            combinacion = self.ultima_letra + self.penultima_letra + self.antepenultima_letra
            self.senal_cheat.emit(combinacion)

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

    # -------------------------- Otros

    def ocultar_ventana(self, respuesta):
        if respuesta:
            self.hide()
            self.label_personaje.move(*p.POSICION_DESAPARECER_PERSONAJE)
            self.antepenultima_letra = "z"
            self.penultima_letra = "z"
            self.ultima_letra = "z"

    def mostrar_ventana(self):
        self.show()

    def metodo_boton_salir(self):
        self.senal_boton_salir.emit()


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
        if tiempo_nuevo - self.tiempo_antiguo > p.TIEMPO_ENTRE_MENSAJES_DE_ERROR:
            # Este método es para que no salte la ventana todo el rato
            self.tiempo_antiguo = tiempo_nuevo
            self.show()

    def metodo_volver(self):
        self.hide()
