from typing import List, Dict
import random


def contar_palabras(texto:str, archivo:str) -> Dict[str, Dict[str, int]]:
    """Dado un texto y un archivo, cuenta la cantidad de veces que aparecen las palabras del texto en dicho archivo."""
    dic = {}
    palabras_a_encontrar = set(texto.split())
    if not palabras_a_encontrar:
        return dic
    with open(archivo) as archivo:
        for linea in archivo:
            datos = linea.rstrip('\n')
            datos = datos_procesados(datos)
            if not datos:
                continue
            autor, mensaje = datos
            dic[autor] = dic.get(autor, {})
            for palabra in mensaje:
                if palabra in palabras_a_encontrar:
                    dic[autor][palabra] = dic[autor].get(palabra, 0) + 1
    for autor, palabras in dic.items():
        for palabra in palabras_a_encontrar:
            dic[autor][palabra] = dic[autor].get(palabra, 0)
    return dic


def datos_procesados(datos:str) -> str|List[str]:
    """Dado una cadena, devuelve un str(autor) y una lista de str(mensaje)"""
    datos = datos.split('-')
    if len(datos) < 2:
        return
    elif len(datos) == 2:
        fecha, datos = datos
        if not ':' in datos:
            return
        datos = datos.split(':')
        autor = datos[0]
        mensaje = " ".join(datos[1:])
    elif len(datos) >= 3:
        datos = (" ".join(datos[1:])).split(':')
        autor = datos[0]
        mensaje = " ".join(datos[1:])
    autor = autor.lstrip(' ')
    mensaje = mensaje.lstrip(' ').lower().split()
    return autor, mensaje


def generar_reporte(palabras_por_autor: Dict[str, Dict[str, int]], nombre_archivo_destino:str) -> None:
    """Dado un diccionario con autores|palabras y un nombre de archivo, genera un reporte y lo guarda con dicho nombre de archivo"""
    with open(nombre_archivo_destino, 'w') as archivo:
        header = archivo.write('contacto,palabra,frecuencia\n')
        for autor, palabras in palabras_por_autor.items():
            for palabra, frecuencia in palabras.items():
                archivo.write(f'{autor},{palabra},{frecuencia}\n')
    print()
    print('Reporte generado!')


def cadenas_de_markov(archivo:str) -> Dict[str, Dict[str, Dict[str, int]]]:
    """Dado un archivo, genera un diccionario de diccionarios de diccionarios."""
    cadenas = {}
    with open(archivo) as archivo:
        for linea in archivo:
            datos = linea.rstrip('\n')
            datos = datos_procesados(datos)
            if not datos:
                continue
            autor, palabras = datos
            if " ".join(palabras) == '<multimedia omitido>' or len(palabras) < 3:
                continue  
            cadenas[autor] = cadenas.get(autor, {})
            cadenas[autor]['comienzo de oracion'] = cadenas[autor].get('comienzo de oracion', {})
            for i in range(1, len(palabras)):
                anterior = palabras[i - 1]
                actual = palabras[i]
                if i == 1:
                    cadenas[autor]['comienzo de oracion'][anterior] = cadenas[autor]['comienzo de oracion'].get(anterior, 0) + 1
                    cadenas[autor][anterior] = cadenas[autor].get(anterior, {})
                    cadenas[autor][anterior][actual] = cadenas[autor][anterior].get(actual, 0) + 1
                elif i == len(palabras) - 1:
                    cadenas[autor][actual] = cadenas[autor].get(actual, {})
                    cadenas[autor][actual]['fin de oracion'] = cadenas[autor][actual].get('fin de oracion', 0) + 1
                else:
                    cadenas[autor][anterior] = cadenas[autor].get(anterior, {})
                    cadenas[autor][anterior][actual] = cadenas[autor][anterior].get(actual, 0) + 1
    return cadenas


def contactos(cadenas:Dict[str, Dict[str, Dict[str, int]]]) -> List[str]:
    """Dado un diccionario de diccionarios de diccionarios, devuelve una lista con todos los contactos presentes en dicho diccionario"""
    contactos = []
    for contacto in cadenas.keys():
        contactos.append(contacto)
    contactos.append('Salir')
    return contactos


def generar_mensaje(cadenas:Dict[str, Dict[str, Dict[str, int]]], contacto:str) -> str:
    """Dado un diccionario de diccionarios de diccionarios y un contacto, genera un mensaje pseudo-aleatorio simulando dicho contacto."""
    longitud_maxima = 15
    mensaje = []
    palabra_actual = 'comienzo de oracion'
    for _ in range(longitud_maxima - 1):
            if not palabra_actual in cadenas[contacto]:
                break
            palabras = list(cadenas[contacto][palabra_actual].keys())
            probabilidades = list(cadenas[contacto][palabra_actual].values())
            palabra_actual = random.choices(palabras, weights=probabilidades, k=1)[0]
            if palabra_actual == 'comienzo de oracion':
                continue
            elif palabra_actual == 'fin de oracion':
                break
            mensaje.append(palabra_actual)
    return " ".join(mensaje)