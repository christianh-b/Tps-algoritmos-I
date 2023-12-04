from typing import List

SIMBOLO_O = 'o'
SIMBOLO_X = 'x'


def crear_tablero(n_filas: int, n_columnas: int) -> List[List[str]]:
    """Crea un nuevo tablero de cuatro en línea, con dimensiones
    n_filas por n_columnas.
    Para todo el módulo `cuatro_en_linea`, las cadenas reconocidas para los
    valores de la lista de listas son las siguientes:
        - Celda vacía: ' '
        - Celda con símbolo X: 'X'
        - Celda con símbolo O: 'O'

    PRECONDICIONES:
        - n_filas y n_columnas son enteros positivos mayores a tres.

    POSTCONDICIONES:
        - la función devuelve un nuevo tablero lleno de casilleros vacíos
          que se puede utilizar para llamar al resto de las funciones del
          módulo.

    EJEMPLO:
        >>> crear_tablero(4, 5)
        [
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ']
        ]
    """
    tablero = []
    for f in range(n_filas):
        fila = []
        for c in range(n_columnas):
            fila.append(' ')
        tablero.append(fila)
    return tablero


def es_turno_de_x(tablero: List[List[str]]) -> bool:
    """Dado un tablero, devuelve True si el próximo turno es de X. Si, en caso
    contrario, es el turno de O, devuelve False.
    - Dado un tablero vacío, dicha función debería devolver `True`, pues el
      primer símbolo a insertar es X.
    - Luego de insertar el primer símbolo, esta función debería devolver `False`
      pues el próximo símbolo a insertar es O.
    - Luego de insertar el segundo símbolo, esta función debería devolver `True`
      pues el próximo símbolo a insertar es X.
    - ¿Qué debería devolver si hay tres símbolos en el tablero? ¿Y con cuatro
      símbolos?

    PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`
        - los símbolos del tablero fueron insertados previamente insertados con
          la función `insertar_simbolo`"""
    n_filas = len(tablero)
    n_columnas = len(tablero[0])
    cont_x = 0
    cont_o = 0
    for f in range(n_filas):
        for c in range(n_columnas):
            if tablero[f][c] == 'X':
                cont_x += 1
            elif tablero[f][c] == 'O':
                cont_o += 1
    return cont_x <= cont_o

                
def insertar_simbolo(tablero: List[List[str]], columna: int) -> bool:
    """Dado un tablero y un índice de columna, se intenta colocar el símbolo del
    turno actual en dicha columna.
    Un símbolo solo se puede colocar si el número de columna indicada por
    parámetro es válido, y si queda espacio en dicha columna.
    El número de la columna se encuentra indexado en 0, entonces `0` corresponde
    a la primer columna.

    PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`
    POSTCONDICIONES:
        - si la función devolvió `True`, se modificó el contenido del parámetro
          `tablero`. Caso contrario, el parámetro `tablero` no se vio modificado
    """
    ancho = len(tablero[0])
    c = columna
    if c < 0 or c >= ancho:
        return False
    for f in range(len(tablero)-1 ,-1, -1):
            if tablero[f][c] == ' ':
                if es_turno_de_x(tablero):
                    tablero[f][c] = 'X'
                else:
                    tablero[f][c] = 'O'
                return True
    return False
    

def tablero_completo(tablero: List[List[str]]) -> bool:
    """Dado un tablero, indica si se encuentra completo. Un tablero se considera
    completo cuando no hay más espacio para insertar un nuevo símbolo, en tal
    caso la función devuelve `True`.

    PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`
    """
    ancho = len(tablero[0])
    alto = len(tablero)
    for f in range(alto):
        for c in range(ancho):
            if tablero[f][c] == ' ':
                return False
    return True


def obtener_ganador(tablero: List[List[str]]) -> str:
    """Dado un tablero, devuelve el símbolo que ganó el juego.
    El símbolo ganador estará dado por aquel que tenga un cuatro en línea. Es
    decir, por aquel símbolo que cuente con cuatro casilleros consecutivos
    alineados de forma horizontal, vertical, o diagonal.
    En el caso que el juego no tenga ganador, devuelve el símbolo vacío.
    En el caso que ambos símbolos cumplan con la condición de cuatro en línea,
    la función devuelve cualquiera de los dos.

    PRECONDICIONES:
        - el parámetro `tablero` fue inicializado con la función `crear_tablero`

    EJEMPLO: para el siguiente tablero, el ganador es 'X' por tener un cuatro en
    línea en diagonal
        [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'X', 'O', ' ', ' ', ' '],
            [' ', ' ', 'O', 'X', ' ', ' ', ' '],
            [' ', ' ', 'X', 'O', 'X', ' ', ' '],
            [' ', 'O', 'O', 'X', 'X', 'X', 'O'],
        ]
    """
    ganador_horizontal = verificar_ganador_horizontal(tablero)
    if not ganador_horizontal == ' ':
        return ganador_horizontal
    ganador_vertical = verificar_ganador_vertical(tablero)
    if not ganador_vertical == ' ':
        return ganador_vertical
    ganador_diagonal = verificar_ganador_diagonal(tablero)
    if not ganador_diagonal == ' ':
        return ganador_diagonal 
    ganador_diagonal_inversa = verificar_ganador_diagonal_inversa(tablero)
    if not ganador_diagonal_inversa == ' ':
        return ganador_diagonal_inversa
    return ' '
    

