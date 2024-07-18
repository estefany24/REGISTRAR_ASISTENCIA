import tkinter as tk
from tkinter import messagebox
from scr.modulos import usuarios
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
import bcrypt

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Inicio de Sesión")
        self.master.geometry("400x450")
        self.master.configure(bg="#282c34")  # Fondo oscuro de la ventana

        # Agregar espacio para el logo
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pictures', 'Logo_UNAP.png')

        # Verificar si el logo existe
        if not os.path.exists(logo_path):
            messagebox.showerror("Error", f"No se encontró el logo en {logo_path}")
            return

        # Redimensionar el logo
        image = Image.open(logo_path)
        image = image.resize((120, 120), Image.LANCZOS)  # Ajusta el tamaño del logo
        self.logo = ImageTk.PhotoImage(image)

        tk.Label(self.master, image=self.logo, bg="#282c34").grid(row=0, column=0, columnspan=2, pady=20)

        # Título
        ttk.Label(self.master, text="Registro de Asistencia", font=("Arial", 20, "bold"), background="#282c34", foreground="#61dafb").grid(row=1, column=0, columnspan=2, pady=10)

        # Etiqueta de Usuario
        ttk.Label(self.master, text="Usuario:", background="#282c34", foreground="#ffffff").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_usuario = ttk.Entry(self.master, font=("Arial", 14))
        self.entry_usuario.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        # Etiqueta de Contraseña
        ttk.Label(self.master, text="Contraseña:", background="#282c34", foreground="#ffffff").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.entry_contrasena = ttk.Entry(self.master, show="*", font=("Arial", 14))
        self.entry_contrasena.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        self.btn_iniciar_sesion = tk.Button(self.master, text="Iniciar Sesión", command=self.iniciar_sesion,
                                           bg="#4CAF50", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                                           padx=20, pady=10,  # Aumentar el tamaño del botón
                                           borderwidth=0,  # Eliminar el borde del botón
                                           highlightthickness=0,  # Eliminar el borde del foco
                                           activebackground="#ebed6b",  # Color de fondo cuando se presiona
                                           activeforeground="#ffffff",  # Color del texto cuando se presiona
                                           )
        self.btn_iniciar_sesion.bind("<Enter>", lambda e: self.change_button_color(self.btn_iniciar_sesion, "#ebed6b"))
        self.btn_iniciar_sesion.bind("<Leave>", lambda e: self.change_button_color(self.btn_iniciar_sesion, "#4CAF50"))
        self.btn_iniciar_sesion.grid(row=4, column=0, columnspan=2, padx=10, pady=15)

        # Botón de Continuar como Usuario
        self.btn_continuar_como_usuario = tk.Button(self.master, text="Continuar como Usuario", command=self.continuar_como_usuario,
                                                   bg="#61dafb", fg="#ffffff", font=("Arial", 12, "bold"), relief="flat",
                                                   padx=20, pady=10,  # Aumentar el tamaño del botón
                                                   borderwidth=0,  # Eliminar el borde del botón
                                                   highlightthickness=0,  # Eliminar el borde del foco
                                                   activebackground="#4a90e2",  # Color de fondo cuando se presiona
                                                   activeforeground="#ffffff",  # Color del texto cuando se presiona
                                                   )
        self.btn_continuar_como_usuario.bind("<Enter>", lambda e: self.change_button_color(self.btn_continuar_como_usuario, "#4a90e2"))
        self.btn_continuar_como_usuario.bind("<Leave>", lambda e: self.change_button_color(self.btn_continuar_como_usuario, "#61dafb"))
        self.btn_continuar_como_usuario.grid(row=5, column=0, columnspan=2, padx=10, pady=15)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Centrar todo
        for i in range(6):
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.master.grid_columnconfigure(i, weight=1)

    def change_button_color(self, button, color):
        button.config(bg=color)

    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Realmente desea cerrar la aplicación?"):
            self.master.destroy()

    def verificar_contrasena(self, password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except ValueError as e:
            print(f"Error al verificar contraseña: {e}")
            return False

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        
        try:
            # Obtener la contraseña encriptada de la base de datos
            resultado = usuarios.obtener_password_por_nombre(usuario)
            if resultado:
                comparar_contraseña = resultado[0]
            else:
                comparar_contraseña = None
        except Exception as e:
            print(f"Error al obtener la contraseña: {e}")
            comparar_contraseña = None

        # Verificar la contraseña usando bcrypt
        if usuario and comparar_contraseña and self.verificar_contrasena(contrasena, comparar_contraseña):
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.master.destroy()
            self.abrir_ventana_admin()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def continuar_como_usuario(self):
        self.master.destroy()
        self.abrir_ventana_general()

    def abrir_ventana_general(self):
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from interfaces.registra_asistencia import RegistrarAsistencia  # Asegúrate de importar la clase RegistrarAsistencia
        ventana_principal = tk.Tk()
        app = RegistrarAsistencia(ventana_principal)
        ventana_principal.mainloop()

    def abrir_ventana_admin(self):
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from interfaces.main_window import MainWindow  # Asegúrate de importar la clase MainWindow
        ventana_principal = tk.Tk()
        app = MainWindow(ventana_principal)
        ventana_principal.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
