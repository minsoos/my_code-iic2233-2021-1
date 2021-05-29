import sys
from ventana_preparacion import LogicaVentanaPreparacion, VentanaPreparacion
from ventana_ranking import LogicaVentanaRanking, VentanaRanking

from PyQt5.QtWidgets import QApplication

import parametros as p
from ventana_de_inicio import VentanaError, VentanaInicio, LogicaVentanaInicio
from ventana_preparacion import VentanaPreparacion, LogicaVentanaPreparacion
###Hay que crear el ranking.txt si no existe


def hook(type_error, traceback):
    print(type_error)
    print(traceback)

open("ranking.txt", "a")

if __name__ == "__main__":
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    # --------------------------Ventana inicio
    ventana_inicio = VentanaInicio()
    logica_ventana_inicio = LogicaVentanaInicio()
    # Señales
    ventana_inicio.senal_solicitar_partida.connect(logica_ventana_inicio.comprobar_alfanum)
    ventana_inicio.senal_abrir_ranking.connect(logica_ventana_inicio.requerimiento_ver_ranking)
    logica_ventana_inicio.senal_inicio_partida.connect(ventana_inicio.inicio_partida)
    # ---------------------------Ventana error
    ventana_inicio_error = VentanaError()
    # Señales
    logica_ventana_inicio.senal_ventana_error.connect(ventana_inicio_error.mostrar)
    # ----------------------------Ventana ranking
    ventana_ranking = VentanaRanking()
    logica_ventana_ranking = LogicaVentanaRanking()
    # Señales
    ventana_inicio.senal_abrir_ranking.connect(ventana_ranking.mostrar)
    ventana_ranking.senal_pedir_actualizar.connect(logica_ventana_ranking.extraer_lugares)
    logica_ventana_ranking.senal_cargar_puntajes.connect(ventana_ranking.actualizar)
    # -----------------------------Ventana preparación partida
    ventana_preparacion = VentanaPreparacion()
    logica_ventana_preparacion = LogicaVentanaPreparacion()
    # Señales
    conexion_n = logica_ventana_preparacion.iniciar_nueva_partida
    logica_ventana_inicio.senal_inicio_partida.connect(conexion_n)
    conexion_n = ventana_preparacion.actualizar_info
    logica_ventana_preparacion.senal_actualizar_info_ventana.connect(conexion_n)
    conexion_n = logica_ventana_preparacion.cambiar_personaje
    ventana_preparacion.senal_solicitud_cambiar_personaje.connect(conexion_n)


    app.exec()
