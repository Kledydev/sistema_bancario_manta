class NodoCola:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ColaFIFO:
    """Implementación propia de una Cola FIFO basada en nodos."""
    def __init__(self):
        self.frente = None
        self.final = None
        self._tamanio = 0

    def esta_vacia(self) -> bool:
        return self.frente is None

    def encolar(self, dato):
        nuevo_nodo = NodoCola(dato)
        if self.esta_vacia():
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self._tamanio += 1

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía.")
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self._tamanio -= 1
        return dato

    def obtener_elementos(self) -> list:
        elementos = []
        actual = self.frente
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __len__(self):
        return self._tamanio