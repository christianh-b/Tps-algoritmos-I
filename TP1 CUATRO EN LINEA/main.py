import cuatro_en_linea


def main():
    ancho, alto = cuatro_en_linea.dimensiones_tablero()
    tablero = cuatro_en_linea.crear_tablero(alto, ancho)
    cuatro_en_linea.jugar(tablero)
    
main()