import sqlite3
from tkinter import messagebox
import os
from datetime import datetime

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
    
def registra_asistencia(usuario_id):
    conn = conectar_bd()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora_entrada = datetime.now().time().strftime("%H:%M")
        #hora_entrada="03:20"
        print(fecha)
        print(hora_entrada)
        print(usuario_id)

        cursor.execute('''
        INSERT INTO asistencia (lista_id, fecha, hora_entrada)
        VALUES (?, ?, ?)
        ''', (usuario_id, fecha, hora_entrada))
        conn.commit()

        return True
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener el ID del libro: {e}")
        return False
    finally:
        conn.close()


def obtener_asistencia():
    conn = conectar_bd()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT asistencia.id, lista_persona.nombres, lista_persona.apellido_pat, lista_persona.apellido_mat, lista_persona.dni, asistencia.hora_entrada, asistencia.fecha
        FROM asistencia
        INNER JOIN lista_persona ON asistencia.lista_id=lista_persona.ID
        ''')
        prestamos = cursor.fetchall()
        return prestamos
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener los préstamos: {e}")
        return []
    finally:
        conn.close()

# Función para obtener los datos de asistencia por intervalo de fecha
def obtener_asistencia_por_fecha(fecha_inicio, fecha_fin):
    conn = conectar_bd()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT asistencia.id, lista_persona.nombres, lista_persona.apellido_pat, lista_persona.apellido_mat, lista_persona.dni, asistencia.hora_entrada, asistencia.fecha
        FROM asistencia
        INNER JOIN lista_persona ON asistencia.lista_id = lista_persona.ID
        WHERE asistencia.fecha BETWEEN ? AND ?
        ORDER BY asistencia.fecha DESC  -- Ordenar por fecha descendente
        ''', (fecha_inicio, fecha_fin))
        asistencias = cursor.fetchall()
        return asistencias
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener la asistencia por fecha: {e}")
        return []
    finally:
        conn.close()

def obtener_grafico_por_fecha(fecha_inicio, fecha_fin):
    conn = conectar_bd()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT asistencia.id, lista_persona.nombres, asistencia.fecha, asistencia.hora_entrada 
        FROM asistencia
        INNER JOIN lista_persona ON asistencia.lista_id=lista_persona.ID
        WHERE asistencia.fecha BETWEEN ? AND ?
        ''', (fecha_inicio, fecha_fin))
        asistencias = cursor.fetchall()
        return asistencias
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener la asistencia por fecha: {e}")
        return []
    finally:
        conn.close()


import pandas as pd

def agregar_asistencia_desde_excel(df):
    conn = conectar_bd()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Convertir las fechas y horas a cadenas
        df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')
        df['hora_entrada'] = pd.to_datetime(df['hora_entrada'], format='%H:%M:%S').dt.strftime('%H:%M')

        for _, row in df.iterrows():
            cursor.execute('''
            INSERT INTO asistencia (lista_id, fecha, hora_entrada)
            VALUES (?, ?, ?)
            ''', (row['lista_id'], row['fecha'], row['hora_entrada']))
        
        conn.commit()
        messagebox.showinfo("Éxito", "Datos agregados correctamente a la base de datos.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al agregar datos a la base de datos: {e}")
    finally:
        conn.close()