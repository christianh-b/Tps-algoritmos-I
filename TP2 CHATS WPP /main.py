import chats_de_whatsapp
from typing import List


def menu_principal() -> None:
    """Menu interactivo con el usuario"""
    print('*'*44)
    print(f"*  {'--- Menu Principal ---'.center(38)}  *")
    print(f"*  {' '*39} *")
    print(f"*  {'1. Contar palabras por contacto'}{' '*7}  *")
    print(f"*  {'2. Generar un mensaje pseudo-aleatorio'}  *")
    print(f"*  {'3. Salir del programa'}{' '*17}  *")
    print('*'*44)
    print()


def pedir_ruta() -> str:
    """Le pide al usuario la ruta donde se encuentra el archivo de chat que desea cargar.
    Lanza FileNotFoundError si no se encuentra el archivo."""
    while True:
        try:
            ruta_archivo = input('Ingrese la ruta donde se encuentra su archivo de chat: ')
            with open(ruta_archivo, 'r') as archivo:
                primera_linea = archivo.readline()
            print()
            print('Archivo cargado correctamente!')
            return ruta_archivo
        except FileNotFoundError:
            print('Archivo no encontrado')
            opcion = input('Desea introducir otra ruta? (s/n): ').lower()
            if opcion == 'n':
                return


def elegir_opcion() -> int:
    """Le pide al usuario que seleccione una de las opciones a realizar."""
    while True:
        opcion = input('Seleccione una opcion: ')
        if not opcion.isdigit():
            print('Opcion invalida')
            continue
        opcion = int(opcion)
        if not 1 <= opcion <= 3:
            print('Opcion no encontrada')
            continue
        return opcion
    
    
def pedir_palabras() -> str:
    """Le pide al usuario que ingrese una serie de palabras."""
    palabras = input('Ingrese las palabras para contar entre contactos: ')
    return palabras


def pedir_destino() -> str:
    """Le pide al usuario que ingrese el nombre del archivo de destino."""
    nombre_archivo = input('Ingrese el archivo destino para guardar el reporte: ')
    print()
    if not nombre_archivo:
        print('No se especifico ninguna ruta de destino')
        print()
        return
    elif ' ' in nombre_archivo or not '.' in nombre_archivo:
        print('El nombre del archivo de destino es invalido')
        print()
        return
    if not nombre_archivo.split('.')[1] == 'csv':
        print('El archivo de destino no tiene una extension valida')
        print()
        return
    return nombre_archivo


def elegir_contacto(contactos:List[str]) -> str:
    """Dado una lista de contactos, le pide al usuario que seleccione un contacto de dicha lista."""
    print('Contactos: ')
    for i, c in enumerate(contactos):
        print(f"{' '*8}{i}. {c}")
    print()
    while True:
        numero = input('Ingrese el contacto que desea simular: ')
        if not numero.isdigit():
            print('Opcion invalida')
            continue
        numero = int(numero)
        if not 0 <= numero < len(contactos):
            print('Usuario no encontrado')
            continue
        return contactos[numero]


def aviso() -> None:
    """Imprime por pantalla un mensaje avisando que el programa finalizo correctamente."""
    print('Programa finalizado con exito!')

    
def main():
    archivo = pedir_ruta()
    if not archivo:
        aviso()
        return
    print()
    while True:
        menu_principal()
        opcion = elegir_opcion()
        if opcion == 1:
            palabras = pedir_palabras()
            destino = pedir_destino()
            if not destino:
                continue
            palabras_por_contacto = chats_de_whatsapp.contar_palabras(palabras, archivo)
            chats_de_whatsapp.generar_reporte(palabras_por_contacto, destino)
            print()
        if opcion == 2:
            cadenas = chats_de_whatsapp.cadenas_de_markov(archivo)
            contacto_a_elegir = chats_de_whatsapp.contactos(cadenas)
            while True:
                print()
                contacto_elegido = elegir_contacto(contacto_a_elegir)
                if contacto_elegido.lower() == 'salir':
                    print()
                    break
                mensaje = chats_de_whatsapp.generar_mensaje(cadenas, contacto_elegido)
                print()
                print(f'"""{contacto_elegido}: {mensaje}"""')
        if opcion == 3:
            print()
            aviso()
            return
main()