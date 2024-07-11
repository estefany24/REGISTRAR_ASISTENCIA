import tkinter as tk
from tkinter import Tk, Menu
from tkcalendar import DateEntry  # Importación correcta de DateEntry
from tkinter import messagebox ,ttk,Menu
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from scr.modulos import asistencia
<<<<<<< HEAD
from scr.modulos import reportes
from scr.modulos import exportar_pdf
from datetime import datetime
import datetime
from tkcalendar import DateEntry 
from datetime import datetime, timedelta

=======
from datetime import datetime, timedelta
>>>>>>> 6ae52fe3f7c817e5fa033c0f542da4470b174d6a

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Información de asistencia")
        self.master.geometry("900x600")

        # Crear la barra de menú
        self.crear_menu()

    def crear_menu(self):
        menubar = Menu(self.master)
      
        # Menú Reportes
        libros_menu = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="white", activeforeground="black", font=('Helvetica', 9))
        libros_menu.add_command(label="Ver todo", command=self.mostrar_reportes_por_dia)
        menubar.add_cascade(label="Reportes", menu=libros_menu)

        # Menú Reporte Semanal
        categorias_menu = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="white", activeforeground="black", font=('Helvetica', 9))
<<<<<<< HEAD
        categorias_menu.add_command(label="Reporte semanal",command=self.mostrar_reporte_semanal)
        menubar.add_cascade(label="Reporte Semanal", menu=categorias_menu)
=======
        categorias_menu.add_command(label="Reporte semanal", command=self.mostrar_reporte_semanal)
        menubar.add_cascade(label="Reporte semanal", menu=categorias_menu)
>>>>>>> 6ae52fe3f7c817e5fa033c0f542da4470b174d6a

        # Menú Reporte Semanal
        autores_menu = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="white", activeforeground="black", font=('Helvetica', 9))
        autores_menu.add_command(label="Reporte mensual")
        menubar.add_cascade(label="Reporte Semanal", menu=autores_menu)

        # Menú Cargar Datos
        cerrar_sesion_menu = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="white", activeforeground="black", font=('Helvetica', 9))
        cerrar_sesion_menu.add_command(label="Cargar datos")
        menubar.add_cascade(label="Cargar Datos", menu=cerrar_sesion_menu)

        # Menú Salir
        cerrar_sesion_menu = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="white", activeforeground="black", font=('Helvetica', 9))
        cerrar_sesion_menu.add_command(label="Cerrar sesión", command=self.logout)
        menubar.add_cascade(label="Salir", menu=cerrar_sesion_menu)

        self.master.config(menu=menubar)
        self.mostrar_reportes_por_dia()

    def logout(self):
        self.master.destroy()
        from main import LoginWindow
        root = tk.Tk()
        app = LoginWindow(root)
        root.mainloop()

    def mostrar_reportes_por_dia(self):
        self.limpiar_pantalla()
        self.agregar_barra_reportes()
        self.crear_area_resultado_registro()
        self.mostrar_datos_registro()
<<<<<<< HEAD
        self.agregar_botones_reportes()

=======
        
>>>>>>> 6ae52fe3f7c817e5fa033c0f542da4470b174d6a
    def mostrar_reporte_semanal(self):
        self.limpiar_pantalla()
        self.agregar_barra_seleccion_fechas()
        self.crear_area_resultado_registro_SEMA()
        self.agregar_boton_exportar()
<<<<<<< HEAD

    def agregar_boton_exportar(self):
        exportar_frame = tk.Frame(self.master)
        exportar_frame.pack(pady=10)
        boton_exportar = tk.Button(exportar_frame, text="Exportar", command=self.exportar_a_pdf)
        boton_exportar.pack()

    def exportar_a_pdf(self):
        fecha_inicio = self.fecha_inicio_entry.get_date()
        fecha_fin = self.fecha_fin_entry.get_date()

        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha final debe ser mayor o igual a la fecha de inicio.")
            return
        
        # Llamar a la función de exportación con el rango de fechas
        exportar_pdf.exportar_datos_rango_pdf(fecha_inicio, fecha_fin)
        messagebox.showinfo("Éxito", "Datos exportados a PDF exitosamente.")
