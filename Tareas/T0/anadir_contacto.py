import menu_contactos
from collections import defaultdict


def anadir_contacto(usuario):
    print("\n¿A quién desea añadir?\n")
    #  revisamos archivo de contactos.csv
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
    #  revisamos si está el input en el archivo
    agregar_a = input()
    if agregar_a in dict_contactos:
        if agregar_a in contactos_del_user:
            print("Este contacto ya está agregado\n")
            return menu_contactos.menu_contactos(usuario)
        else:
            contactos_archivo = open("contactos.csv", "a")
            contactos_archivo.write(f"\n{usuario},{agregar_a}")
            contactos_archivo.close()
            print(f"Contacto añadido con éxito, ve y habla con {agregar_a}!")
            print("")
            return menu_contactos.menu_contactos(usuario)
    else:
        print("El usuario no existe\n")
        return menu_contactos.menu_contactos(usuario)


if __name__ == "__main__":
    anadir_contacto("lily416")