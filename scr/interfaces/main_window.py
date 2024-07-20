import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import tkinter as tk
from tkinter import Tk, Menu, Toplevel,filedialog
from tkinter import messagebox ,ttk,Menu
from scr.modulos import asistencia
from scr.modulos import reportes
from scr.modulos import exportar_pdf
from datetime import datetime
import datetime
from tkcalendar import DateEntry 
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from collections import Counter
import calendar
from PIL import Image, ImageTk
from calendar import monthrange,day_abbr
from scr.modulos.asistencia import obtener_asistencia_LISTA_matris
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import tkinter as tk
from tkinter import messagebox, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime, timedelta
import calendar
from collections import Counter

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Información de asistencia")
        self.master.geometry("900x600")
        self.master.configure(bg="#282c34") 

        # Crear la barra de menú
        #self.crear_menu_lateral()
        self.mostrar_reportes_por_dia()  # Muestra la vista por defecto al iniciar la aplicación
        self.master.protocol("WM_DELETE_WINDOW", self.logout)


    def crear_menu_lateral(self):

        self.frame_menu = tk.Frame(self.master, bg="black", height=50)
        self.frame_menu.pack(side="top", fill="x")

        # Carpeta de iconos
        carpeta_iconos = os.path.join(os.path.dirname(__file__), '..', 'pictures')

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


    def logout(self):
        self.master.destroy()
        from main import LoginWindow
        root = tk.Tk()
        app = LoginWindow(root)
        root.mainloop()

    def mostrar_reportes_por_dia(self):
        self.limpiar_pantalla()
        self.crear_menu_lateral()
        self.entrada()
        self.agregar_barra_reportes()
        self.crear_area_resultado_registro()
        self.mostrar_datos_registro()
        self.agregar_botones_reportes()

    def mostrar_reporte_mensual(self):
        self.limpiar_pantalla()
        self.crear_menu_lateral()
        self.entrada()
        self.agregar_barra_seleccion_mes()
        self.crear_area_resultado_registro_SEMA()
        self.agregar_boton_exportarMEN()
        self.agregar_boton_graficoMEN()
    
    def mostrar_pordia_mes(self):
        self.limpiar_pantalla()
        self.crear_menu_lateral()
        self.entrada()
        self.agregar_barra_seleccion_matris()
        self.crear_area_resultado_registro_MATRI()
        self.agregar_boton_descargar_pdf()
        self.agregar_boton_graficoMEN()
        #self.agregar_boton_exportarMEN

    def mostrar_reporte_semanal(self):
        self.limpiar_pantalla()
        self.crear_menu_lateral()
        self.entrada()
        self.agregar_barra_seleccion_fechas()
        self.crear_area_resultado_registro_SEMA()
        self.agregar_boton_exportar()
        self.agregar_boton_grafico()
       # self.agregar_boton_graficoMEN
    def agregar_boton_exportarMEN(self):
        boton_exportar = tk.Button(self.master, text="Exportar Gráfico a PDF", command=self.exportar_grafico_mensual)
        boton_exportar.pack()

    def exportar_grafico_mensual(self):
        try:
            # Verificar que self.fig esté definido
            if not hasattr(self, 'fig'):
                messagebox.showerror("Error", "No hay gráfico disponible para exportar. Genere el gráfico primero.")
                return

            mes = int(self.mes_entry.get())
            anio = int(self.anio_entry.get())

            # Validar mes y año
            if not mes or not anio:
                messagebox.showerror("Error", "Debe seleccionar el mes y el año.")
                return
            if mes < 1 or mes > 12:
                messagebox.showerror("Error", "El mes debe estar entre 1 y 12.")
                return
            if anio < 1900 or anio > 2100:
                messagebox.showerror("Error", "El año debe estar entre 1900 y 2100.")
                return

            # Guardar el gráfico en un archivo PDF
            archivo_pdf = f"grafico_asistencia_{anio}_{mes:02d}.pdf"
            with PdfPages(archivo_pdf) as pdf:
                pdf.savefig(self.fig)

            messagebox.showinfo("Exportación exitosa", f"El gráfico se ha exportado correctamente a {archivo_pdf}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al exportar el gráfico: {e}")

