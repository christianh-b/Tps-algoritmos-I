import random
from pila import *
from cola import *


class Flood:
    """
    Clase para administrar un tablero de N colores.
    """

    def __init__(self, alto, ancho):
        """
        Genera un nuevo Flood de un mismo color con las dimensiones dadas.

        Argumentos:
            alto, ancho (int): Tamaño de la grilla.
        """
        self.alto = alto
        self.ancho = ancho
        self.tablero = self.generar_tablero()
        self.n_colores = None
    
    
    def generar_tablero(self):
        """
        Genera un nuevo tablero de n filas y m columnas.
        """
        tablero = []
        for fil in range(self.alto):
            fila = []
            for col in range(self.ancho):
                fila.append(0)
            tablero.append(fila)
        return tablero


    def mezclar_tablero(self, n_colores):
        """
        Asigna de forma completamente aleatoria hasta `n_colores` a lo largo de
        las casillas del tablero.

        Argumentos:
            n_colores (int): Cantidad maxima de colores a incluir en la grilla.
        """
        colores = list(range(n_colores))
        self.n_colores = sorted(list(range(n_colores)))
        for fil in range(self.alto):
            for col in range(self.ancho):
                self.tablero[fil][col] = random.choice(colores)


    def obtener_color(self, fil, col):
        """
        Devuelve el color que se encuentra en las coordenadas solicitadas.

        Argumentos:
            fil, col (int): Posiciones de la fila y columna en la grilla.

        Devuelve:
            Color asignado.
        """
        return self.tablero[fil][col]


    def obtener_posibles_colores(self):
        """
        Devuelve una secuencia ordenada de todos los colores posibles del juego.
        La secuencia tendrá todos los colores posibles que fueron utilizados
        para generar el tablero, sin importar cuántos de estos colores queden
        actualmente en el tablero.

        Devuelve:
            iterable: secuencia ordenada de colores.
        """
        return self.n_colores


    def dimensiones(self):
        """
        Dimensiones de la grilla (filas y columnas)

        Devuelve:
            (int, int): alto y ancho de la grilla en ese orden.
        """
        return self.alto, self.ancho


    def cambiar_color(self, color_nuevo):
        """
        Asigna el nuevo color al Flood de la grilla. Es decir, a todas las
        coordenadas que formen un camino continuo del mismo color comenzando
        desde la coordenada origen en (0, 0) se les asignará `color_nuevo`

        Argumentos:
            color_nuevo: Valor del nuevo color a asignar al Flood.
        """
        color_actual = self.tablero[0][0]
        if not color_actual == color_nuevo:
            self._cambiar_color(color_actual, color_nuevo, 0, 0)
        return


    def _cambiar_color(self, color_actual, color_nuevo, fil, col):
        """
        Cambia el color de manera recursiva en todas las coordenadas conectadas del Flood.
        """
        if 0 <= fil < self.alto and 0 <= col < self.ancho:
            if self.tablero[fil][col] == color_actual:
                self.tablero[fil][col] = color_nuevo
                for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nueva_fil, nueva_col = fil + i, col + j
                    self._cambiar_color(color_actual, color_nuevo, nueva_fil, nueva_col)


    def clonar(self):
        """
        Devuelve:
            Flood: Copia del Flood actual
        """
        clon = Flood(self.alto, self.ancho)
        clon.n_colores = self.n_colores
        clon.tablero = self.clonar_tablero()
        return clon
    
    
    def clonar_tablero(self):
        """
        Crea una copia del tablero del flood.
        
        Devuelve una nueva instancia del tablero del flood
        """
        tablero_clonado = []
        for fil in self.tablero:
            fila_clonada = []
            for col in fil:
                fila_clonada.append(col)
            tablero_clonado.append(fila_clonada)
        return tablero_clonado


    def esta_completado(self):
        """
        Indica si todas las coordenadas de grilla tienen el mismo color

        Devuelve:
            bool: True si toda la grilla tiene el mismo color
        """
        color_actual = self.tablero[0][0]
        for fil in self.tablero:
            for col in fil:
                if not col == color_actual:
                    return False
        return True


    def camino_mas_corto(self):
        """
        Encuentra el camino para completar el flood en la menor cantidad de pasos.
        
        Devuelve una tupla de la forma (int, Cola)
        """
        pasos = Cola()
        numero_de_mov = 0
        while not self.esta_completado():
            color, area = self.color_con_area_maxima()
            self.cambiar_color(color)
            pasos.encolar(color)
            numero_de_mov += 1
        return numero_de_mov, pasos
        
    
    def color_con_area_maxima(self):
        """
        Encuentra el color que agrega la mayor cantidad de area al flood.
        
        Devuelve una tupla de la forma (int, int).
        """
        colores = self.obtener_posibles_colores()
        area_inicial = self.clonar().calcular_area(0, 0, {})
        mejor_color = colores[0]
        mejor_area = area_inicial
        for color in colores:
            clon = self.clonar()
            clon.cambiar_color(color)
            area = clon.calcular_area(0, 0, {})
            if area + area_inicial > mejor_area:
                mejor_color = color
                mejor_area = area + area_inicial
        return mejor_color, mejor_area


    def calcular_area(self, fil, col, dicc):
        """
        Calcula el area del flood contando todas las coordenadas conectadas del mismo color.
        
        Devuelve un resultado de tipo int.
        """
        color_actual = self.tablero[0][0]
        resultado = 0
        if 0 <= fil < self.alto and 0 <= col < self.ancho:
            if self.tablero[fil][col] == color_actual and (fil, col) not in dicc:
                dicc[(fil, col)] = 1
                resultado = 1
                for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    resultado += self.calcular_area(fil + i, col + j, dicc)
        return resultado