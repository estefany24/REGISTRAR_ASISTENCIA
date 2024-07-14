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
        categorias_menu.add_command(label="Reporte semanal",command=self.mostrar_reporte_semanal)
        menubar.add_cascade(label="Reporte Semanal", menu=categorias_menu)

        # Menú Reporte Semanal
        autores_menu = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="white", activeforeground="black", font=('Helvetica', 9))
        autores_menu.add_command(label="Reporte mensual", command=self.mostrar_reporte_mensual)
        menubar.add_cascade(label="Reporte mensual", menu=autores_menu)

        # Menú Cargar Datos
        cerrar_sesion_menu = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="white", activeforeground="black", font=('Helvetica', 9))
        cerrar_sesion_menu.add_command(label="Cargar datos(excel)",command=self.crear_barra_añadir_excel_asistencia)
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
        self.agregar_botones_reportes()

    def mostrar_reporte_mensual(self):
        self.limpiar_pantalla()
        self.agregar_barra_seleccion_mes()
        self.crear_area_resultado_registro_SEMA()
        self.agregar_boton_exportarMEN()
        self.agregar_boton_graficoMEN()

    def mostrar_reporte_semanal(self):
        self.limpiar_pantalla()
        self.agregar_barra_seleccion_fechas()
        self.crear_area_resultado_registro_SEMA()
        self.agregar_boton_exportar()
        self.agregar_boton_grafico()
        
    def agregar_boton_exportarMEN(self):
        exportar_frame = tk.Frame(self.master)
        exportar_frame.pack(pady=10)
        boton_exportar = tk.Button(exportar_frame, text="Exportar", command=self.exportar_a_pdf_MESUAL)
        boton_exportar.pack()

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
    
    def exportar_a_pdf_MESUAL(self):

        mes = int(self.mes_entry.get())
        anio = int(self.anio_entry.get())

        fecha_inicioS = f"{anio}-{mes:02d}-01"
        fecha_finN = f"{anio}-{mes:02d}-{calendar.monthrange(anio, mes)[1]:02d}"

        if fecha_inicioS > fecha_finN:
            messagebox.showerror("Error", "La fecha final debe ser mayor o igual a la fecha de inicio.")
            return
        
        # Llamar a la función de exportación con el rango de fechas
        exportar_pdf.exportar_datos_rango_pdf(fecha_inicioS, fecha_finN)
        messagebox.showinfo("Éxito", "Datos exportados a PDF exitosamente.")

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

        boton_inicio = tk.Button(search_frame, text="Actualizar", command=self.mostrar_reportes_por_dia)
        boton_inicio.pack(side=tk.LEFT, padx=5)

        # Guardar el botón de exportar en una variable de instancia
        self.boton_fin = tk.Button(search_frame, text="Exportar", command=self.exportar_datos_hoy)
        self.boton_fin.pack(side=tk.LEFT, padx=5)

    def crear_area_resultado_registro(self):
        self.resultados_frame = tk.Frame(self.master)
        self.resultados_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.resultados_frame, columns=('ID', 'Nombres', 'Apellido Pat', 'Apellido Mat', 'DNI', 'Hora Entrada'), show='headings', height=15)
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
    

    def agregar_barra_seleccion_mes(self):
        mes_frame = tk.Frame(self.master)
        mes_frame.pack(pady=10)

        tk.Label(mes_frame, text="Seleccione el mes y el año:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.mes_entry = ttk.Combobox(mes_frame, values=list(range(1, 13)), state="readonly")
        self.mes_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.mes_entry.current(datetime.now().month - 1)
        
        self.anio_entry = ttk.Combobox(mes_frame, values=list(range(2000, datetime.now().year + 1)), state="readonly")
        self.anio_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.anio_entry.current(datetime.now().year - 2000)

        boton_generar_reporte = tk.Button(mes_frame, text="Generar reporte", command=self.mostrar_datos_mensuales)
        boton_generar_reporte.grid(row=1, columnspan=3, padx=5, pady=10)
    
    

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

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.column('ID', width=5, anchor=tk.CENTER)
        self.tree.column('Nombres', width=100, anchor=tk.CENTER)
        self.tree.column('Apellido Pat', width=100, anchor=tk.CENTER)
        self.tree.column('Apellido Mat', width=100, anchor=tk.CENTER)
        self.tree.column('DNI', width=100, anchor=tk.CENTER)
        self.tree.column('Hora Entrada', width=100, anchor=tk.CENTER)
        self.tree.column('Fecha',width=180, anchor=tk.CENTER)


    def agregar_boton_grafico(self):
            grafico_frame = tk.Frame(self.master)
            grafico_frame.pack(pady=10)
            boton_grafico = tk.Button(grafico_frame, text="Ver gráfico", command=self.mostrar_grafico_semanal)
            boton_grafico.pack(side=tk.LEFT, padx=5)
    def agregar_boton_graficoMEN(self):
            grafico_frame = tk.Frame(self.master)
            grafico_frame.pack(pady=10)
            boton_grafico = tk.Button(grafico_frame, text="Ver gráfico", command=self.mostrar_grafico_mensual)
            boton_grafico.pack(side=tk.LEFT, padx=5)

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
