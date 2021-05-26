from os.path import join
#Personajes
VELOCIDAD_HOMERO = None
PONDERADOR_VIDA_HOMERO = None
VELOCIDAD_LISA = None
PONDERADOR_TIEMPO_LISA = None

#Dificultad

#Paths
RUTAS_RANKING = join("ranking.txt")
RUTASS_MADRE = {
    "planta": join("sprites", "Mapa", "Planta_nuclear"),
    "krustyland": join("sprites", "Mapa", "Krustyland"),
    "bar": join("sprites", "Mapa", "Bar"),
    "preparacion": join("sprites", "Mapa", "Mapa_Preparacion"),
    "primaria": join("sprites", "Mapa", "Primaria")
}

RUTAS_IMAGENES_JUEGO = {
    "mapa_planta": join(RUTASS_MADRE["planta"], "Mapa.png"),
    "obstaculon_planta": join(RUTASS_MADRE["planta"]),
    "logo": join("sprites", "Logo.png"),
    "mapa_krustyland": join(RUTASS_MADRE["krustyland"], "Mapa.png"),
    "mapa_bar": join(RUTASS_MADRE["bar"], "Mapa.png"),
    "mapa_preparacion": join(RUTASS_MADRE["preparacion"], "Mapa.png"),
    "mapa_primaria": join(RUTASS_MADRE["primaria"], "Mapa.png")
    
}
RUTAS_PERSONAJES = {
    "homero": join("sprites", "Personajes", "Homero"),
    "lisa": join("sprites", "Personajes", "Lisa"),
    "krusty": join("sprites", "Personajes", "Krusty"),
    "gorgory": join("sprites", "Personajes", "Gorgory"),
    "moe": join("sprites", "Personajes", "Moe")
}
RUTAS_OBSTACULOS_PLANTA = {
    "1": join(RUTASS_MADRE["planta"], "Obstaculo1.png"),
    "2": join(RUTASS_MADRE["planta"], "Obstaculo2.png"),
    "3": join(RUTASS_MADRE["planta"], "Obstaculo3.png")
}
RUTAS_OBJETOS_PLANTA = {
    "veneno": join("sprites", "Objetos", "Veneno.png"),
    "dona": join("sprites", "Objetos", "Dona.png"),
    "donax2": join("sprites", "Objetos", "DonaX2.png")
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