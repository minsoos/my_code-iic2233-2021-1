from os.path import join
from PyQt5 import uic
#Personajes
VELOCIDAD_HOMERO = None
PONDERADOR_VIDA_HOMERO = None
VELOCIDAD_LISA = None
PONDERADOR_TIEMPO_LISA = None
VELOCIDAD_PRUEBA = 8

#Dificultad

#Paths

RUTAS_RANKING = join("ranking.txt")
RUTAS_MADRE = {
    "planta": join("sprites", "Mapa", "Planta_nuclear"),
    "krustyland": join("sprites", "Mapa", "Krustyland"),
    "bar": join("sprites", "Mapa", "Bar"),
    "preparacion": join("sprites", "Mapa", "Mapa_Preparación"),
    "primaria": join("sprites", "Mapa", "Primaria")
}
RUTA_CEREBRO_HOMERO = join("sprites", "cerebro_homero.jpg")
#fuente: https://www.vix.com/es/series/189634/me-dijeron-lento-las-13-mejores-conversaciones-que-homero-tuvo-con-su-cerebro
RUTA_LOGO_INICIO = join("sprites", "logo_inicio.png")
RUTA_LOGO_RANKING = join("sprites", "logo_ranking.png")
#designer
DISENO_VENTANA_INICIO = join("assets", "ventana_inicio.ui")
DISENO_VENTANA_ERROR = join("assets", "ventana_de_error.ui")
DISENO_VENTANA_RANKING = join("assets", "ventana_ranking.ui")
DISENO_VENTANA_PREPARACION = join("assets", "ventana_preparacion.ui")

RUTAS_IMAGENES_JUEGO = {
    "mapa_planta": join(RUTAS_MADRE["planta"], "Mapa.png"),
    "obstaculon_planta": join(RUTAS_MADRE["planta"]),
    "logo": join("sprites", "Logo.png"),
    "mapa_krustyland": join(RUTAS_MADRE["krustyland"], "Mapa.png"),
    "mapa_bar": join(RUTAS_MADRE["bar"], "Mapa.png"),
    "mapa_preparacion": join(RUTAS_MADRE["preparacion"], "Mapa.png"),
    "mapa_primaria": join(RUTAS_MADRE["primaria"], "Mapa.png")
    
}
RUTAS_PERSONAJES = {
    "homero": join("sprites", "Personajes", "Homero"),
    "lisa": join("sprites", "Personajes", "Lisa"),
    "krusty": join("sprites", "Personajes", "Krusty"),
    "gorgory": join("sprites", "Personajes", "Gorgory"),
    "moe": join("sprites", "Personajes", "Moe")
}
RUTAS_OBSTACULOS_PLANTA = {
    "1": join(RUTAS_MADRE["planta"], "Obstaculo1.png"),
    "2": join(RUTAS_MADRE["planta"], "Obstaculo2.png"),
    "3": join(RUTAS_MADRE["planta"], "Obstaculo3.png")
}
RUTAS_OBJETOS_PLANTA = {
    "veneno": join("sprites", "Objetos", "Veneno.png"),
    "dona": join("sprites", "Objetos", "Dona.png"),
    "donax2": join("sprites", "Objetos", "DonaX2.png")
}
RUTAS_VENTANA_PREPARACION = {
    "homero": join("sprites", "Personajes", "Homero", "down_3.png"),
    "lisa": join("sprites", "Personajes", "Lisa", "down_1.png"),
    "krusty": join("sprites", "Personajes", "Krusty", "down_1.png"),
    "moe": join("sprites", "Personajes", "Moe", "down_1.png"),
    "logo": RUTA_LOGO_INICIO,
    "fondo": join(RUTAS_MADRE["preparacion"], "Fondo.png"),
    "planta": join(RUTAS_MADRE["preparacion"],"PlantaNuclear.png"),
    "bar": join(RUTAS_MADRE["preparacion"],"Bar.png"),
    "krustyland": join(RUTAS_MADRE["preparacion"],"Krustyland.png"),
    "primaria": join(RUTAS_MADRE["preparacion"],"Primaria.png")
}
#Objetos#########revisar
#APARICION_{DIFICULTAD} = None
#TIEMPO_OBJETO_{DIFICULTAD} = None
#Objetos normales
POSICION_INICIAL_VENTANA_PREPARACION = (50, 550)
PUNTOS_OBJETO_NORMAL = None
PROB_NORMAL = None
#Objetos buenos
PROB_BUENO = None
PONDERADOR_CORAZON = None
#Objetos peligrosos
PONDERADOR_VENENO = None
PROB_VENENO = None

#Obstáculos

#Personaje enemigo (Jefe Gorgory)##########
#TIEMPO_DELAY_{DIFICULTAD} = None

#Configuración rondas
DURACION_INTRO = None
APARICION_INTRO = None
DURACION_AVANZADA = None
APARICION_AVANZADA = None

#cheatscodes
VIDA_TRAMPA = None