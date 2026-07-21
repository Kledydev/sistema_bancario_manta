from datetime import datetime

class Transaccion:
    """Clase que representa una operación realizada en ventanilla."""
    def __init__(self, id_transaccion: int, cliente: object, ventanilla: int, tipo_operacion: str, monto: float = 0.0):
        self.id_transaccion = id_transaccion
        self.cliente = cliente
        self.ventanilla = ventanilla
        self.tipo_operacion = tipo_operacion
        self.monto = monto
        self.fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"[{self.fecha_hora}] Transacción #{self.id_transaccion} - Ventanilla {self.ventanilla} | Cliente: {self.cliente.nombre} | Op: {self.tipo_operacion} | Monto: ${self.monto:.2f}"