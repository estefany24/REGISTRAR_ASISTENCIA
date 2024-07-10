import tkinter as tk
from tkinter import Tk, Menu
from tkcalendar import DateEntry  # Importación correcta de DateEntry
from tkinter import messagebox ,ttk,Menu
from scr.modulos import asistencia

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Informacion de asistencia")
        self.master.geometry("900x600")
        #self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Crear la barra de menú
        self.crear_menu()

    def crear_menu(self):
        menubar = Menu(self.master)
      
        # Menú Libros
        libros_menu = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="white", activeforeground="black", font=('Helvetica', 9))
        libros_menu.add_command(label="Reportes", command=self.mostrar_reportes_por_dia)
        menubar.add_cascade(label="Reportes", menu=libros_menu)

        # Menú Categorías
        categorias_menu = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="white", activeforeground="black", font=('Helvetica', 9))
        categorias_menu.add_command(label="Reporte semanal", command=self.mostrar_reporte_semanal)
        menubar.add_cascade(label="Reporte semanal", menu=categorias_menu)

        # Menú Autores
        autores_menu = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="white", activeforeground="black", font=('Helvetica', 9))
        autores_menu.add_command(label="Reporte semanal")
        menubar.add_cascade(label="Reporte semanal", menu=autores_menu)

        cerrar_sesion_menu = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="white", activeforeground="black", font=('Helvetica', 9))
        cerrar_sesion_menu.add_command(label="cargar datos")
        menubar.add_cascade(label="Cargar datos", menu=cerrar_sesion_menu)

        cerrar_sesion_menu = Menu(menubar, tearoff=0, bg="black", fg="white", activebackground="white", activeforeground="black", font=('Helvetica', 9))
        cerrar_sesion_menu.add_command(label="cerrar sesion", command=self.logout)
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
        
    def mostrar_reporte_semanal(self):
        self.limpiar_pantalla()
        self.agregar_barra_seleccion_fechas()
        self.crear_area_resultado_registro_SEMA()

    def limpiar_pantalla(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()
        # Aquí puedes agregar el código para las funcionalidades de tu aplicación


    def agregar_barra_reportes(self):
        search_frame = tk.Frame(self.master)
        search_frame.pack(pady=10)

        boton_reportes= tk.Button(search_frame,text="Reprote de hoy")
        boton_reportes.pack(side=tk.LEFT,padx=5)

        boton_inicio= tk.Button(search_frame,text="Fecha inicio")
        boton_inicio.pack(side=tk.LEFT,padx=5)

        boton_fin= tk.Button(search_frame,text="Fecha fin")
        boton_fin.pack(side=tk.LEFT,padx=5)


        search_button = tk.Button(search_frame, text="Buscar regsitro")
        search_button.pack(side=tk.LEFT, padx=5)


#OJO ESTA FUNCION SEMANAL NO ESTA UTILIZANDO 
    def crear_area_resultado_registro(self):
        self.resultados_frame = tk.Frame(self.master)
        self.resultados_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.resultados_frame, columns=('ID', 'Nombres','Apellidos','DNI'), show='headings', height=50)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombres', text='Nombres')
        self.tree.heading('Apellidos', text='Apellidos')
        self.tree.heading('DNI', text='DNI')
  
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.column('ID',width=5,anchor=tk.CENTER)
        self.tree.column('Nombres',width=180,anchor=tk.CENTER)
        self.tree.column('Apellidos',width=180,anchor=tk.CENTER)
        self.tree.column('DNI',width=180,anchor=tk.CENTER)
    


    def mostrar_datos_registro(self):
        resultados = asistencia.obtener_asistencia()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for resultado in resultados:
            self.tree.insert('', tk.END, values=resultado)

    
    #BARRA AGREGAR .. SEMANAL 
    def agregar_barra_seleccion_fechas(self):
        fechas_frame = tk.Frame(self.master)
        fechas_frame.pack(pady=10)

        tk.Label(fechas_frame, text="Fecha inicio:").pack(side=tk.LEFT, padx=5)
        self.fecha_inicio_entry = DateEntry(fechas_frame, date_pattern='yyyy-mm-dd')
        self.fecha_inicio_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(fechas_frame, text="Fecha fin:").pack(side=tk.LEFT, padx=5)
        self.fecha_fin_entry = DateEntry(fechas_frame, date_pattern='yyyy-mm-dd')
        self.fecha_fin_entry.pack(side=tk.LEFT, padx=5)

        boton_generar_reporte = tk.Button(fechas_frame, text="Generar reporte", command=self.mostrar_datos_semanales)
        boton_generar_reporte.pack(side=tk.LEFT, padx=5)



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

        self.tree = ttk.Treeview(self.resultados_frame, columns=('ID', 'Nombres', 'Fecha', 'Hora de entrada'), show='headings', height=50)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombres', text='Nombres')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Hora de entrada', text='Hora de entrada')

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.column('ID', width=5, anchor=tk.CENTER)
        self.tree.column('Nombres', width=180, anchor=tk.CENTER)
        self.tree.column('Fecha', width=180, anchor=tk.CENTER)
        self.tree.column('Hora de entrada', width=180, anchor=tk.CENTER)
