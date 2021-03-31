import menu_grupos
from funciones_recurrentes import respuesta_invalida_seguir
from collections import defaultdict
import abrir_chat


def ver_grupos(usuario):
    print("")
    print("*"*50 + "\n" + "*"*9 + " GRUPOS DE LOS QUE ERES MIEMBRO " + "*"*9 + "\n" + "*"*50)
    print(f"\n{usuario}, tus grupos actuales se encuentran abajo\n")
    #  #####Guardamos los grupos en una lista llamada grupos_del_user
    grupos_archivo = open("grupos.csv")
    grupos = grupos_archivo.readlines()
    grupos_archivo.close()
    dict_grupos = defaultdict(list)
    for i in range(len(grupos)):
        grupos[i] = grupos[i].strip().split(",")
        dict_grupos[grupos[i][1]].append(grupos[i][0])
    hay_grupos = False
    for user in dict_grupos:
        if user == usuario:
            grupos_del_user = list(set(dict_grupos[user]))
            hay_grupos = True
    #  #####imprimimos cada uno de los grupos de esa lista con su índice
    if hay_grupos:
        for i in range(len(grupos_del_user)):
            print(f"[{i+1}] {grupos_del_user[i]}")
    print("[0] Volver al menú de grupos\n")
    #  #####damos el input y retornamos según la elección
    opcion = input()
    if opcion == "0":
        return menu_grupos.menu_grupos(usuario)
    elif opcion.isdigit():
        opcion = int(opcion)
        if 1 <= opcion <= len(grupos_del_user) and hay_grupos:
            # Si es dígito y está entre los pedidos abrimos el chat
            grupo_elegido = grupos_del_user[opcion-1]
            return abrir_chat.abrir_chat(usuario, grupo_elegido, "grupo")
        else:
            # Los dos else que quedan es para o repetir, o para volver al menú de chats
            print("opción no válida")
            desea_seguir = respuesta_invalida_seguir()
            if desea_seguir:
                return ver_grupos(usuario)
            else:
                return menu_grupos.menu_grupos(usuario)
    else:
        print("opción no válida")
        desea_seguir = respuesta_invalida_seguir()
        if desea_seguir:
            return ver_grupos(usuario)
        else:
            return menu_grupos.menu_grupos(usuario)


if __name__ == "__main__":
    ver_grupos("lily416")