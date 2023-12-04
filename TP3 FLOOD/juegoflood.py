from flood import Flood
from pila import Pila
from cola import Cola


class JuegoFlood:
    """
    Clase para administrar un Flood, junto con sus estados y acciones
    """

    def __init__(self, alto, ancho, n_colores):
        """
        Genera un nuevo JuegoFlood, el cual tiene un Flood y otros
        atributos para realizar las distintas acciones del juego.

        Argumentos:
            alto, ancho (int): Tamaño de la grilla del Flood.
            n_colores: Cantidad maxima de colores a incluir en la grilla.
        """
        self.flood = Flood(alto, ancho)
        self.flood.mezclar_tablero(n_colores)
        self.mejor_n_movimientos, _ = self._calcular_movimientos()
        self.n_movimientos = 0
        self.pasos_solucion = Cola()
        self.pila_deshacer = Pila()
        self.pila_rehacer = Pila()


    def cambiar_color(self, color):
        """
        Realiza la acción para seleccionar un color en el Flood, sumando a la
        cantidad de movimientos realizados y manejando las estructuras para
        deshacer y rehacer

        Argumentos:
            color (int): Nuevo color a seleccionar
        """
        tablero_ant = self.flood.clonar().tablero
        tablero_act = self.flood.clonar()
        tablero_act.cambiar_color(color)
        tablero_act = tablero_act.tablero
        if not tablero_ant == tablero_act:
            estado_act = self.flood.clonar()
            self.pila_deshacer.apilar(estado_act)
            self.flood.cambiar_color(color)
            self.n_movimientos += 1
        while not self.pila_rehacer.esta_vacia():
            self.pila_rehacer.desapilar()
        if not self.pasos_solucion.esta_vacia() and self.pasos_solucion.ver_frente() == color:
            self.pasos_solucion.desencolar()
        else:
            self.pasos_solucion = Cola()


    def deshacer(self):
        """
        Deshace el ultimo movimiento realizado si existen pasos previos,
        manejando las estructuras para deshacer y rehacer.
        """
        if not self.pila_deshacer.esta_vacia():
            estado_act = self.flood.clonar()
            self.pila_rehacer.apilar(estado_act)
            self.flood = self.pila_deshacer.desapilar().clonar()
            self.n_movimientos -= 1
            self.pasos_solucion = Cola()


    def rehacer(self):
        """
        Rehace el movimiento que fue deshecho si existe, manejando las
        estructuras para deshacer y rehacer.
        """
        if not self.pila_rehacer.esta_vacia():
            estado_act = self.flood.clonar()
            self.pila_deshacer.apilar(estado_act)
            self.flood = self.pila_rehacer.desapilar().clonar()
            self.n_movimientos += 1
            self.pasos_solucion = Cola()
            

    def _calcular_movimientos(self):
        """
        Realiza una solución de pasos contra el Flood actual (en una Cola)
        y devuelve la cantidad de movimientos que llevó a esa solución.

        CRITERIO:
                Busqueda del color que agrega la mayor cantidad de area del mismo color al Flood.
                
        Devuelve:
            int: Cantidad de movimientos que llevó a la solución encontrada.
            Cola: Pasos utilizados para llegar a dicha solución
        """
        clon = self.flood.clonar()
        numero_de_mov, pasos = clon.camino_mas_corto()
        return numero_de_mov, pasos


    def hay_proximo_paso(self):
        """
        Devuelve un booleano indicando si hay una solución calculada
        """
        return not self.pasos_solucion.esta_vacia()


    def proximo_paso(self):
        """
        Si hay una solución calculada, devuelve el próximo paso.
        Caso contrario devuelve ValueError

        Devuelve:
            Color del próximo paso de la solución
        """
        return self.pasos_solucion.ver_frente()


    def calcular_nueva_solucion(self):
        """
        Calcula una secuencia de pasos que solucionan el estado actual
        del flood, de tal forma que se pueda llamar al método `proximo_paso()`
        """
        _, self.pasos_solucion = self._calcular_movimientos()


    def dimensiones(self):
        return self.flood.dimensiones()


    def obtener_color(self, fil, col):
        return self.flood.obtener_color(fil, col)


    def obtener_posibles_colores(self):
        return self.flood.obtener_posibles_colores()


    def esta_completado(self):
        return self.flood.esta_completado()