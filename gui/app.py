import tkinter as tk
from tkinter import ttk, messagebox
from estructuras.cola_fifo import ColaFIFO
from estructuras.cola_prioridad import ColaPrioridad
from estructuras.lista_enlazada import ListaEnlazada
from modelos.cliente import Cliente
from modelos.transaccion import Transaccion

class SistemaBancarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Atención Bancaria - Sucursal Manta")
        self.root.geometry("950x650")

        self.cola_regular = ColaFIFO()
        self.cola_prioridad = ColaPrioridad()
        self.historial_operaciones = ListaEnlazada()
        self.contador_transacciones = 1

        self._crear_interfaz()

    def _crear_interfaz(self):
        # Panel Superior: Registro
        frame_registro = ttk.LabelFrame(self.root, text=" Registro de Cliente ")
        frame_registro.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_registro, text="ID / Cédula:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(frame_registro, width=15)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_registro, text="Nombre:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(frame_registro, width=20)
        self.entry_nombre.grid(row=0, column=3, padx=5, pady=5)

        self.var_prioridad = tk.BooleanVar()
        chk_prioridad = ttk.Checkbutton(frame_registro, text="¿Atención Preferencial?", variable=self.var_prioridad, command=self._toggle_condicion)
        chk_prioridad.grid(row=0, column=4, padx=5, pady=5)

        ttk.Label(frame_registro, text="Tipo:").grid(row=0, column=5, padx=5, pady=5)
        self.combo_condicion = ttk.Combobox(frame_registro, values=["Tercera Edad", "Discapacidad"], state="disabled", width=15)
        self.combo_condicion.grid(row=0, column=6, padx=5, pady=5)

        btn_agregar = ttk.Button(frame_registro, text="Encolar Cliente", command=self._registrar_cliente)
        btn_agregar.grid(row=0, column=7, padx=10, pady=5)

        # Panel Central: Colas
        frame_colas = ttk.Frame(self.root)
        frame_colas.pack(fill="both", expand=True, padx=10, pady=5)

        frame_prio = ttk.LabelFrame(frame_colas, text=" ⭐ Cola de Prioridad (Normativa EC) ")
        frame_prio.pack(side="left", fill="both", expand=True, padx=5)
        self.list_prioritaria = tk.Listbox(frame_prio, bg="#fff3cd")
        self.list_prioritaria.pack(fill="both", expand=True, padx=5, pady=5)

        frame_reg = ttk.LabelFrame(frame_colas, text=" 👤 Cola Regular (FIFO) ")
        frame_reg.pack(side="right", fill="both", expand=True, padx=5)
        self.list_regular = tk.Listbox(frame_reg, bg="#e2e3e5")
        self.list_regular.pack(fill="both", expand=True, padx=5, pady=5)

        # Panel de Atención
        frame_atencion = ttk.LabelFrame(self.root, text=" Atención en Ventanilla ")
        frame_atencion.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_atencion, text="Ventanilla N°:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_ventanilla = ttk.Combobox(frame_atencion, values=["1", "2", "3"], width=5, state="readonly")
        self.combo_ventanilla.current(0)
        self.combo_ventanilla.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_atencion, text="Operación:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_operacion = ttk.Combobox(frame_atencion, values=["Depósito", "Retiro", "Consulta"], width=12, state="readonly")
        self.combo_operacion.current(0)
        self.combo_operacion.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_atencion, text="Monto ($):").grid(row=0, column=4, padx=5, pady=5)
        self.entry_monto = ttk.Entry(frame_atencion, width=10)
        self.entry_monto.insert(0, "0.00")
        self.entry_monto.grid(row=0, column=5, padx=5, pady=5)

        btn_atender = ttk.Button(frame_atencion, text="Atender Siguiente Cliente", command=self._atender_cliente)
        btn_atender.grid(row=0, column=6, padx=15, pady=5)

        # Panel Inferior: Historial
        frame_historial = ttk.LabelFrame(self.root, text=" 📂 Historial de Operaciones (Lista Enlazada) ")
        frame_historial.pack(fill="both", expand=True, padx=10, pady=5)

        self.list_historial = tk.Listbox(frame_historial, bg="#d1e7dd")
        self.list_historial.pack(fill="both", expand=True, padx=5, pady=5)

    def _toggle_condicion(self):
        if self.var_prioridad.get():
            self.combo_condicion.config(state="readonly")
            self.combo_condicion.current(0)
        else:
            self.combo_condicion.config(state="disabled")

    def _registrar_cliente(self):
        cid = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        es_prio = self.var_prioridad.get()
        condicion = self.combo_condicion.get() if es_prio else "Ninguna"

        if not Cliente.es_cedula_valida(cid):
            messagebox.showerror("Cédula Inválida", "La cédula debe contener exactamente 10 dígitos numéricos.")
            return

        if not nombre:
            messagebox.showwarning("Error de Entrada", "Por favor ingrese el nombre del cliente.")
            return

        cliente = Cliente(cid, nombre, es_prio, condicion)

        if es_prio:
            self.cola_prioridad.encolar(cliente, prioridad=1)
        else:
            self.cola_regular.encolar(cliente)

        self._limpiar_entradas_cliente()
        self._actualizar_vistas_colas()

    def _atender_cliente(self):
        cliente = None
        if not self.cola_prioridad.esta_vacia():
            cliente = self.cola_prioridad.desencolar()
        elif not self.cola_regular.esta_vacia():
            cliente = self.cola_regular.desencolar()
        else:
            messagebox.showinfo("Atención", "No hay clientes en espera.")
            return

        ventanilla = int(self.combo_ventanilla.get())
        operacion = self.combo_operacion.get()
        try:
            monto = float(self.entry_monto.get())
        except ValueError:
            monto = 0.0

        transaccion = Transaccion(self.contador_transacciones, cliente, ventanilla, operacion, monto)
        self.historial_operaciones.agregar_al_final(transaccion)
        self.contador_transacciones += 1

        self._actualizar_vistas_colas()
        self._actualizar_vista_historial()
        messagebox.showinfo("Éxito", f"Cliente {cliente.nombre} atendido en Ventanilla {ventanilla}.")

    def _actualizar_vistas_colas(self):
        self.list_prioritaria.delete(0, tk.END)
        for c in self.cola_prioridad.obtener_elementos():
            self.list_prioritaria.insert(tk.END, str(c))

        self.list_regular.delete(0, tk.END)
        for c in self.cola_regular.obtener_elementos():
            self.list_regular.insert(tk.END, str(c))

    def _actualizar_vista_historial(self):
        self.list_historial.delete(0, tk.END)
        for t in self.historial_operaciones.obtener_elementos():
            self.list_historial.insert(tk.END, str(t))

    def _limpiar_entradas_cliente(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.var_prioridad.set(False)
        self._toggle_condicion()
