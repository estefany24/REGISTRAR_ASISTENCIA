import sqlite3
from tkinter import messagebox
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Carpeta modulos
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')  # Carpeta data
DB_PATH = os.path.join(DATA_DIR, 'asistencia.db')

def conectar_bd():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al conectar con la base de datos: {e}")
        return None
    
def obtener_password_por_nombre(nombre):
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM usuarios WHERE dni LIKE ?', ('%' + nombre + '%',))
        resultados = cursor.fetchone()
        print (resultados)
        return resultados
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener el ID del libro: {e}")
        return False
    finally:
        conn.close()