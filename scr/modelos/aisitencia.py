import sqlite3

def registrar_asistencia(dni):
    try:
        conexion = sqlite3.connect('scr1/data/REGISTRO.db')
        cursor = conexion.cursor()

        # Utiliza DATETIME("now") para obtener fecha y hora
        cursor.execute('INSERT INTO asistencias (dni, fecha) VALUES (?, DATETIME("now", "localtime"))', (dni,))
        
        conexion.commit()
        conexion.close()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error al registrar asistencia: {e}")
        return False

def obtener_asistencias():
    conexion = sqlite3.connect('scr1/data/ABIBLIOTECA.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT dni, fecha FROM asistencias')
    datos = cursor.fetchall()
    conexion.close()
    return datos
