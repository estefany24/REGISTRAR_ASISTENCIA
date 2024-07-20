import tkinter as tk
import winsound
from scr.modulos import lista_personas
from scr.modulos import asistencia
from datetime import datetime
from tkinter import messagebox, ttk
from modelos import api_conculta
from PIL import Image, ImageTk
import os

class RegistrarAsistencia:
    def __init__(self, master):
        self.master = master
        self.master.title("Registrar Asistencia")
        self.master.geometry("400x420")
        self.master.configure(bg="#282c34") 
        self.master.resizable(False, False)
        self.ventana_agregar_abierta = False
        self.iniciar()
        
    def iniciar(self):
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'pictures', 'humano.png')
        if not os.path.exists(logo_path):
            messagebox.showerror("Error", f"No se encontró el logo en {logo_path}")
            return

        self.logo_img = Image.open(logo_path)
        self.logo_img = self.logo_img.resize((100,100), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo_img)

        # Etiqueta con el logo
        tk.Label(self.master, image=self.logo, bg="#282c34").grid(row=0, column=0, columnspan=2, pady=20)

        # Título al lado del logo
        tk.Label(self.master, text="Asistencia", font=("Arial", 20, "bold"), bg="#282c34", fg="#61dafb").grid(row=1, column=0, columnspan=2, pady=10)

        # Etiqueta DNI
        tk.Label(self.master, text="DNI:", font=("Arial", 14, "bold"), bg="#282c34", fg="#ffffff").grid(row=2, column=0, padx=10, pady=10, sticky='e')

        # Entrada DNI
        self.entry_dni = tk.Entry(self.master, font=("Arial", 14), bd=2, relief="solid")  # Añadido borde y mejorado el estilo
        self.entry_dni.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.entry_dni.bind('<Return>', self.mostrar_informacion)
        self.entry_dni.focus_set()

        # Etiqueta para mostrar información del usuario
        self.info_usuario = tk.Label(self.master, text="", font=("Arial", 12), bg="#282c34", fg="#ffffff")  # Cambiado el color del texto y la fuente
        self.info_usuario.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        # Botón de Registrar Asistencia
        self.btn_registrar = tk.Button(self.master, text="Registrar Asistencia", command=self.registrar_asistencia, state=tk.DISABLED,
                                      bg="#4CAF50", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                                      padx=20, pady=10,  # Tamaño del botón
                                      borderwidth=0,  # Eliminar el borde del botón
                                      highlightthickness=0,  # Eliminar el borde del foco
                                      activebackground="#45a049",  # Color de fondo cuando se presiona
                                      activeforeground="#ffffff",  # Color del texto cuando se presiona
                                      )
        self.btn_registrar.bind("<Enter>", lambda e: self.change_button_color(self.btn_registrar, "#45a049"))
        self.btn_registrar.bind("<Leave>", lambda e: self.change_button_color(self.btn_registrar, "#4CAF50"))
        self.btn_registrar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Botón de Salir
        tk.Button(self.master, text="Salir", command=self.logout, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=20, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  ).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Centrar todo
        for i in range(5):
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.master.grid_columnconfigure(i, weight=1)

        self.master.protocol("WM_DELETE_WINDOW", self.logout)

    def change_button_color(self, button, color):
        button.config(bg=color)

    def logout(self):
        self.master.destroy()
        from main import LoginWindow
        root = tk.Tk()
        app = LoginWindow(root)
        root.mainloop()

    def mostrar_informacion(self, event=None):
        dni = self.entry_dni.get()
        id_persona = lista_personas.obtener_id_por_dni(dni)

        if dni and len(dni) == 8:
            if id_persona:
                nombre = lista_personas.obtener_nombre_por_id(id_persona[0])
                apellido_pat = lista_personas.obtener_apellido_por_id(id_persona[0])

                if nombre and apellido_pat:
                    self.info_usuario.config(
                        text=f"          Nombre: {nombre} {apellido_pat}",
                        anchor="center",
                        bg="#282c34",  # Fondo del marco
                        fg="white"  # Color del texto
                    )

                    self.btn_registrar.config(state=tk.NORMAL)
                    # Registrar asistencia inmediatamente
                    self.registrar_asistencia()
                else:
                    self.info_usuario.config(text="No se pudo obtener el nombre o apellido_pat",
                                             anchor="center",
                                             bg="#282c34",  # Fondo del marco
                                             fg="white"  # Color del texto
                                             )
                    self.master.after(2000, self.limpiar_informacion)

            else:
                encontrado, datos_dni = api_conculta.verificar_si_existe(dni)
                if encontrado and datos_dni:
                    apellido_materno = datos_dni.get('apellido_materno')
                    apellido_paterno = datos_dni.get('apellido_paterno')
                    nombres = datos_dni.get('nombres')
                    dni_api = datos_dni.get('dni')
                    lista_personas.insertar_personas(nombres, apellido_paterno, apellido_materno, dni_api)

                    id_persona = lista_personas.obtener_id_por_dni(dni_api)
                    nombre = lista_personas.obtener_nombre_por_id(id_persona[0])
                    apellido_pat = lista_personas.obtener_apellido_por_id(id_persona[0])
                    hora = datetime.now().strftime("%H:%M:%S")
                    if nombre and apellido_pat:
                        self.info_usuario.config(
                            text=f"                  Nombre: {nombre} {apellido_pat}\n                  Hora de entrada: {hora}",
                            bg="#282c34",
                            fg="white"
                        )
                        self.btn_registrar.config(state=tk.NORMAL)
                        # Registrar asistencia inmediatamente
                        self.registrar_asistencia()
                    else:
                        self.info_usuario.config(text="No se pudo obtener el nombre o apellido_pat", bg="red")
                        self.master.after(2000, self.limpiar_informacion)
                else:
                    if not self.ventana_agregar_abierta:  # Verifica que la ventana de agregar usuario no esté abierta
                        self.crear_ventana_agregar_usuario()
                    else:
                        self.info_usuario.config(text="Ya está abierta una ventana para agregar el usuario.", bg="red")
        else:
            messagebox.showerror("Error", "Ingrese un DNI")
            self.master.after(2000, self.limpiar_informacion)

    def registrar_asistencia(self, event=None):
        dni = self.entry_dni.get()
        id_persona = lista_personas.obtener_id_por_dni(dni)

        if id_persona and asistencia.registra_asistencia(id_persona[0]):
            nombre = lista_personas.obtener_nombre_por_id(id_persona[0])
            apellido_pat = lista_personas.obtener_apellido_por_id(id_persona[0])

            if nombre:
                hora = datetime.now().strftime("%H:%M:%S")
                self.info_usuario.config(
                    text=f"                  Nombre: {nombre} {apellido_pat}\n                  Hora de entrada: {hora}",
                    bg="#282c34",
                    fg="white"
                )
                self.play_sound()
                self.master.after(5000, self.limpiar_informacion)  # Tiempo reducido a 2 segundos (2000 ms)
            else:
                self.info_usuario.config(text="No se pudo obtener el nombre o apellido_pat", bg="red")
                self.master.after(2000, self.limpiar_informacion)
        else:
            self.info_usuario.config(text="No se pudo registrar la asistencia", bg="red")
            self.master.after(2000, self.limpiar_informacion)

    def limpiar_informacion(self):
        self.entry_dni.delete(0, tk.END)
        self.info_usuario.config(text="", bg="#282c34")
        self.btn_registrar.config(state=tk.DISABLED)
        self.entry_dni.bind('<Return>', self.mostrar_informacion)
        self.entry_dni.focus_set()

    def play_sound(self):
        winsound.Beep(1000, 200)  # Sonido simple

    def crear_ventana_agregar_usuario(self):
        dni = self.entry_dni.get()
        self.ventana_agregar_abierta = True  # Marcar que la ventana de agregar usuario está abierta
        self.agregar_personas = tk.Toplevel(self.master)
        self.agregar_personas.geometry("400x450")
        self.agregar_personas.configure(bg="#282c34")
        self.agregar_personas.title("Agregar Usuario")

        logo_path = os.path.join(os.path.dirname(__file__), '..', 'pictures', 'logo_UNAP.png')
        if not os.path.exists(logo_path):
            messagebox.showerror("Error", f"No se encontró el logo en {logo_path}")
            return

        self.logo_img = Image.open(logo_path)
        self.logo_img = self.logo_img.resize((50, 50), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)

        label_font = ("Arial", 12, "bold")
        entry_font = ("Arial", 12)

        logo_frame = tk.Frame(self.agregar_personas, bg="#282c34")
        logo_frame.pack(pady=(20, 10))

        tk.Label(logo_frame, image=self.logo_photo, bg="#282c34").pack(side="left", padx=10)
        tk.Label(logo_frame, text="Agregando al Registro", font=("Arial", 16, "bold"), bg="#282c34", fg="#ffffff").pack(side="left")

        # Nombres
        tk.Label(self.agregar_personas, text="Nombres", font=label_font, bg="#282c34", fg="#ffffff").pack(pady=(20, 5))
        nombre_entry = tk.Entry(self.agregar_personas, font=entry_font, bd=2, relief="solid")
        nombre_entry.pack(pady=5)

        # Apellido paterno
        tk.Label(self.agregar_personas, text="Apellido paterno", font=label_font, bg="#282c34", fg="#ffffff").pack(pady=5)
        apellido_paterno_entry = tk.Entry(self.agregar_personas, font=entry_font, bd=2, relief="solid")
        apellido_paterno_entry.pack(pady=5)

        # Apellido materno
        tk.Label(self.agregar_personas, text="Apellido materno", font=label_font, bg="#282c34", fg="#ffffff").pack(pady=5)
        apellido_materno_entry = tk.Entry(self.agregar_personas, font=entry_font, bd=2, relief="solid")
        apellido_materno_entry.pack(pady=5)

        # DNI
        tk.Label(self.agregar_personas, text="DNI", font=label_font, bg="#282c34", fg="#ffffff").pack(pady=5)
        dni_entry = tk.Entry(self.agregar_personas, font=entry_font, bd=2, relief="solid")
        dni_entry.insert(0, dni)
        dni_entry.config(state='disabled')  # Hacer que el campo de DNI sea solo lectura
        dni_entry.pack(pady=5)

        def agregar_persona():
            nombre = nombre_entry.get()
            apellido_pat = apellido_paterno_entry.get()
            apellido_mat = apellido_materno_entry.get()
            dni = dni_entry.get()

            if nombre and apellido_pat and dni and apellido_mat:
                if lista_personas.insertar_personas(nombre, apellido_pat, apellido_mat, dni):
                    self.info_usuario.config(text="Persona agregada exitosamente", bg="green")
                    #self.play_sound()
                    # Cierra la ventana emergente
                    self.agregar_personas.destroy()
                    # Actualiza la ventana principal con la información del nuevo usuario
                    self.entry_dni.delete(0, tk.END)
                    self.entry_dni.insert(0, dni)
                    self.mostrar_informacion()
                    # Marca que la ventana de agregar usuario está cerrada
                    self.ventana_agregar_abierta = False
                else:
                    self.info_usuario.config(text="No se pudo agregar la persona.", bg="red")
                    self.master.after(2000, self.limpiar_informacion)
            else:
                self.info_usuario.config(text="Todos los campos son obligatorios.", bg="yellow")
                self.master.after(2000, self.limpiar_informacion)

        # Llamar a `agregar_persona` al presionar Enter en el último campo
        apellido_materno_entry.bind('<Return>', lambda event: agregar_persona())

        # Botón de agregar
        tk.Button(self.agregar_personas, text="Agregar", command=agregar_persona,
                bg='#4CAF50', fg='white', font=('Helvetica', 12, 'bold'),
                bd=0, relief="flat", activebackground="#45a049", activeforeground="white").pack(pady=10)

        self.agregar_personas.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.ventana_agregar_abierta = False
        self.agregar_personas.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrarAsistencia(root)
    root.mainloop()
