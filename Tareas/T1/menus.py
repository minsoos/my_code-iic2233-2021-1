import manejo_de_archivos
from canales import Canal ##  Sacar después, es para pruebas locales
import parametros
from barcos import ordenar_por_km
from simular_hora import acc_simular_hora

def menu_de_inicio():
    print("")
    print("*"*50 + "\n" + "*"*17 + " MENÚ DE INICIO " + "*"*17 + "\n" + "*"*50)
    print("\nHola, ¿qué deseas hacer?")
    print("\n[1]Comenzar una nueva simulación\n[0]Salir\n")
    input_usuario = input()
    if input_usuario == "1":
        print("Qué canal deseas simular?")
        canal_a_simular = input()
        dict_canales = manejo_de_archivos.dict_canales()
        if canal_a_simular in dict_canales.keys():
            menu_de_acciones(dict_canales[canal_a_simular])
        else:
            print("Canal no encontrado")
            menu_de_inicio()
    elif input_usuario == "0":
        print("Sé que te va bien")
        print("La verdad sé que te va cabrón")
        print("pero no quiero aceptar esto al cien")
        None
    else:
        print("No ingresaste una opción válida")
        menu_de_inicio()


def menu_de_acciones(canal):
    print("")
    if canal.dinero >= 0:
        print("*"*50 + "\n" + "*"*16 + " MENÚ DE ACCIONES " + "*"*16 + "\n" + "*"*50)
        print(f"\nHola, veo que eres admin de {canal.nombre}")
        print("\n[1]Mostrar riesgo de encallamiento\n[2]Desencallar barco")
        print("[3]Simular nueva hora\n[4]Mostar estado\n[0]Volver\n")
        input_del_usuario = input()
        ##  Se usará la notación acc_<funcion> para referirse
        ##  a una acción del menú de acciones
        if input_del_usuario == "1":
            acc_mostrar_proba(canal)
        elif input_del_usuario == "2":
            acc_desencallar(canal)
        elif input_del_usuario == "3":
            acc_simular_hora(canal)
        elif input_del_usuario == "4":
            acc_mostrar_estado(canal)
        elif input_del_usuario == "0":
            menu_de_inicio()
        else:
            print("No ingresaste una opción válida")
            menu_de_acciones(canal)
    else:
        print("Quebraste, ya no puedes seguir controlando el canal")


def acc_mostrar_proba(canal):
    print(f"\nBarcos: Probabilidad de encallar")
    print("-"*50)
    for barco in canal.barcos:
        print(f"{barco.nombre}: {barco.prob_encallar}")
    print("\n" + "-"*50)
    if len(canal.barcos) == 0:
        print(" "*10 + "**Lista vacía**")
    menu_de_acciones(canal)


def acc_desencallar(canal):
    print(f"\nBarcos encallados:")
    print("-"*50)
    n_barco = 1
    lista_barcos_encallados = list()
    numeros_barcos_encallados = set()
    for barco in canal.barcos:
        if barco.esta_encallado:
            print(f"[{n_barco}]{barco.nombre}")
            lista_barcos_encallados.append((barco))
            numeros_barcos_encallados.add(n_barco)
            n_barco += 1
    print("[0]Volver")
    print("-"*50)
    print("\nEscoge una opción\n")
    #  Ahora el usuario ingresa el input
    opcion = input()
    try:
        opcion = int(opcion)
        if opcion == 0:
            menu_de_acciones(canal)
        elif opcion in numeros_barcos_encallados:
            barco = lista_barcos_encallados[opcion - 1]
            if canal.dinero >= parametros.COSTO_DESENCALLAR:
                se_pudo_desencallar = canal.desencallar_barco(barco)
                if se_pudo_desencallar:
                    print("El barco fue desencallado")
                    menu_de_acciones(canal)
                elif not se_pudo_desencallar:
                    print("Operación no exitosa, perdimos dinero para nada")
                    menu_de_acciones(canal)
            else:
                print("No hay money")
                menu_de_acciones(canal)
        else:
            print("opción no válida")
            menu_de_acciones(canal)
    except ValueError:
        print("opción no válida")
        menu_de_acciones(canal)
        # Comentario para mí: ojo si se repite el menú de acc

def acc_mostrar_estado(canal):
    mensaje = "Estado del canal"
    print(f"\n{mensaje:^50s}\n")
    print("-" * 50)
    print(f"{canal.nombre} de {canal.largo}km de largo, con dificultad {canal.dificultad}")
    print(f"Horas simuladas: {canal.horas_simuladas}")
    print(f"Dinero disponible: {canal.dinero}")
    print(f"Dinero gastado: {canal.dinero_gastado}")
    print(f"Dinero recibido: {canal.dinero_recibido}")
    print(f"Número de barcos que pasaron: {canal.n_barcos_historicos}")
    print(f"Número de barcos que encallaron: {canal.n_barcos_encallados}")
    print(f"Eventos especiales ocurridos: {canal.n_eventos_especiales}")
    if len(canal.barcos) > 0:
        print("\nBarcos y sus posiciones:\n")
        canal.barcos.sort(key=ordenar_por_km, reverse=False)
        for barco in canal.barcos:
            print(f"{barco.nombre} está en el km {barco.km}")
    print("-" * 50 + "\n")
    menu_de_acciones(canal)




if __name__ == "__main__":
    menu_de_inicio()
    #canal_prueba = Canal("canal de pana", 37, "avanzado")
    #barcos = manejo_de_archivos.dict_barcos()
    #barco_prueba1 = barcos["La Nao Victoria"]
    #canal_prueba.ingresar_barco(barco_prueba1)
    #menu_de_acciones(canal_prueba)

# Crear eventos especiales
# La lista de barcos no cambia (no se descuentan barcos que están dentro)
# Seguir probando