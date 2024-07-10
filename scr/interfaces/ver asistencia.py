import tkinter as tk
from tkinter import ttk
from modulos.base_datos import obtener_asistencias  # Función para obtener asistencias desde la base de datos

class VerAsistencia:
    def __init__(self, master):
        self.master = master
        self.master.title("Ver Asistencia")

        # Crear una tabla para mostrar asistencias
        self.tree = ttk.Treeview(self.master, columns=("DNI", "Fecha"), show='headings')
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.pack(padx=10, pady=10)

        # Cargar los datos
        self.cargar_datos()

    def cargar_datos(self):
        datos = obtener_asistencias()
        for fila in datos:
            self.tree.insert("", tk.END, values=fila)
