import manejo_de_archivos
def menu_de_inicio():
    print("")
    print("*"*50 + "\n" + "*"*17 + " MENÚ DE INICIO " + "*"*17 + "\n" + "*"*50)
    print("\nHola, ¿qué deseas hacer?")
    print("\n[1]Comenzar una nueva simulación\n[0]Cerrar sesión\n")
    input_usuario = input()
    if input_usuario == "1":
        print("Qué canal deseas simular?")
        canal_a_simular = input()
        manejo_de_archivos.lista_canales()
        if
    elif input_usuario == "0":
        print("Sé que te va bien")
        print("La verdad sé que te va cabrón")
        print("pero no quiero aceptar esto al cien")
        return None
    
    else:
        print("No ingresaste una opción válida")
        return menu_de_inicio()
