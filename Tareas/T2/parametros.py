from os import path
#Personajes
VELOCIDAD_HOMERO = None
PONDERADOR_VIDA_HOMERO = None
VELOCIDAD_LISA = None
PONDERADOR_TIEMPO_LISA = None

#Dificultad

#Paths
RUTA_RANKING = path.join("ranking.txt")
RUTAS_MADRE = {
    "planta": path.join("sprites", "Mapa", "Planta_nuclear"),
    "krustyland": path.join("sprites", "Mapa", "Krustyland"),
    "bar": path.join("sprites", "Mapa", "Bar"),
    "preparacion": path.join("sprites", "Mapa", "Mapa_Preparacion"),
    "primaria": path.join("sprites", "Mapa", "Primaria")
}

RUTA_IMAGENES_JUEGO = {
    "mapa_planta": path.join(RUTAS_MADRE["planta"], "Mapa.png"),
    "obstaculon_planta": path.join(RUTAS_MADRE["planta"]),
    "logo": path.join("sprites", "Logo.png"),
    "mapa_krustyland": path.join(RUTAS_MADRE["krustyland"], "Mapa.png"),
    "mapa_bar": path.join(RUTAS_MADRE["bar"], "Mapa.png"),
    "mapa_preparacion": path.join(RUTAS_MADRE["preparacion"], "Mapa.png"),
    "mapa_primaria": path.join(RUTAS_MADRE["primaria"], "Mapa.png")
    
}
RUTA_PERSONAJES = {
    "homero": path.join("sprites", "Personajes", "Homero"),
    "lisa": path.join("sprites", "Personajes", "Lisa"),
    "krusty": path.join("sprites", "Personajes", "Krusty"),
    "gorgory": path.join("sprites", "Personajes", "Gorgory"),
    "moe": path.join("sprites", "Personajes", "Moe")
}
#Objetos#########revisar
#APARICION_{DIFICULTAD} = None
#TIEMPO_OBJETO_{DIFICULTAD} = None
#Objetos normales
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