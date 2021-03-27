def respuesta_invalida_seguir():  
    #  Se llama cuando el usuario da una respuesta inválida
    #  Returna True o False dependiendo si el usuario desea repetir la acción
    #  o desea volver al menú principal de la sección
    print("¿Desea volver a intentarlo?\n")
    print("[1]Sí\n[2]No, volver al menú principal\n")
    desea_seguir = input()
    if desea_seguir == "1":
        return True
    elif desea_seguir == "2":
        return False
    else:
        print("Respuesta inválida\n")
        return respuesta_invalida_seguir()