=======
>>>>>>> 6ae52fe3f7c817e5fa033c0f542da4470b174d6a

    def limpiar_pantalla(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()
        if hasattr(self, 'action_frame_rango'):
            self.action_frame_rango.destroy()

    def agregar_barra_reportes(self):
        search_frame = tk.Frame(self.master)
        search_frame.pack(pady=10)

        boton_reportes = tk.Button(search_frame, text="Reporte de hoy", command=self.mostrar_reportes_hoy)
        boton_reportes.pack(side=tk.LEFT, padx=5)

        tk.Label(search_frame, text="Fecha inicio:").pack(side=tk.LEFT, padx=5)
        self.fecha_inicio_entry = DateEntry(search_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.fecha_inicio_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(search_frame, text="Fecha fin:").pack(side=tk.LEFT, padx=5)
        self.fecha_fin_entry = DateEntry(search_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.fecha_fin_entry.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(search_frame, text="Buscar asistencia", command=self.buscar_asistencia)
        search_button.pack(side=tk.LEFT, padx=5)

    def agregar_botones_reportes(self):
        search_frame = tk.Frame(self.master)
        search_frame.pack(pady=10)

<<<<<<< HEAD
        boton_inicio = tk.Button(search_frame, text="Actualizar", command=self.mostrar_reportes_por_dia)
        boton_inicio.pack(side=tk.LEFT, padx=5)

        # Guardar el botón de exportar en una variable de instancia
        self.boton_fin = tk.Button(search_frame, text="Exportar", command=self.exportar_datos_hoy)
        self.boton_fin.pack(side=tk.LEFT, padx=5)

=======
#OJO ESTA FUNCION SEMANAL NO ESTA UTILIZANDO  en semanla 
>>>>>>> 6ae52fe3f7c817e5fa033c0f542da4470b174d6a
    def crear_area_resultado_registro(self):
        self.resultados_frame = tk.Frame(self.master)
        self.resultados_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.resultados_frame, columns=('ID', 'Nombres', 'Apellido Pat', 'Apellido Mat', 'DNI', 'Hora Entrada'), show='headings', height=20)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombres', text='Nombres')
        self.tree.heading('Apellido Pat', text='Apell. Paterno')
        self.tree.heading('Apellido Mat', text='Apell. Materno')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('Hora Entrada', text='Hora Entrada')

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.column('ID', width=5, anchor=tk.CENTER)
        self.tree.column('Nombres', width=100, anchor=tk.CENTER)
        self.tree.column('Apellido Pat', width=100, anchor=tk.CENTER)
        self.tree.column('Apellido Mat', width=100, anchor=tk.CENTER)
        self.tree.column('DNI', width=100, anchor=tk.CENTER)
        self.tree.column('Hora Entrada', width=100, anchor=tk.CENTER)


    def mostrar_datos_registro(self):
        resultados = asistencia.obtener_asistencia()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for resultado in resultados:
            self.tree.insert('', tk.END, values=resultado)

<<<<<<< HEAD
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

        boton_exportar_rango = tk.Button(self.action_frame_rango, text="Exportar Rango a PDF", command=self.exportar_datos_rango)
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


=======
    
    #BARRA AGREGAR .. SEMANAL 
>>>>>>> 6ae52fe3f7c817e5fa033c0f542da4470b174d6a
    def agregar_barra_seleccion_fechas(self):
        fechas_frame = tk.Frame(self.master)
        fechas_frame.pack(pady=10)

        tk.Label(fechas_frame, text="Fecha inicio:").pack(side=tk.LEFT, padx=5)
        self.fecha_inicio_entry = DateEntry(fechas_frame, date_pattern='yyyy-mm-dd')
        self.fecha_inicio_entry.pack(side=tk.LEFT, padx=5)
        self.fecha_inicio_entry.bind("<<DateEntrySelected>>", self.actualizar_fecha_inicio_y_fin)

        tk.Label(fechas_frame, text="Fecha fin:").pack(side=tk.LEFT, padx=5)
        self.fecha_fin_entry = DateEntry(fechas_frame, date_pattern='yyyy-mm-dd')
        self.fecha_fin_entry.pack(side=tk.LEFT, padx=5)
        self.fecha_fin_entry.config(state='readonly')

        boton_generar_reporte = tk.Button(fechas_frame, text="Generar reporte", command=self.mostrar_datos_semanales)
        boton_generar_reporte.pack(side=tk.LEFT, padx=5)


    def actualizar_fecha_inicio_y_fin(self, event):
        fecha_inicio_str = self.fecha_inicio_entry.get()
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
<<<<<<< HEAD

        # Ajustar la fecha de inicio al primer día de la semana (lunes)
        while fecha_inicio.weekday() != 0:  # 0 es lunes
            fecha_inicio -= timedelta(days=1)

        fecha_fin = fecha_inicio + timedelta(days=6)

        self.fecha_inicio_entry.set_date(fecha_inicio)
        self.fecha_fin_entry.set_date(fecha_fin)



=======
        
        # Ajustar la fecha de inicio al primer día de la semana (lunes)
        while fecha_inicio.weekday() != 0:  # 0 es lunes
            fecha_inicio -= timedelta(days=1)
        
        fecha_fin = fecha_inicio + timedelta(days=6)
        
        self.fecha_inicio_entry.set_date(fecha_inicio)
        self.fecha_fin_entry.set_date(fecha_fin)

>>>>>>> 6ae52fe3f7c817e5fa033c0f542da4470b174d6a
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


    def crear_area_resultado_registro_SEMA(self):
        self.resultados_frame = tk.Frame(self.master)
        self.resultados_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.resultados_frame, columns=('ID', 'Nombres', 'Fecha', 'Hora de entrada'), show='headings', height=20)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombres', text='Nombres')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Hora de entrada', text='Hora de entrada')

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.column('ID', width=5, anchor=tk.CENTER)
        self.tree.column('Nombres', width=180, anchor=tk.CENTER)
        self.tree.column('Fecha', width=180, anchor=tk.CENTER)
        self.tree.column('Hora de entrada', width=180, anchor=tk.CENTER)
