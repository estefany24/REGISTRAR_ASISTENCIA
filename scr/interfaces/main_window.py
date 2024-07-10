import tkinter as tk
from tkinter import Tk, Menu
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
        categorias_menu.add_command(label="Reporte semanal")
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


        exel_button = tk.Button(search_frame, text="Exel")
        exel_button.pack(side=tk.LEFT, padx=5)



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