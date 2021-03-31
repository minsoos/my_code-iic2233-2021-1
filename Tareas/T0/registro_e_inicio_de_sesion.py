def funcion_interfaz_menu():
    #  Esta función muestra la interfaz del menú de inicio
    print("\n[1] Iniciar sesión\n[2] Registrarse\n[0] Fuirse :(\n")
    respuesta = input()
    if respuesta == "1":
        return funcion_iniciar_sesion()
    elif respuesta == "2":
        return funcion_registrar_usuario()
    elif respuesta == "0":
        return False, False
    else:
        print("Respuesta inválida")
        return funcion_interfaz_menu()


def funcion_iniciar_sesion():
    #  Esta función le da el ingreso de sesión al usuario:
    print("\nIngrese su nombre de usuario para iniciar sesión\n")
    nombre_a_verificar = input()
    archivo_usuarios = open("usuarios.csv")
    usuarios = archivo_usuarios.readlines()
    for i in range(1, len(usuarios)):
        usuarios[i] = usuarios[i].strip()
    usuarios = set(usuarios)
    if nombre_a_verificar in usuarios:
        #  busca el nombre ingresado en el archivo de usuarios
        archivo_usuarios.close()
        return (True, nombre_a_verificar)
    else:
        print("Este nombre de usuario no existe")
        return funcion_interfaz_menu()


def funcion_registrar_usuario():
    print("\nIngrese el nombre de usuario que desea")
    print("Su nombre de usuario debe tener entre 3 y 15 caracteres,\
 y no puede llevar una \",\"\n")
    nombre_a_verificar = input()
    if 3 <= len(nombre_a_verificar) <= 15 and "," not in nombre_a_verificar:
        #  Revisa si el nombre cumple los requisitos dados
        archivo_usuarios = open("usuarios.csv")
        usuarios = archivo_usuarios.readlines()
        archivo_usuarios.close()
        for i in range(1, len(usuarios)):
            usuarios[i] = usuarios[i].strip()
        usuarios = set(usuarios)
        if nombre_a_verificar not in usuarios:
            #  Revisa si el nombre dado está registrado
            archivo_usuarios = open("usuarios.csv", "a")
            archivo_usuarios.write("\n" + nombre_a_verificar)
            archivo_usuarios.close()
            print("\nFelicidades, ya eres parte de nuestra comunidad!")
            print("Ahora sólo debes iniciar sesión")
            return funcion_interfaz_menu()
        else:
            print("\n El nombre de usuario ya está en uso")
            return funcion_interfaz_menu()
    else:
        print("Su nombre de usuario no cumple los requisitos indicados\n")
        return funcion_interfaz_menu()


if __name__ == "__main__":
    funcion_interfaz_menu()
