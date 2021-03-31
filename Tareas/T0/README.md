# Tarea 0: DCConecta2 :school_satchel:

### Cosas implementadas y no implementadas :white_check_mark: :x:

  

* <Menú de inicio<sub>1</sub>>: Hecha completa

* <Menú de chats<sub>1</sub>>: Hecha completa

* <Menú de contactos<sub>1</sub>>: Hecha completa

* <Menú de grupos<sub>1</sub>>: Hecha completa

* <Chats<sub>1</sub>>: Hecha completa

* <Archivos<sub>1</sub>>: Hecha completa
  

## Ejecución :computer:

El módulo principal de la tarea a ejecutar es ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:

1.  ```grupos.csv``` en ```T0```

2.  ```mensajes.csv``` en ```T0```

3.  ```usuarios.csv``` en ```T0```

4.  ```contactos.csv``` en ```T0```

5.  ```parametros.py``` en ```T0```

  

## Librerías :books:

### Librerías externas utilizadas

La lista de librerías externas que utilicé fue la siguiente:

  

1.  ```datetime```: ```función now() e instancias month, day, year, hour, minute, second // módulo datetime```

2.  ```collections```: ```función defaultdict``` 

### Librerías propias

Por otro lado, los módulos que fueron creados fueron los siguientes:

  

1.  ```registro_e_inicio_de_sesion.py```: Contiene a ```funcion_interfaz_menu()```, ```funcion_iniciar_sesion()```, ```funcion_registrar_usuario()```

2.  ```menú_de_chats.py```: Contiene a ```interfaz_menu_de_chats()```, ```menu_de_chats()```

3.  ```menú_contactos.py```: Contiene a ```menu_contactos()```

4.  ```ver_contactos.py```: Contiene a ```ver_contactos()```

5.  ```anadir_contacto.py```: Contiene a ```anadir_contacto()```

6. ```menú_grupos.py```: Contiene a ```menu_grupos()```

7. ```ver_grupos.py```: Contiene a ```ver_grupos()```

8. ```anadir_grupo.py```: Contiene a ```anadir_grupo()```

9. ```abrir_chat.py```: Contiene a ```Clase Mensaje```, ```Clase Fecha```, ```abrir_chat()```, ```abrir_chat_regular()```, ```abrir_chat_grupal()```, ```escribir_mensaje()```, ```sacar_de_grupo()```, ```ordenar_mensajes()```, ```unir_mensajes_con_coma()```

10.  ```funciones_recurrentes.py```: Contiene a ```respuesta_invalida_seguir()```
## Funcionamiento general

El funcionamiento de este código consiste en una seguidilla de funciones iniciadas con el archivo main.py, en donde cada una está interconectada con las otras mediante un cierto tipo de recursividad y llamados entre ellas. Cada función que no se entiende a simple vista tiene una seguidilla de comentarios, con el formato "#  _comentario_", que indican lo que hace el código que viene justo después de este. 


## Supuestos y consideraciones adicionales :thinking:

Los supuestos que realicé durante la tarea son los siguientes:

  

1. Los archivos están configurados tal como aparece en el enunciado de T0, donde cada línea existente es de la forma en que se dice allí, esto es válido porque así lo estipula la actividad.

2. Python ejecuta el código lo suficientemente rápido para que la hora sea la misma desde que se llama a la función, hasta que se guarda en las variables para imprimir.

3.  	En las frases armadas mediante concatenación de strings, cada término de la suma se escribió sin espacios para facilitar la lectura.

## Referencias de código externo :book:

  

Para realizar mi tarea saqué código de:

1. \<https://docs.python.org/es/3/library/datetime.html>: esta función permite conocer la fecha y hora en la que se ejecuta cierta parte del código. Está implementado en el archivo <abrir_chat.py>, en las líneas 134 - 140.


## Descuentos

No pude lograr configurar el .gitignore :(