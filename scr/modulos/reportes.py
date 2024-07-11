import sqlite3
from tkinter import messagebox
import os
from datetime import date

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
    
def obtener_asistencia_hoy():
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        hoy = date.today().strftime("%Y-%m-%d")
        query = "SELECT asistencia.id, lista_persona.nombres, lista_persona.apellido_pat, lista_persona.apellido_mat, lista_persona.dni, asistencia.hora_entrada, asistencia.fecha FROM asistencia INNER JOIN lista_persona ON asistencia.lista_id=lista_persona.ID WHERE fecha = ?"
        cursor.execute(query, (hoy,))
        resultados = cursor.fetchall()
        return resultados
    
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener el ID del libro: {e}")
        return False
    finally:
        conn.close()


def obtener_asistencias_en_rango(fecha_inicio, fecha_fin):
    conn = conectar_bd()
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return []

    cursor = conn.cursor()
    query = """
        SELECT asistencia.id, lista_persona.nombres, lista_persona.apellido_pat, lista_persona.apellido_mat, lista_persona.dni, asistencia.hora_entrada, asistencia.fecha
        FROM asistencia
        INNER JOIN lista_persona ON asistencia.lista_id = lista_persona.ID
        WHERE asistencia.fecha BETWEEN ? AND ?
        ORDER BY asistencia.fecha, asistencia.hora_entrada
    """
    cursor.execute(query, (fecha_inicio, fecha_fin))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
