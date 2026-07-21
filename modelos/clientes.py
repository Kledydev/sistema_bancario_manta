class Cliente:
    """Modelo que representa a un cliente del banco."""
    def __init__(self, id_cliente: str, nombre: str, es_prioritario: bool = False, condicion: str = "Ninguna"):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.es_prioritario = es_prioritario
        self.condicion = condicion

    @staticmethod
    def es_cedula_valida(cedula: str) -> bool:
        """Valida que sea un número de cédula ecuatoriana válido (10 dígitos)."""
        return cedula.isdigit() and len(cedula) == 10

    def __str__(self):
        tipo = f"Prioritario ({self.condicion})" if self.es_prioritario else "Regular"
        return f"[{self.id_cliente}] {self.nombre} - {tipo}"
