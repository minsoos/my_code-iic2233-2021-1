from json.decoder import JSONDecodeError
import requests
import json


# ------------------------------------------------------------------------------------------------
# DEFINIR AQUI LAS CONSTANTES QUE SERAN UTILIZADAS PARA INTERACTUAR CON LA API
NOMBRE = "Min Soo"
USERNAME = "min_soos"
URL = "https://actividad-bonus-iic2233.herokuapp.com/"


# ------------------------------------------------------------------------------------------------
# Completar a continuación el código para realizar las solicitudes necesarias a la API. Cada
# función recibe los argumentos necesarios para realizar la consulta y aplicar lógica adicional,
# en caso de ser necesario

# Registro en aplicación
def registro(nombre, username):
    url = URL+"estudiantes"
    data = {
        "nombre": nombre,
        "username": username
    }
    respuesta = requests.post(url, data=data)
    return respuesta.status_code

# Descarga de documento Markdown
def descargar_documento(identificador_documento, ruta_documento):
    url = URL+f"documentos/{identificador_documento}"
    respuesta = requests.get(url)
    with open(ruta_documento, "w") as file:
        file.write(respuesta.json()["texto"])


# Probar una de las consulas
def entregar_consulta(n_consulta, identificador_documento, patron, respuesta):
    url = URL+f"estudiantes/{USERNAME}/consultas"
    data = {
        "consulta": n_consulta,
        "documento": identificador_documento,
        "regex": patron,
        "respuesta": respuesta
    }
    respuesta1_servidor = requests.post(url, json=data)

    codigo_respuesta = respuesta1_servidor.json()["proceso"]


    return codigo_respuesta
