class NodoPrioridad:
    def __init__(self, dato, prioridad: int):
        self.dato = dato
        self.prioridad = prioridad  # Menor número = Mayor prioridad (ej. 1: Alta, 2: Normal)
        self.siguiente = None

class ColaPrioridad:
    """Implementación de Cola de Prioridad basada en listas enlazadas ordenadas."""
    def __init__(self):
        self.frente = None
        self._tamanio = 0

    def esta_vacia(self) -> bool:
        return self.frente is None

    def encolar(self, dato, prioridad: int = 2):
        nuevo_nodo = NodoPrioridad(dato, prioridad)
        if self.esta_vacia() or prioridad < self.frente.prioridad:
            nuevo_nodo.siguiente = self.frente
            self.frente = nuevo_nodo
        else:
            actual = self.frente
            while actual.siguiente and actual.siguiente.prioridad <= prioridad:
                actual = actual.siguiente
            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo
        self._tamanio += 1

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola de prioridad está vacía.")
        dato = self.frente.dato
        self.frente = self.frente.siguiente
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