# Ejemplo de uso:

    def entrada(self):
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'pictures', 'blogger.png')
        if not os.path.exists(logo_path):
            messagebox.showerror("Error", f"No se encontró el logo en {logo_path}")
            return

        self.logo_img = Image.open(logo_path)
        self.logo_img = self.logo_img.resize((100,100), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo_img)

        # Etiqueta con el logo
        tk.Label(self.master, image=self.logo, bg="#282c34").pack(side=tk.TOP, padx=5)

        # Título al lado del logo
        #tk.Label(self.master, text="VENTANA ADMINISTRADOR ", font=("Arial", 20, "bold"), bg="#282c34", fg="#61dafb").pack(side=tk.TOP, padx=5)


        
    def agregar_boton_exportarMEN(self):
        exportar_frame = tk.Frame(self.master)
        exportar_frame.pack(pady=10)
        boton_exportar = tk.Button(exportar_frame, text="Exportar", command=self.exportar_a_pdf_MESUAL, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=15, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  )
        boton_exportar.pack(side=tk.LEFT, padx=5)

    def agregar_boton_exportar(self):
        exportar_frame = tk.Frame(self.master)
        exportar_frame.pack(pady=10)
        boton_exportar = tk.Button(exportar_frame, text="Exportar", command=self.exportar_a_pdf, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=15, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  )
        boton_exportar.pack(side=tk.LEFT, padx=5)

    def exportar_a_pdf(self):
        fecha_inicio = self.fecha_inicio_entry.get_date()
        fecha_fin = self.fecha_fin_entry.get_date()

        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha final debe ser mayor o igual a la fecha de inicio.")
            return
        
        # Llamar a la función de exportación con el rango de fechas
        exportar_pdf.exportar_datos_rango_pdf(fecha_inicio, fecha_fin)
        messagebox.showinfo("Éxito", "Datos exportados a PDF exitosamente.")
    
    def exportar_a_pdf_MESUAL(self):

        mes = int(self.mes_entry.get())
        anio = int(self.anio_entry.get())

        # Validar que el mes sea válido (de 1 a 12)
        if mes < 1 or mes > 12:
            messagebox.showerror("Error", "Ingrese un número de mes válido (1-12).")
            return

        # Obtener el último día del mes
        ultimo_dia_mes = calendar.monthrange(anio, mes)[1]

        # Construir las fechas de inicio y fin del mes
        fecha_inicio = f"{anio}-{mes:02d}-01"
        fecha_fin = f"{anio}-{mes:02d}-{ultimo_dia_mes:02d}"

        try:
            # Llamar a la función de exportación con el mes seleccionado
            exportar_pdf.exportar_datos_mes_pdf(fecha_inicio, fecha_fin, mes, anio)
            messagebox.showinfo("Éxito", f"Datos del mes {mes}/{anio} exportados a PDF exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar a PDF: {e}")

    def limpiar_pantalla(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()
        if hasattr(self, 'action_frame_rango'):
            self.action_frame_rango.destroy()

    def agregar_barra_reportes(self):
        search_frame = tk.Frame(self.master)
        search_frame.pack(pady=10)
        search_frame.configure(bg="#282c34")

        #boton_reportes = tk.Button(search_frame, text="Reporte de hoy", command=self.mostrar_reportes_hoy)
        #boton_reportes.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Reporte de hoy", command=self.mostrar_reportes_hoy, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=15, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  ).pack(side=tk.LEFT, padx=5)

        tk.Label(search_frame, text="Fecha inicio:",font=("Arial", 14, "bold"), bg="#282c34", fg="#61dafb").pack(side=tk.LEFT, padx=5)
        self.fecha_inicio_entry = DateEntry(search_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.fecha_inicio_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(search_frame, text="Fecha fin:",font=("Arial", 14, "bold"), bg="#282c34", fg="#61dafb").pack(side=tk.LEFT, padx=5)
        self.fecha_fin_entry = DateEntry(search_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.fecha_fin_entry.pack(side=tk.LEFT, padx=5)

        #search_button = tk.Button(search_frame, text="Buscar asistencia", command=self.buscar_asistencia)
        #search_button.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Buscar asisteb¿ncia", command=self.buscar_asistencia, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=15, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  ).pack(side=tk.LEFT, padx=5)

    def agregar_botones_reportes(self):
        search_frame = tk.Frame(self.master)
        search_frame.pack(pady=10)
        search_frame.configure(bg="#282c34")

        #boton_inicio = tk.Button(search_frame, text="Actualizar", command=self.mostrar_reportes_por_dia)
        #boton_inicio.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Actualizar", command=self.mostrar_reportes_por_dia, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=15, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  ).pack(side=tk.LEFT, padx=5)

        # Guardar el botón de exportar en una variable de instancia
        self.boton_fin = tk.Button(search_frame, text="Exportar", command=self.exportar_datos_hoy, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=15, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  )
        self.boton_fin.pack(side=tk.LEFT, padx=5)
        

    def crear_area_resultado_registro(self):
        self.resultados_frame = tk.Frame(self.master)
        self.resultados_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.resultados_frame, columns=('ID', 'Nombres', 'Apellido Pat', 'Apellido Mat', 'DNI', 'Hora Entrada','fecha'), show='headings', height=16)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombres', text='Nombres')
        self.tree.heading('Apellido Pat', text='Apell. Paterno')
        self.tree.heading('Apellido Mat', text='Apell. Materno')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('Hora Entrada', text='Hora Entrada')
        self.tree.heading('fecha',text='fecha')

        #self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.column('ID', width=5, anchor=tk.CENTER)
        self.tree.column('Nombres', width=150)
        self.tree.column('Apellido Pat', width=160)
        self.tree.column('Apellido Mat', width=160)
        self.tree.column('DNI', width=110, anchor=tk.CENTER)
        self.tree.column('Hora Entrada', width=100, anchor=tk.CENTER)
        self.tree.column('fecha',width=100, anchor=tk.CENTER)

        # Estilo de la tabla
        style = ttk.Style()
        style.configure('Treeview', background='#FFFFFF')
        style.configure('Treeview.Heading', background='#CCCCCC')

        # Agregar barras de desplazamiento
        scroll_y = ttk.Scrollbar(self.resultados_frame, orient='vertical', command=self.tree.yview)
        scroll_y.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scroll_y.set)

        self.tree.pack(fill=tk.BOTH, expand=True)        
    def mostrar_datos_registro(self):
        resultados = asistencia.obtener_asistencia()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for resultado in resultados:
            self.tree.insert('', tk.END, values=resultado)

    def mostrar_reportes_hoy(self):
        resultados = reportes.obtener_asistencia_hoy()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for resultado in resultados:
            self.tree.insert('', tk.END, values=resultado)

        if not resultados:
            messagebox.showinfo("Info", "No hay registros de asistencia para hoy.")

    def exportar_datos_hoy(self):
        import datetime
        fecha = datetime.date.today().strftime('%Y-%m-%d')
        exportar_pdf.exportar_datos_pdf(fecha)
        messagebox.showinfo("Éxito", "Datos exportados a PDF exitosamente.")

    def mostrar_datos_rango(self, resultado):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for result in resultado:
            self.tree.insert('', tk.END, values=result)

    def buscar_asistencia(self):
        fecha_inicio = self.fecha_inicio_entry.get_date()
        fecha_fin = self.fecha_fin_entry.get_date()

        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha final debe ser mayor o igual a la fecha de inicio.")
            return

        self.mostrar_datos_rango([])

        resultado = reportes.obtener_asistencias_en_rango(fecha_inicio, fecha_fin)
        self.mostrar_datos_rango(resultado)

        # Ocultar el botón de exportar datos de hoy si está visible
        if hasattr(self, 'boton_fin'):
            self.boton_fin.pack_forget() 
              # Ocultar el botón de exportar datos de hoy

        # Agregar los botones para el rango de fechas si no existen
        self.agregar_botones_accion_rango()

    def agregar_botones_accion_rango(self):
        # Si el frame de botones de acción para el rango ya existe, lo eliminamos
        if hasattr(self, 'action_frame_rango'):
            self.action_frame_rango.destroy()
        
        # Crear un nuevo frame para los botones de acción
        self.action_frame_rango = tk.Frame(self.master)
        self.action_frame_rango.pack(pady=10)

        #boton_actualizar = tk.Button(self.action_frame_rango, text="Actualizar", command=self.buscar_asistencia)
        #boton_actualizar.pack(side=tk.LEFT, padx=5)

        boton_exportar_rango = tk.Button(self.action_frame_rango, text="Exportar Rango a PDF", command=self.exportar_datos_rango, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=15, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  )
        boton_exportar_rango.pack(side=tk.LEFT, padx=5)

    def exportar_datos_rango(self):
        fecha_inicio = self.fecha_inicio_entry.get_date()
        fecha_fin = self.fecha_fin_entry.get_date()

        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha final debe ser mayor o igual a la fecha de inicio.")
            return
        
        # Llamar a la función de exportación con el rango de fechas
        exportar_pdf.exportar_datos_rango_pdf(fecha_inicio, fecha_fin)
        messagebox.showinfo("Éxito", "Datos exportados a PDF exitosamente.")


    def agregar_barra_seleccion_fechas(self):
        fechas_frame = tk.Frame(self.master)
        fechas_frame.pack(pady=10)
        fechas_frame.configure(bg="#282c34")
        

        tk.Label(fechas_frame, text="Fecha inicio:",font=("Arial", 14, "bold"), bg="#282c34", fg="#61dafb").pack(side=tk.LEFT, padx=5)
        self.fecha_inicio_entry = DateEntry(fechas_frame, date_pattern='yyyy-mm-dd')
        self.fecha_inicio_entry.pack(side=tk.LEFT, padx=5)
        self.fecha_inicio_entry.bind("<<DateEntrySelected>>", self.actualizar_fecha_inicio_y_fin)

        tk.Label(fechas_frame, text="Fecha fin:",font=("Arial", 14, "bold"), bg="#282c34", fg="#61dafb").pack(side=tk.LEFT, padx=5)
        self.fecha_fin_entry = DateEntry(fechas_frame, date_pattern='yyyy-mm-dd')
        self.fecha_fin_entry.pack(side=tk.LEFT, padx=5)
        self.fecha_fin_entry.config(state='readonly')

        boton_generar_reporte = tk.Button(fechas_frame, text="Generar reporte", command=self.mostrar_datos_semanales, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=15, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  )
        boton_generar_reporte.pack(side=tk.LEFT, padx=5)
    

    def agregar_barra_seleccion_mes(self):
        mes_frame = tk.Frame(self.master)
        mes_frame.pack(pady=10)
        mes_frame.configure(bg="#282c34")

        #tk.Label(mes_frame, text="Seleccione el mes y el año:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(mes_frame, text="Seleccione el mes y el año:",font=("Arial", 14, "bold"), bg="#282c34", fg="#61dafb").pack(side=tk.LEFT, padx=5)
        
        
        
        self.mes_entry = ttk.Combobox(mes_frame, values=list(range(1, 13)), state="readonly")
        self.mes_entry.pack(side=tk.LEFT, padx=5)
        self.mes_entry.current(datetime.now().month - 1)
        
        self.anio_entry = ttk.Combobox(mes_frame, values=list(range(2000, datetime.now().year + 1)), state="readonly")
        self.anio_entry.pack(side=tk.LEFT, padx=5)
        self.anio_entry.current(datetime.now().year - 2000)

        boton_generar_reporte = tk.Button(mes_frame, text="Generar reporte", command=self.mostrar_datos_mensuales, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=15, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  )
        boton_generar_reporte.pack(side=tk.LEFT, padx=5)
    
    

    def actualizar_fecha_inicio_y_fin(self, event):
        fecha_inicio_str = self.fecha_inicio_entry.get()
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')

        # Ajustar la fecha de inicio al primer día de la semana (lunes)
        while fecha_inicio.weekday() != 0:  # 0 es lunes
            fecha_inicio -= timedelta(days=1)

        fecha_fin = fecha_inicio + timedelta(days=6)

        self.fecha_inicio_entry.set_date(fecha_inicio)
        self.fecha_fin_entry.set_date(fecha_fin)



    def mostrar_datos_semanales(self):
        fecha_inicio = self.fecha_inicio_entry.get()
        fecha_fin = self.fecha_fin_entry.get()
        if not fecha_inicio or not fecha_fin:
            messagebox.showerror("Error", "Debe ingresar ambas fechas.")
            return
        resultados = asistencia.obtener_asistencia_por_fecha(fecha_inicio, fecha_fin)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for resultado in resultados:
            self.tree.insert('', tk.END, values=resultado)

     
    def mostrar_datos_mensuales(self):
        try:
            mes = int(self.mes_entry.get())
            anio = int(self.anio_entry.get())
            
            if not mes or not anio:
                messagebox.showerror("Error", "Debe seleccionar el mes y el año.")
                return
            
            # Validar mes y año
            if mes < 1 or mes > 12:
                messagebox.showerror("Error", "El mes debe estar entre 1 y 12.")
                return
            if anio < 1900 or anio > 2100:
                messagebox.showerror("Error", "El año debe estar entre 1900 y 2100.")
                return
            
            # Formatear correctamente la fecha
            fecha_inicio = f"{anio}-{mes:02d}-01"
            fecha_fin = f"{anio}-{mes:02d}-{calendar.monthrange(anio, mes)[1]:02d}"
            
            print(fecha_inicio)
            print(fecha_fin)
            
            resultados = asistencia.obtener_asistencia_por_fecha(fecha_inicio, fecha_fin)
            
            for row in self.tree.get_children():
                self.tree.delete(row)
            for resultado in resultados:
                self.tree.insert('', tk.END, values=resultado)
        except ValueError:
            messagebox.showerror("Error", "Mes y año deben ser números enteros.")



    def crear_area_resultado_registro_SEMA(self):
        self.resultados_frame = tk.Frame(self.master)
        self.resultados_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.resultados_frame, columns=('ID', 'Nombres', 'Apellido Pat', 'Apellido Mat', 'DNI', 'Hora Entrada','Fecha'), show='headings', height=15)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombres', text='Nombres')
        self.tree.heading('Apellido Pat', text='Apell. Paterno')
        self.tree.heading('Apellido Mat', text='Apell. Materno')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('Hora Entrada', text='Hora Entrada')
        self.tree.heading('Fecha',text='Fecha')

        #self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.column('ID', width=5, anchor=tk.CENTER)
        self.tree.column('Nombres', width=150)
        self.tree.column('Apellido Pat', width=160)
        self.tree.column('Apellido Mat', width=160)
        self.tree.column('DNI', width=110, anchor=tk.CENTER)
        self.tree.column('Hora Entrada', width=100, anchor=tk.CENTER)
        self.tree.column('Fecha',width=180, anchor=tk.CENTER)

        style = ttk.Style()
        style.configure('Treeview', background='#FFFFFF')
        style.configure('Treeview.Heading', background='#CCCCCC')

        # Agregar barras de desplazamiento
        scroll_y = ttk.Scrollbar(self.resultados_frame, orient='vertical', command=self.tree.yview)
        scroll_y.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scroll_y.set)

        self.tree.pack(fill=tk.BOTH, expand=True)


    def agregar_boton_grafico(self):
            grafico_frame = tk.Frame(self.master)
            grafico_frame.pack(pady=10)
            boton_grafico = tk.Button(grafico_frame, text="Ver gráfico", command=self.mostrar_grafico_semanal, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=15, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  )
            boton_grafico.pack(side=tk.LEFT, padx=5)
            
    def agregar_boton_graficoMEN(self):
            grafico_frame = tk.Frame(self.master)
            grafico_frame.pack(pady=10)
            boton_grafico = tk.Button(grafico_frame, text="Ver gráfico", command=self.mostrar_grafico_mensual, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=15, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  )
            boton_grafico.pack(side=tk.LEFT, padx=5)
            boton_exporta = tk.Button(grafico_frame, text="exportar gráfico", command=self.exportar_grafico_mensual, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=15, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  )
            boton_exporta.pack(side=tk.LEFT, padx=5)

    def mostrar_grafico_semanal(self):
        from collections import Counter
        
        fecha_inicio = self.fecha_inicio_entry.get()
        fecha_fin = self.fecha_fin_entry.get()
        resultados = asistencia.obtener_grafico_por_fecha(fecha_inicio, fecha_fin)
        
        if not resultados:
            messagebox.showerror("Error", "No hay datos para mostrar en el gráfico.")
            return
        
        # Crear una lista de todas las fechas en el rango seleccionado
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        todas_fechas = [(fecha_inicio_dt + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((fecha_fin_dt - fecha_inicio_dt).days + 1)]

        # Contar la asistencia por día
        fechas = [resultado[2] for resultado in resultados]
        conteo_fechas = Counter(fechas)
        
        conteos = [conteo_fechas.get(fecha, 0) for fecha in todas_fechas]
        
        fig, ax = plt.subplots()
        ax.bar(todas_fechas, conteos, color='blue')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Número de asistentes')
        ax.set_title('Asistencia Semanal')
        ax.grid(True)
        ax.set_xticks(todas_fechas)  # Asegurar que todas las fechas estén en el eje x
        ax.set_xticklabels(todas_fechas, rotation=45, ha='right')  # Rotar etiquetas para mejor visualización

        # Crear una nueva ventana para el gráfico
        ventana_grafico = Toplevel(self.master)
        ventana_grafico.title("Gráfico de Asistencia Semanal")
        ventana_grafico.geometry("800x600")

        # Insertar el gráfico en la nueva ventana
        canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def mostrar_grafico_mensual(self):
        try:
            from collections import Counter
            
            mes = int(self.mes_entry.get())
            anio = int(self.anio_entry.get())
            
            if not mes or not anio:
                messagebox.showerror("Error", "Debe seleccionar el mes y el año.")
                return
            
            # Validar mes y año
            if mes < 1 or mes > 12:
                messagebox.showerror("Error", "El mes debe estar entre 1 y 12.")
                return
            if anio < 1900 or anio > 2100:
                messagebox.showerror("Error", "El año debe estar entre 1900 y 2100.")
                return

            # Formatear correctamente la fecha
            fecha_inicio = f"{anio}-{mes:02d}-01"
            fecha_fin = f"{anio}-{mes:02d}-{calendar.monthrange(anio, mes)[1]:02d}"
       
            

            resultados = asistencia.obtener_asistencia_por_fecha(fecha_inicio, fecha_fin)
            resultados = asistencia.obtener_grafico_por_fecha(fecha_inicio, fecha_fin)

            
            if not resultados:
                messagebox.showerror("Error", "No hay datos para mostrar en el gráfico.")
                return
            
            
            
            # Crear una lista de todas las fechas en el rango seleccionado
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            todas_fechas = [(fecha_inicio_dt + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((fecha_fin_dt - fecha_inicio_dt).days + 1)]
            
            # Contar la asistencia por día
            fechas = [resultado[2] for resultado in resultados]
            conteo_fechas = Counter(fechas)
            
           
            
            conteos = [conteo_fechas.get(fecha, 0) for fecha in todas_fechas]
            
      
            
            fig, ax = plt.subplots()
            ax.bar(todas_fechas, conteos, color='blue')
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Número de asistentes')
            ax.set_title('Asistencia Mensual')
            ax.grid(True)
            ax.set_xticks(todas_fechas)  # Asegurar que todas las fechas estén en el eje x
            ax.set_xticklabels(todas_fechas, rotation=45, ha='right')  # Rotar etiquetas para mejor visualización

            # Crear una nueva ventana para el gráfico
            ventana_grafico = Toplevel(self.master)
            ventana_grafico.title("Gráfico de Asistencia Mensual")
            ventana_grafico.geometry("800x600")

            # Insertar el gráfico en la nueva ventana
            canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Guardar el gráfico en una variable de instancia para exportarlo después
            self.fig = fig

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error: {e}")




    # TRATANDO DE AGREGAR PROR EXCEL 
    
    def crear_barra_añadir_excel_asistencia(self):
        def open_file():
            filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
            if not filepath:
                return
            
            try:
                df = pd.read_excel(filepath)
                
                # Convertir columnas numéricas a tipo 'object' antes de reemplazar NaN
                for col in df.select_dtypes(include=[float, int]).columns:
                    df[col] = df[col].astype('object')
                    
                df.fillna('', inplace=True)  # Reemplazar NaN con una cadena vacía

                self.text_widget.delete('1.0', tk.END)
                self.text_widget.insert(tk.END, df.to_string(index=False))

                self.file_label.config(text=f"Archivo seleccionado: {filepath}")

                self.data = df
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo\n{e}")

        def agregar_a_SQlite():
            if self.data is None:
                messagebox.showwarning("Advertencia", "No hay datos para agregar a la base de datos")
                return
            asistencia.agregar_asistencia_desde_excel(self.data)
            reset()
        
        def reset():
            # Borrar el contenido del Text widget
            self.text_widget.delete('1.0', tk.END)
            # Restablecer el Label del archivo seleccionado
            self.file_label.config(text="Archivo seleccionado: Ninguno")
            # Restablecer la variable de datos
            self.data = None

        ventana_archivo = tk.Toplevel(self.master)
        ventana_archivo.title("Importar Asistencia desde Excel")
        ventana_archivo.geometry("700x500")

        search_frame = tk.Frame(ventana_archivo)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Seleccionar Archivo").pack(side=tk.LEFT, padx=5)
        self.file_label = tk.Label(ventana_archivo, text="Archivo seleccionado: Ninguno")
        self.file_label.pack(pady=10)

        search_button = ttk.Button(search_frame, text="Buscar", command=open_file)
        search_button.pack(side=tk.LEFT, padx=5)

        self.text_widget = tk.Text(ventana_archivo, wrap='none', width=70, height=30)
        self.text_widget.pack(expand=True, fill='both')

        boton_agregar_pres = ttk.Button(search_frame, text="Agregar a SQlite", command=agregar_a_SQlite)
        boton_agregar_pres.pack(side=tk.LEFT, padx=5)

        self.data = None



# todo el genera una matriz(lista)
    def agregar_barra_seleccion_matris(self):
        mes_frame = tk.Frame(self.master)
        mes_frame.pack(pady=10)
        mes_frame.configure(bg="#282c34")

        tk.Label(mes_frame, text="Seleccione el mes y el año:", font=("Arial", 14, "bold"), bg="#282c34", fg="#61dafb").pack(side=tk.LEFT, padx=5)

        self.mes_entry = ttk.Combobox(mes_frame, values=list(range(1, 13)), state="readonly")
        self.mes_entry.pack(side=tk.LEFT, padx=5)
        self.mes_entry.current(datetime.now().month - 1)

        self.anio_entry = ttk.Combobox(mes_frame, values=list(range(2000, datetime.now().year + 1)), state="readonly")
        self.anio_entry.pack(side=tk.LEFT, padx=5)
        self.anio_entry.current(datetime.now().year - 2000)

        boton_generar_reporte = tk.Button(mes_frame, text="Generar reporte", command=self.mostrar_datos_mensualesMA, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                                          padx=15, pady=10,  borderwidth=0,  highlightthickness=0,  activebackground="#e53935",  activeforeground="#ffffff")
        boton_generar_reporte.pack(side=tk.LEFT, padx=5)


    def crear_area_resultado_registro_MATRI(self):
        self.resultados_frame = tk.Frame(self.master)
        self.resultados_frame.pack(pady=10)
        
        dias = [f'{i+1}' for i in range(31)]
        columnas = ['ID', 'Nombres', 'Apellido Pat', 'Apellido Mat', 'DNI'] + dias
        
        self.tree = ttk.Treeview(self.resultados_frame, columns=columnas, show='headings', height=15)

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=20, anchor=tk.CENTER)
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('Nombres', width=120)
        self.tree.column('Apellido Pat', width=130)
        self.tree.column('Apellido Mat', width=130)
        self.tree.column('DNI', width=100, anchor=tk.CENTER)

        style = ttk.Style()
        style.configure('Treeview', background='#FFFFFF')
        style.configure('Treeview.Heading', background='#CCCCCC')

        # Crear barra de desplazamiento vertical
        scroll_y = ttk.Scrollbar(self.resultados_frame, orient='vertical', command=self.tree.yview)
        scroll_y.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scroll_y.set)

        # Crear barra de desplazamiento horizontal
        scroll_x = ttk.Scrollbar(self.resultados_frame, orient='horizontal', command=self.tree.xview)
        scroll_x.pack(side='bottom', fill='x')
        self.tree.configure(xscrollcommand=scroll_x.set)

        self.tree.pack(fill=tk.BOTH, expand=True)

        
    def mostrar_datos_mensualesMA(self):
        mes = int(self.mes_entry.get())
        anio = int(self.anio_entry.get())
        self.mes = mes
        self.anio = anio

        fecha_inicio = datetime(anio, mes, 1).strftime('%Y-%m-%d')
        _, num_days = monthrange(anio, mes)
        fecha_fin = datetime(anio, mes, num_days).strftime('%Y-%m-%d')

        asistencias = obtener_asistencia_LISTA_matris(fecha_inicio, fecha_fin)

        # Limpiar datos anteriores
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insertar nuevos datos
        for asistencia in asistencias:
            persona_info = asistencia[:5]
            fechas_asistencia = asistencia[5]
            valores = list(persona_info) + ['✓' if dia in [datetime.strptime(fecha, '%Y-%m-%d').day for fecha in fechas_asistencia] else '-' for dia in range(1, num_days + 1)]
            self.tree.insert('', 'end', values=valores)
            
    def agregar_boton_descargar_pdf(self):
        boton_frame = tk.Frame(self.master)
        boton_frame.pack(pady=10)

        boton_descargar_pdf = tk.Button(boton_frame, text="Descargar en PDF", command=self.descargar_pdf, bg="#4caf50", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                                        padx=15, pady=10, borderwidth=0, highlightthickness=0, activebackground="#43a047", activeforeground="#ffffff")
        boton_descargar_pdf.pack(side=tk.LEFT, padx=5)

    def descargar_pdf(self):
        self.exportar_datos_matris_pdf(self.mes, self.anio)

    def exportar_datos_matris_pdf(self, mes, anio):
        # Crear el archivo PDF
        archivo = filedialog.asksaveasfilename(defaultextension=".pdf",
                                            filetypes=[("PDF Files", "*.pdf")],
                                            title="Guardar archivo como",
                                            initialfile=f"reporte_asistencia_{mes}_{anio}.pdf")
        if not archivo:
            return

        doc = SimpleDocTemplate(archivo, pagesize=landscape(letter))
        contenido = []

        styles = getSampleStyleSheet()
        titulo_style = ParagraphStyle(name='CustomTitle', fontSize=16, alignment=1, spaceAfter=12, parent=styles['Title'])
        contenido.append(Paragraph(f"Reporte de Asistencia del {calendar.month_name[mes]} de {anio}", style=titulo_style))

        # Preparar los datos para la tabla
        datos_tabla = [['Apellido Pat', 'DNI'] + [f'{dia}' for dia in range(1, 31)]]

        # Obtener los datos de la Treeview
        for child in self.tree.get_children():
            item = self.tree.item(child)["values"]
            apellido_pat = item[2]  # Índice 2 para Apellido Pat
            dni = item[4]  # Índice 4 para DNI
            asistencia = item[5:5+30]  # Índices 5 a 34 para la asistencia
            datos_tabla.append([apellido_pat, dni] + asistencia)

        # Crear la tabla
        tabla = Table(datos_tabla)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#D0E0F0")),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        contenido.append(tabla)
        doc.build(contenido)
        messagebox.showinfo("Éxito", f"Datos exportados a {archivo}.")