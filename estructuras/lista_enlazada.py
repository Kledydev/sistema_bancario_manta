class NodoLista:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    """Implementación de Lista Enlazada para registrar el historial de transacciones."""
    def __init__(self):
        self.cabeza = None
        self._tamanio = 0

    def esta_vacia(self) -> bool:
        return self.cabeza is None

    def agregar_al_final(self, dato):
        nuevo_nodo = NodoLista(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self._tamanio += 1

    def buscar(self, criterio_func) -> list:
        """Busca elementos que cumplan con una función criterio (lambda)."""
        resultados = []
        actual = self.cabeza
        while actual:
            if criterio_func(actual.dato):
                resultados.append(actual.dato)
            actual = actual.siguiente
        return resultados

    def obtener_elementos(self) -> list:
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __len__(self):
        return self._tamanio