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
    
def obtener_id_por_dni(dni):
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT ID FROM lista_persona WHERE dni LIKE ?', ('%' + dni + '%',))
        resultados = cursor.fetchone()
        print(resultados)
        if resultados is None:
            return False
        else:
            return resultados
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener el ID del libro: {e}")
        return False
    finally:
        conn.close()

def obtener_nombre_por_id(id):
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT nombres FROM lista_persona WHERE ID = ?', (id,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        return None
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener el nombre: {e}")
        return None
    finally:
        conn.close()

def obtener_apellido_por_id(id):
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT apellido_pat FROM lista_persona WHERE ID = ?', (id,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        return None
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener el apellido: {e}")
        return None
    finally:
        conn.close()

def insertar_personas(nombre, apellido_pat, apellido_mat, dni):
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO lista_persona (nombres, apellido_pat, apellido_mat, dni)
        VALUES (?, ?, ?, ?)
        ''', (nombre, apellido_pat, apellido_mat, dni))
        conn.commit()

        return True
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al insertar la persona: {e}")
        return False
    finally:
        conn.close()
