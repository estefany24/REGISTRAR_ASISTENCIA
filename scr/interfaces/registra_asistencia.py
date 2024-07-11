import tkinter as tk
import winsound
from scr.modulos import lista_personas
from scr.modulos import asistencia
from datetime import datetime
from tkinter import messagebox
from modelos import api_conculta
from PIL import Image, ImageTk
import os

class RegistrarAsistencia:
    def __init__(self, master):
        self.master = master
        self.master.title("Registrar Asistencia")
        self.master.geometry("400x400")
        self.master.configure(bg="#282c34") 
        self.ventana_agregar_abierta = False
        self.iniciar()
        

    def iniciar(self):
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'pictures', 'logo_UNAP.png')
        if not os.path.exists(logo_path):
            messagebox.showerror("Error", f"No se encontró el logo en {logo_path}")
            return

        self.logo_img = Image.open(logo_path)
        self.logo_img = self.logo_img.resize((50, 50), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)

        # Etiqueta con el logo
        self.logo_label = tk.Label(self.master, image=self.logo_photo, bg="#282c34")
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Título al lado del logo
        tk.Label(self.master, text="Asistencia", font=("Arial", 20, "bold"), bg="#282c34", fg="#ffffff").grid(row=0, column=1, padx=10, pady=10, sticky='w')


        # Etiqueta DNI
        tk.Label(self.master, text="DNI:", font=("Arial", 14, "bold"), bg="#282c34", fg="#ffffff").grid(row=1, column=0, padx=10, pady=10, sticky='e')

        # Entrada DNI
        self.entry_dni = tk.Entry(self.master, font=("Arial", 14), bd=2, relief="solid")  # Añadido borde y mejorado el estilo
        self.entry_dni.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.entry_dni.bind('<Return>', self.mostrar_informacion)
        self.entry_dni.focus_set()

        # Etiqueta para mostrar información del usuario
        self.info_usuario = tk.Label(self.master, text="", font=("Arial", 12), bg="#282c34", fg="#ffffff")  # Cambiado el color del texto y la fuente
        self.info_usuario.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='w')

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
        self.btn_registrar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Botón de Salir
        tk.Button(self.master, text="Salir", command=self.logout, bg="#f44336", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                  padx=20, pady=10,  # Tamaño del botón
                  borderwidth=0,  # Eliminar el borde del botón
                  highlightthickness=0,  # Eliminar el borde del foco
                  activebackground="#e53935",  # Color de fondo cuando se presiona
                  activeforeground="#ffffff",  # Color del texto cuando se presiona
                  ).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

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

        if dni and len(dni)==8:
            if id_persona:
                nombre = lista_personas.obtener_nombre_por_id(id_persona[0])
                apellido_pat = lista_personas.obtener_apellido_por_id(id_persona[0])

                if nombre and apellido_pat:
                    self.info_usuario.config(text=f"Nombre: {nombre} {apellido_pat}", bg="yellow")
                    self.btn_registrar.config(state=tk.NORMAL)
                    # Desvincular el evento '<Return>' para evitar que se llame a `registrar_asistencia` más de una vez
                    self.master.unbind('<Return>')
                    # Solo vincular el evento '<Return>' para llamar a `registrar_asistencia` una vez
                    self.master.bind('<Return>', self.registrar_asistencia)
                else:
                    self.info_usuario.config(text="No se pudo obtener el nombre o apellido_pat", bg="red")
                    self.master.after(2000, self.limpiar_informacion)

            else:
                encontrado, datos_dni = api_conculta.verificar_si_existe(dni)
                if encontrado and datos_dni:
                    apellido_materno = datos_dni.get('apellido_materno')
                    apellido_paterno = datos_dni.get('apellido_paterno')
                    nombres = datos_dni.get('nombres')
                    dni_api = datos_dni.get('dni')
                    lista_personas.insertar_personas(nombres, apellido_paterno, apellido_materno, dni_api)
                    print(f"Apellido Materno: {apellido_materno}")
                    print(f"Apellido Paterno: {apellido_paterno}")
                    print(f"Nombres: {nombres}")
                    print(f"DNI: {dni_api}")

                    id_persona = lista_personas.obtener_id_por_dni(dni_api)
                    nombre = lista_personas.obtener_nombre_por_id(id_persona[0])
                    apellido_pat = lista_personas.obtener_apellido_por_id(id_persona[0])

                    if nombre and apellido_pat:
                        self.info_usuario.config(text=f"Nombre: {nombres} {apellido_paterno}", bg="yellow")
                        self.btn_registrar.config(state=tk.NORMAL)
                        # Desvincular el evento '<Return>' para evitar que se llame a `registrar_asistencia` más de una vez
                        self.master.unbind('<Return>')
                        # Solo vincular el evento '<Return>' para llamar a `registrar_asistencia` una vez
                        self.master.bind('<Return>', self.registrar_asistencia)
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

            if nombre and apellido_pat:
                #messagebox.showinfo("exito","asistencia registrada")
                self.play_sound()
                self.master.after(1000, self.limpiar_informacion)  # Tiempo reducido a 1 segundo (1000 ms)
            else:
                self.info_usuario.config(text="No se pudo obtener el nombre o apellido_pat", bg="red")
                self.master.after(2000, self.limpiar_informacion)
        else:
            self.info_usuario.config(text="No se pudo registrar la asistencia", bg="red")
            self.master.after(2000, self.limpiar_informacion)

        # Desvincular el evento '<Return>' después de registrar la asistencia para evitar múltiples llamadas
        self.master.unbind('<Return>')

    def limpiar_informacion(self):
        self.entry_dni.delete(0, tk.END)
        self.info_usuario.config(text="", bg="white")
        self.btn_registrar.config(state=tk.DISABLED)
        self.iniciar()

    def play_sound(self):
        winsound.Beep(1000, 200)  # Sonido simple

    def crear_ventana_agregar_usuario(self):
        dni = self.entry_dni.get()
        self.ventana_agregar_abierta = True  # Marcar que la ventana de agregar usuario está abierta
        self.agregar_personas = tk.Toplevel(self.master)
        self.agregar_personas.title("Agregar Usuario")

        tk.Label(self.agregar_personas, text="Nombres").pack()
        nombre_entry = tk.Entry(self.agregar_personas)
        nombre_entry.pack()

        tk.Label(self.agregar_personas, text="Apellido paterno").pack()
        apellido_paterno_entry = tk.Entry(self.agregar_personas)
        apellido_paterno_entry.pack()

        tk.Label(self.agregar_personas, text="Apellido materno").pack()
        apellido_materno_entry = tk.Entry(self.agregar_personas)
        apellido_materno_entry.pack()

        tk.Label(self.agregar_personas, text="DNI").pack()
        dni_entry = tk.Entry(self.agregar_personas)
        dni_entry.insert(0, dni)
        dni_entry.config(state='disabled')  # Hacer que el campo de DNI sea solo lectura
        dni_entry.pack()

        

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
        tk.Button(self.agregar_personas, text="Agregar", command=agregar_persona, bg='#4CAF50', fg='white', font=('Helvetica', 12, 'bold')).pack(pady=10)

        self.agregar_personas.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.ventana_agregar_abierta = False
        self.agregar_personas.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrarAsistencia(root)
    root.mainloop()