<<<<<<< HEAD
=======


    # funcion para exportar en pdf los datos por semana 
    def agregar_boton_exportar(self):
        exportar_frame = tk.Frame(self.master)
        exportar_frame.pack(pady=10)
        boton_exportar = tk.Button(exportar_frame, text="Exportar", command=self.exportar_a_pdf)
        boton_exportar.pack()

    def exportar_a_pdf(self):
        fecha_inicio = self.fecha_inicio_entry.get()
        fecha_fin = self.fecha_fin_entry.get()
        resultados = asistencia.obtener_asistencia_por_fecha(fecha_inicio, fecha_fin)
        
        if not resultados:
            messagebox.showerror("Error", "No hay datos para exportar en las fechas seleccionadas.")
            return

        pdf_filename = f"Asistencia_{fecha_inicio}_a_{fecha_fin}.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter
        y = height - 40
        
        c.setFont("Helvetica", 14)
        c.drawString(30, y, f"Reporte de Asistencia del {fecha_inicio} al {fecha_fin}")
        y -= 20
        
        c.setFont("Helvetica", 12)
        c.drawString(30, y, "ID")
        c.drawString(100, y, "Nombres")
        c.drawString(300, y, "Fecha")
        c.drawString(400, y, "Hora de entrada")
        y -= 20
        
        for resultado in resultados:
            c.drawString(30, y, str(resultado[0]))
            c.drawString(100, y, resultado[1])
            c.drawString(300, y, resultado[2])
            c.drawString(400, y, resultado[3])
            y -= 20
            if y < 40:  # Salto de página si el contenido supera una página
                c.showPage()
                y = height - 40
                c.setFont("Helvetica", 12)
        
        c.save()
        messagebox.showinfo("Exportar", f"El reporte se ha exportado como {pdf_filename}")
>>>>>>> 6ae52fe3f7c817e5fa033c0f542da4470b174d6a
