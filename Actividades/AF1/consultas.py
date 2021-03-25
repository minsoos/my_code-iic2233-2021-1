import cargar
from collections import defaultdict
platos = cargar.cargar_platos()
def platos_por_categoria(platos):
    diccionario = defaultdict(list)
    for i in platos:
        diccionario[platos[i].categoria].append(platos[i].n)
    return diccionario
    ##############
    #categorias = set()
    #for i in platos:
       # categorias.add(i.categoria)
    #for i in categorias:
      #  for e in range(len(platos)):



# Retorna los platos que no incluyan los ingredientes descartados
def descartar_platos(ingredientes_descartados, platos):
    platos_descartados={}
    for i in platos:
        tiene_ingrediente_descartado = False
        for e in ingredientes_descartados:
            for h in platos[i].ingredientes:
                if e == h:
                    tiene_ingrediente_descartado = True
        if tiene_ingrediente_descartado == False:
            platos_descartados[i] = platos[i]
    return platos_descartados


# Recibe un plato, comprueba si hay ingredientes suficientes y los descuenta
def ordenar_plato(plato, ingredientes):
    ingredientesp = plato.ingredientes
    hay = True
    for i in ingredientesp:
        if ingredientes[i]<1:
            hay = False
    if hay == False:
        return False
    else:
        for i in ingredientesp:
            ingredientes[i]-=1
        return True


# Recibe una lista de platos y retorna el resumen de esa orden
def resumen_orden(lista_platos):
    tiempo = 0
    presio = 0
    cantidad = 0
    platoss = []
    for i in lista_platos:
        platoss.append(i.n)
        cantidad += 1
        tiempo += i.tiempo
        presio += i.precio
    diccio = {"precio total": presio, "tiempo total": tiempo, "cantidad de platos": cantidad}
    diccio["platos"] = platoss
    return diccio


if __name__ == "__main__":
    # ================== PUEDES PROBAR TUS FUNCIONES AQUÍ =====================
    print(" PRUEBA CONSULTAS ".center(80, "="))
    platos_por_categoria(platos)
    print("DESCARTED",descartar_platos({"Lechuga","Queso","Tomate"}, platos))
    
    