# Chequear ganador en todas direcciones    

        
def verificar_ganador_horizontal(tablero: List[List[str]]) -> str:
    """Dado un tablero, verifica si hay un ganador en direcciones horizontales. 
    En tal caso, la función devuelve el símbolo ganador, si no hay ganador, 
    la función devuelve un espacio vacío."""
    alto = len(tablero)
    ancho = len(tablero[0])
    for c in range(ancho):
        for f in range(alto):
            if c + 3 < ancho:
                simbolo_1 = tablero[f][c]
                simbolo_2 = tablero[f][c + 1]
                simbolo_3 = tablero[f][c + 2]
                simbolo_4 = tablero[f][c + 3]
                if not simbolo_1 == ' ' and simbolo_1 == simbolo_2 == simbolo_3 == simbolo_4:
                    return simbolo_1
    return ' '


def verificar_ganador_vertical(tablero:List[List[str]]) -> str:
    """Dado un tablero, verifica si hay un ganador en direcciones verticales. En tal caso la funcion devuelve el simbolo ganador, si no hay ganador la funcion devuelve un espacio vacio."""
    alto = len(tablero)
    ancho = len(tablero[0])
    for c in range(ancho):
        for f in range(alto):
            if f + 3 < alto:
                simbolo_1 = tablero[f][c]
                simbolo_2 = tablero[f + 1][c]
                simbolo_3 = tablero[f + 2][c]
                simbolo_4 = tablero[f + 3][c]
                if not simbolo_1 == ' ' and simbolo_1 == simbolo_2 == simbolo_3 == simbolo_4:
                    return simbolo_1
    return ' '


def verificar_ganador_diagonal(tablero:List[List[str]]) -> str:
    """Dado un tablero, verifica si hay un ganador en direcciones diagonales. En tal caso la funcion devuelve el simbolo ganador, si no hay ganador la funcion devuelve un espacio vacio."""
    alto = len(tablero)
    ancho = len(tablero[0])
    for f in range(alto):
        for c in range(ancho):
            if c + 3 < ancho and f + 3 < alto:
                simbolo_1 = tablero[f][c]
                simbolo_2 = tablero[f + 1][c + 1]
                simbolo_3 = tablero[f + 2][c + 2]
                simbolo_4 = tablero[f + 3][c + 3]
                if not simbolo_1 == ' ' and simbolo_1 == simbolo_2 == simbolo_3 == simbolo_4:
                    return simbolo_1
    return ' '


def verificar_ganador_diagonal_inversa(tablero:List[List[str]]) -> str:
    """Dado un tablero, verifica si hay un ganador en direcciones diagonales inversas. En tal caso la funcion devuelve el simbolo ganador, si no hay ganador la funcion devuelve un espacio vacio."""
    alto = len(tablero)
    ancho = len(tablero[0])
    for f in range(alto - 3):
        for c in range(3, ancho):
            if c - 3 >= 0:
                simbolo_1 = tablero[f][c]
                simbolo_2 = tablero[f + 1][c - 1]
                simbolo_3 = tablero[f + 2][c - 2]
                simbolo_4 = tablero[f + 3][c - 3]
                if not simbolo_1 == ' ' and simbolo_1 == simbolo_2 == simbolo_3 == simbolo_4:
                    return simbolo_1
    return ' '


# Validaciones Usuario


def dimensiones_tablero() -> int|int:
    """La funcion valida las dimensiones(ancho y alto) que ingresa el usuario."""
    while True:
        ancho = input('Ingrese el ancho del juego entre 4 y 10: ')
        if ancho.isdigit() and validar_ancho_alto(ancho):
            ancho = int(ancho)
            break
    while True:
        alto = input('Ingrese el alto del juego entre 4 y 10:  ')
        if alto.isdigit() and validar_ancho_alto(alto):
            alto = int(alto)
            break
    return ancho, alto
    

def validar_ancho_alto(dimension:int) -> bool:
    """La funcion valida que la dimension que recibe por parametro se encuentre dentro del limite permitido."""
    return 4 <= int(dimension) <= 10
    
# Tablero con formato


def imprimir_tablero(tablero:List[List[str]]) -> None:
    """Dado un tablero, imprime dicho tablero con un formato agradable para el usuario."""
    ancho = len(tablero[0])
    alto = len(tablero)
    print()
    for i in range(ancho):
            print(f'{i} |', end=' ')
    print()
    print('____'*ancho)
    print()
    for f in range(alto):
        for c in range(ancho):
            print(f'{tablero[f][c]} |', end=' ')
        print()
    print()


# Jugar cuatro en linea

            
def jugar(tablero:List[List[str]]) -> None:
    """Dado un tablero, permite llevar a cabo una partida del juego cuatro en linea."""
    columnas = len(tablero[0]) - 1
    while not tablero_completo(tablero):
        imprimir_tablero(tablero)
        if es_turno_de_x(tablero):
            print(f'Columna para insertar X entre 0 y {columnas}')
        else:
            print(f'Columna para insertar O entre 0 y {columnas}')
        print(f"O ingrese 's' para salir")
        print()
        entrada = input('Entrada: ')
        print()
        if entrada == 's':
            print('Partida finalizada')
            return
        if not entrada.isdigit() or not 0 <= int(entrada) <= columnas:
            print('Opcion invalida')
            continue
        insertar = insertar_simbolo(tablero, int(entrada))
        ganador = obtener_ganador(tablero)
        if not ganador == ' ':
            imprimir_tablero(tablero)
            print(f"Ganó {ganador}!")
            break    


            
            
        
    

