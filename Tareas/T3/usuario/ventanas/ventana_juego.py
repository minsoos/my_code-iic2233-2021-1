from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5 import uic
from utils import cargar_parametros, normalizar_ruta, ordenamiento_por_turno

parametros = cargar_parametros("parametros.json")
path_ventana_espera = parametros["RUTAS"]["VENTANA_JUEGO"]
path_ventana_espera = normalizar_ruta(path_ventana_espera)
nombre, padre = uic.loadUiType(path_ventana_espera)


class VentanaJuego(nombre, padre):

    senal_comprar_camino = pyqtSignal(tuple)
    senal_sacar_carta = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        parametros = cargar_parametros()
        self.dict_parametros = dict()
        mapa_sj = parametros["RUTAS"]["MAPA_SAN_JOAQUIN"]
        self.dict_parametros["mapa_sj"] = mapa_sj
        mapa_ing = parametros["RUTAS"]["MAPA_INGENIERIA"]
        self.dict_parametros["mapa_ing"] = mapa_ing
        fondo = parametros["RUTAS"]["IMAGEN_NUBES_ESPERA"]
        self.dict_parametros["fondo"] = fondo
        for elemento in self.dict_parametros:
            self.dict_parametros[elemento] = normalizar_ruta(self.dict_parametros[elemento])

        self.label_fondo.setPixmap(QPixmap(self.dict_parametros["fondo"]))
        self.boton_comprar.clicked.connect(self.metodo_comprar_camino)
        self.boton_sacar_carta.clicked.connect(self.metodo_sacar_carta)

        self.labels_turnos_de_jugador = {
            "my": self.mi_turno,
            "1": self.label_turno_j1,
            "2": self.label_turno_j2,
            "3": self.label_turno_j3
        }

        self.labels_nombres_de_jugador = {
            "my": self.mi_nombre,
            "1": self.nombre_j1,
            "2": self.nombre_j2,
            "3": self.nombre_j3
        }

        self.labels_baterias_de_jugador = {
            "my": self.mis_baterias,
            "1": self.baterias_j1,
            "2": self.baterias_j2,
            "3": self.baterias_j3
        }

        self.labels_foto_de_jugador = {
            "my": self.foto_mi_personaje,
            "1": self.foto_perfil_j1,
            "2": self.foto_perfil_j2,
            "3": self.foto_perfil_j3
        }

        self.jugadores = dict()

    def mostrar(self):
        self.show()

    def esconderse(self):
        self.hide()

    def metodo_comprar_camino(self):
        desde = self.edit_comprar_desde.text()
        hasta = self.edit_comprar_hacia.text()
        self.senal_comprar_camino.emit((desde, hasta))

    def metodo_sacar_carta(self):
        self.senal_sacar_carta.emit()

    def configurar_mapa(self, mapa):
        if mapa == "san joaquin":
            self.label_nombre_mapa.setText("San Joaquín")
            self.label_mapa.setPixmap(QPixmap(self.dict_parametros["mapa_sj"]))
        elif mapa == "ingenieria":
            self.label_nombre_mapa.setText("Ingeniería")
            self.label_mapa.setPixmap(QPixmap(self.dict_parametros["mapa_ing"]))
        else:
            raise ValueError("No se pudo configurar bien el mapa")

    def configurar_mi_nombre(self, nombre):
        self.mi_name = nombre

    def definir_jugadores(self, lista):
        for indice, jugador in enumerate(lista):
            print("lista", lista)
            if jugador["nombre"] == self.mi_name:
                self.definir_mi_jugador(lista.pop(indice))
                break

        self.definir_otros_jugadores(lista)
        self.show()

    def definir_mi_jugador(self, dict_):
        self.jugadores[dict_["nombre"]] = {
            "turno": dict_["turno"],
            "nombre": dict_["nombre"],
            "color": dict_["color"],
            "llave_para_labels": "my"
        }
        if dict_["turno"] == 1:
            self.label_turno_actual.setText(dict_["nombre"])
        self.labels_turnos_de_jugador["my"].setText(str(dict_["turno"]))
        self.labels_nombres_de_jugador["my"].setText(dict_["nombre"])

    def definir_otros_jugadores(self, lista_jugadores):
        lista_jugadores.sort(key=ordenamiento_por_turno)

        i = 1

        for persona in lista_jugadores:
            self.jugadores[persona["nombre"]] = {
                "turno": persona["turno"],
                "nombre": persona["nombre"],
                "color": persona["color"],
                "llave_para_labels": str(i)
            }
            if persona["turno"] == 1:
                self.label_turno_actual.setText(persona["nombre"])
            self.labels_turnos_de_jugador[str(i)].setText(str(persona["turno"]))
            self.labels_nombres_de_jugador[str(i)].setText(persona["nombre"])

            i += 1

    def recibir_imagen_de_perfil(self, imagen_en_bytes, color):
        for persona in self.jugadores:
            if self.jugadores[persona]["color"] == color:
                llave = self.jugadores[persona]["llave_para_labels"]
                pixmap = QPixmap()
                pixmap.loadFromData(imagen_en_bytes)
                self.labels_foto_de_jugador[llave].setPixmap(pixmap)
                break
        print(f"los jugadores son {self.jugadores}")

    def setear_baterias(self, baterias):
        for usuario in baterias:
            llave = self.jugadores[usuario]["llave_para_labels"]
            self.labels_baterias_de_jugador[llave].setText(str(baterias[usuario]))

    def definir_objetivo(self, desde, hasta):
        self.label_objetivo_desde.setText(str(desde))
        self.label_objetivo_hasta.setText(str(hasta))
        self.label_objetivo_desde.setStyleSheet("color: rgb(255, 255, 0)")
        self.label_objetivo_hasta.setStyleSheet("color: rgb(255, 255, 0)")
        self.label_objetivo1.setStyleSheet("color: rgb(255, 255, 0)")
        self.label_objetivo2.setStyleSheet("color: rgb(255, 255, 0)")

    def objetivo_cumplido(self):
        self.label_objetivo_desde.setStyleSheet("color: rgb(0, 255, 0);")
        self.label_objetivo_hasta.setStyleSheet("color: rgb(0, 255, 0);")
        self.label_objetivo1.setStyleSheet("color: rgb(0, 255, 0);")
        self.label_objetivo2.setStyleSheet("color: rgb(0, 255, 0);")

    def setear_error(self, mensaje):
        self.label_aviso.setText(mensaje)
    
    def cambiar_turno(self, nombre):
        self.label_turno_actual.setText(nombre)
    
    def dibujar_linea(self, posicion_1, posicion_2, color):
        pintador = QPainter()
        pintador.drawLine(posicion_1[0], posicion_1[1], *posicion_2)