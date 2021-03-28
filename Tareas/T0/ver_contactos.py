import menu_contactos
from funciones_recurrentes import respuesta_invalida_seguir
from collections import defaultdict
from abrir_chat import abrir_chat


def ver_contactos(usuario):
    print("*"*50 + "\n" + "*"*17 + " VER CONTACTOS " + "*"*18 + "\n" + "*"*50)
    print(f"\n{usuario}, tus contactos actuales se encuentran abajo\n")
    #  #####guardamos los contactos en una lista llamada contactos_del_user
    contactos_archivo = open("contactos.csv")
    contactos = contactos_archivo.readlines()
    contactos_archivo.close()
    dict_contactos = defaultdict(list)
    for i in range(len(contactos)):
        contactos[i] = contactos[i].strip().split(",")
        dict_contactos[contactos[i][0]].append(contactos[i][1])
    hay_contactos = False
    for user in dict_contactos:
        if user == usuario:
            contactos_del_user = dict_contactos[user]
            hay_contactos = True
    #  #####imprimimos cada uno de los contactos de esa lista con su índice
    if hay_contactos:
        for i in range(len(contactos_del_user)):
            print(f"[{i+1}] {contactos_del_user[i]}")
    print("[0] Volver al menú de contactos\n")
    #  #####damos el input y retornamos según la elección
    opcion = input()
    if opcion == "0":
        return menu_contactos.menu_contactos(usuario)
    elif opcion.isdigit():
        opcion = int(opcion)
        if 1 <= opcion <= len(contactos_del_user) and hay_contactos:
            # Si es dígito y está entre los pedidos abrimos el chat
            contacto_elegido = contactos_del_user[opcion-1]
            return abrir_chat(usuario, contacto_elegido, "regular")
        else:
            # Los dos else que quedan es para o repetir, o para volver al menú de chats
            print("opción no válida")
            desea_seguir = respuesta_invalida_seguir()
            if desea_seguir:
                return ver_contactos(usuario)
            else:
                return menu_contactos.menu_contactos(usuario)
    else:
        print("opción no válida")
        desea_seguir = respuesta_invalida_seguir()
        if desea_seguir:
            return ver_contactos(usuario)
        else:
            return menu_contactos.menu_contactos(usuario)


if __name__ == "__main__":
    ver_contactos("lily416")