import manejo_de_archivos
from canales import Canal ##  Sacar después, es para pruebas locales

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
    n_barco=1
    lista_barcos_encallados = list()
    numeros_barcos_encallados = set()
    for barco in canal.barcos:
        if barco.esta_encallado:
            print(f"[{n_barco}]{barco.nombre}")
            lista_barcos_encallados.append((barco))
            numeros_barcos_encallados.add(i)
            n_barco+=1
    print("[0]Volver")
    print("-"*50)
    print("\nEscoge una opción\n")
    opcion = input()
    try:
        opcion = int(opcion)
        if opcion == 0:
            menu_de_acciones
        elif opcion in numeros_barcos_encallados:
            barco = lista_barcos_encallados[opcion - 1]
            canal.desencallar_barco(barco)
    except ValueError: 
        menu_de_acciones 
        # Comentario para mí: ojo si se repite el menú de acc

def acc_simular_hora(canal):
    menu_de_acciones(canal)

def acc_mostrar_estado(canal):
    menu_de_acciones(canal)



if __name__ == "__main__":
    canal_prueba = Canal("canal de pana", 37, "avanzado")
    barcos = manejo_de_archivos.dict_barcos()
    barco_prueba1 = barcos["La Nao Victoria"]
    canal_prueba.ingresar_barco_al_canal(barco_prueba1)
    menu_de_acciones(canal_prueba)