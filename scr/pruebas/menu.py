import tkinter as tk
from PIL import Image, ImageTk
import os

class App:
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x600")
        self.crear_menu_superior()

    def crear_menu_superior(self):
        self.frame_menu = tk.Frame(self.master, bg="black", height=50)
        self.frame_menu.pack(side="top", fill="x")

        # Carpeta de iconos
        carpeta_iconos = os.path.join(os.path.dirname(__file__), 'pictures')

        # Opciones del menú principal con colores personalizados
        opciones_principales = [
            ("Reportes", self.mostrar_reportes_por_dia, "red", os.path.join(carpeta_iconos, "logo_dia.png")),
            ("Reporte Semanal", self.mostrar_reporte_semanal, "green", os.path.join(carpeta_iconos, "semana.png")),
        ]

        for (texto, comando, color, icono_path) in opciones_principales:
            imagen = Image.open(icono_path)
            imagen = imagen.resize((20, 20), Image.LANCZOS)
            icono = ImageTk.PhotoImage(imagen)
            boton = tk.Button(self.frame_menu, text=texto, command=comando, bg=color, fg="white", font=('Helvetica', 12, 'bold'), anchor="w", image=icono, compound="left", padx=15, pady=10)
            boton.image = icono  # Necesario para que la imagen no sea recolectada por el garbage collector
            boton.pack(side="left", padx=2, pady=2)

        # Menú desplegable para "Reporte Mensual" con íconos y colores personalizados
        icono_reporte_mensual_path = os.path.join(carpeta_iconos, "calendario.png")
        imagen = Image.open(icono_reporte_mensual_path)
        imagen = imagen.resize((20, 20), Image.LANCZOS)
        icono_reporte_mensual = ImageTk.PhotoImage(imagen)
        boton_reporte_mensual = tk.Menubutton(self.frame_menu, text="Reporte Mensual", bg="blue", fg="white", font=('Helvetica', 12, 'bold'), anchor="w", image=icono_reporte_mensual, compound="left", padx=15, pady=10)
        boton_reporte_mensual.image = icono_reporte_mensual
        boton_reporte_mensual.menu = tk.Menu(boton_reporte_mensual, tearoff=0, bg="black", fg="white", font=('Helvetica', 12))

        boton_reporte_mensual["menu"] = boton_reporte_mensual.menu
        boton_reporte_mensual.menu.add_command(label="Reporte mensual", command=self.mostrar_reporte_mensual)
        boton_reporte_mensual.menu.add_command(label="Lista mensual", command=self.mostrar_pordia_mes)
        boton_reporte_mensual.pack(side="left", padx=2, pady=2)

        # Opciones restantes del menú principal con colores personalizados
        opciones_restantes = [
            ("Cargar Datos (Excel)", self.crear_barra_añadir_excel_asistencia, "purple", os.path.join(carpeta_iconos, "excel.png")),
            ("Cerrar Sesión", self.logout, "orange", os.path.join(carpeta_iconos, "salir.png"))
        ]

        for (texto, comando, color, icono_path) in opciones_restantes:
            imagen = Image.open(icono_path)
            imagen = imagen.resize((30, 30), Image.LANCZOS)
            icono = ImageTk.PhotoImage(imagen)
            boton = tk.Button(self.frame_menu, text=texto, command=comando, bg=color, fg="white", font=('Helvetica', 12, 'bold'), anchor="w", image=icono, compound="left", padx=15, pady=10)
            boton.image = icono
            boton.pack(side="left", padx=2, pady=2)

    # Métodos de ejemplo para los comandos de los botones
    def mostrar_reportes_por_dia(self):
        print("Mostrar reportes por día")

    def mostrar_reporte_semanal(self):
        print("Mostrar reporte semanal")

    def mostrar_reporte_mensual(self):
        print("Mostrar reporte mensual")

    def mostrar_pordia_mes(self):
        print("Mostrar por día del mes")

    def crear_barra_añadir_excel_asistencia(self):
        print("Crear barra para añadir asistencia desde Excel")

    def logout(self):
        print("Cerrar sesión")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
