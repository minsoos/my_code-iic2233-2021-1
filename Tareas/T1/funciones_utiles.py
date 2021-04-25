import random


def ocurre_evento_por_probabilidad(probabilidad):
    if probabilidad > 1:
        return True
    if probabilidad < 0:
        return False
    else:
        probabilidad = str(probabilidad)
        probabilidad = probabilidad[probabilidad.find(".") + 1:]
        n_digitos = len(probabilidad)
        cota_sup = 10**len(probabilidad)
        probabilidad = int(probabilidad)
        numero_random = random.randint(0, cota_sup)
        if numero_random <= probabilidad:
            return True
        else:
            return False

def ordenar_por_km(barco):
    return barco.km

if __name__ == "__main__":
    print(ocurre_evento_por_probabilidad(0.5129389))