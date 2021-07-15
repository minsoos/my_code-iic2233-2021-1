def intentar_comprar_camino(self, id_usuario, desde, hasta):
    diccionario_preventivo = {
        "comando": "anunciar error"
    }
    nombre_jugador = self.usuarios_activos[id_usuario]["nombre"]
    desde, hasta = desde.upper(), hasta.upper()
    nombre_nodos = self.diccionario_nodos.keys()
    primera_condicion = desde in nombre_nodos
    segunda_condicion = hasta in nombre_nodos
    if primera_condicion and segunda_condicion:
        nodo_inicial = self.diccionario_nodos[desde]
        if nodo_inicial.es_su_vecino(hasta):
            camino = nodo_inicial.encontrar_camino_con(hasta)
            if camino is None:
                raise ValueError("El camino no está en los posibles")

            presio = camino.costo
            self.log(f"Tienes {self.baterias[nombre_jugador]} y cuesta {presio} baterías\n")
            if self.baterias[nombre_jugador] - presio >= 0:
                if camino.dueno is None:
                    self.baterias[nombre_jugador] -= presio
                    puntos = self.parametros["COSTO_VS_PUNTOS"][str(presio)]
                    self.puntajes_de_jugadores[nombre_jugador] += puntos
                    self.enviar_info_baterias()
                    self.enviar_pintada_de_camino(id_usuario, camino)
                    camino.dueno = nombre_jugador
                    self.comprobar_objetivo_cumplido(id_usuario)
                    self.enviar_info_puntaje(id_usuario)
                    self.caminos_faltantes -= 1
                    self.log(f"El jugador {nombre_jugador} compró el camino entre "
                        f"{camino.nodo_1.nombre} y {camino.nodo_2.nombre}, "
                        f"le quedan {self.baterias[nombre_jugador]} baterías\n")
                    return True
                else:
                    self.log(f"El jugador {nombre_jugador} no pudo comprar el camino entre"
                        f" {camino.nodo_1.nombre} y {camino.nodo_2.nombre} porque ya tiene "
                        f" dueño, tiene {self.baterias[nombre_jugador]}\n")
                    diccionario_preventivo["mensaje"] = "El camino ya tiene dueño"
                    self.enviar_mensaje_a_usuario(id_usuario, diccionario_preventivo)
                    return False
            else:
                self.log(f"El jugador {nombre_jugador} no pudo comprar el camino entre "
                        f"{camino.nodo_1.nombre} y {camino.nodo_2.nombre} porque "
                        f"tiene {self.baterias[nombre_jugador]} y el camino cuesta "
                        f"{presio}\n")
                diccionario_preventivo["mensaje"] = "No tienes suficiente dinero"
                self.enviar_mensaje_a_usuario(id_usuario, diccionario_preventivo)
                return False
        else:
            self.log(f"El jugador {nombre_jugador} no pudo comprar el camino porque no existe,"
                f" tiene {self.baterias[nombre_jugador]}\n")
            diccionario_preventivo["mensaje"] = "El camino que quieres comprar no existe"
            self.enviar_mensaje_a_usuario(id_usuario, diccionario_preventivo)
            return False
    else:
        self.log(f"El jugador {nombre_jugador} no pudo comprar el camino porque los valores"
            f" ingresados no son válidos. Tiene {self.baterias[nombre_jugador]}\n")
        diccionario_preventivo["mensaje"] = "Los nodos que indicas no son válidos"
        self.enviar_mensaje_a_usuario(id_usuario, diccionario_preventivo)
        return False