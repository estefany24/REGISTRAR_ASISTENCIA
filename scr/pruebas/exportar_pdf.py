from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import calendar
import sqlite3
import os
import tkinter as tk
from tkinter import filedialog

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Carpeta del archivo actual
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')  # Carpeta 'data' relativa al archivo actual
DB_PATH = os.path.join(DATA_DIR, 'asistencia.db')  # Ruta a la base de datos SQLite

def conectar_bd():
    """Función para conectar a la base de datos SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def obtener_asistencias(cursor, persona_id, dias_validos):
    """Función para obtener las asistencias de una persona en días específicos."""
    dias_formateados = ', '.join([str(dia) for dia in dias_validos])
    cursor.execute(f"""
        SELECT strftime('%d', fecha)
        FROM asistencia
        WHERE lista_id = ? AND strftime('%d', fecha) IN ({dias_formateados})
    """, (persona_id,))
    asistencias = cursor.fetchall()
    return [dia[0] for dia in asistencias]

def exportar_datos_mes_pdf(mes, anio):
    """Función principal para exportar el reporte de asistencia a PDF."""
    conn = conectar_bd()
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return

    cursor = conn.cursor()

    # Obtener todas las personas de lista_persona ordenadas por apellido y nombre
    cursor.execute("""
        SELECT 
            ID,
            apellido_pat,
            apellido_mat,
            nombres,
            dni
        FROM lista_persona
        ORDER BY apellido_pat, apellido_mat, nombres
    """)
    personas = cursor.fetchall()

    # Obtener el nombre del mes
    nombre_mes = calendar.month_name[mes]

    # Nombre del archivo PDF
    archivo = filedialog.asksaveasfilename(defaultextension=".pdf",
                                          filetypes=[("PDF Files", "*.pdf")],
                                          title=f"Guardar reporte de asistencia de {nombre_mes} de {anio}",
                                          initialfile=f"reporte_asistencia_{nombre_mes}_{anio}.pdf")

    if not archivo:
        print("No se seleccionó ningún archivo.")
        conn.close()
        return

    # Crear el documento PDF
    doc = SimpleDocTemplate(archivo, pagesize=letter)
    contenido = []

    # Estilos para el contenido del PDF
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        name='CustomTitle',
        fontSize=16,
        alignment=1,
        spaceAfter=12,
        parent=styles['Title']
    )

    # Obtener las semanas del mes y año especificados
    semanas_del_mes = calendar.monthcalendar(anio, mes)

    # Estructura para almacenar las asistencias de cada persona por semana
    asistencias_persona = {}
    for persona in personas:
        persona_id = persona[0]
        apellido_pat = persona[1]
        apellido_mat = persona[2]
        nombres = persona[3]
        dni = persona[4]

        # Inicializar las asistencias para la persona
        asistencias_persona[(apellido_pat, apellido_mat, nombres, dni)] = {str(week + 1): '' for week in range(len(semanas_del_mes))}

        # Obtener asistencias para cada semana
        for week, dias_validos in enumerate(semanas_del_mes):
            # Filtrar días válidos (diferentes de 0)
            dias_validos = [dia for dia in dias_validos if dia != 0]
            # Obtener asistencias para la persona en los días válidos de la semana
            asistencias = obtener_asistencias(cursor, persona_id, dias_validos)
            # Marcar asistencias en la estructura de datos
            asistencias_persona[(apellido_pat, apellido_mat, nombres, dni)][str(week + 1)] = ' '.join(asistencias)

    # Construir el contenido del PDF
    for semana in range(1, len(semanas_del_mes) + 1):
        semana_actual = str(semana)
        contenido.append(Paragraph(f"Semana {semana_actual} de {nombre_mes} de {anio}", titulo_style))

        # Cabecera de la tabla
        encabezados = ["Apellidos", "Nombres", "DNI", "L", "M", "M", "J", "V", "S", "D"]
        datos_tabla = [encabezados]

        # Llenar datos de la tabla
        for persona, asistencias_semana in asistencias_persona.items():
            apellido_pat, apellido_mat, nombres, dni = persona
            asistencias = asistencias_semana[semana_actual].split() if semana_actual in asistencias_semana else []

            # Marcar asistencias con ✔
            asistencias_formateadas = ['✔' if str(dia) in asistencias else '' for dia in ['L', 'M', 'M', 'J', 'V', 'S', 'D']]
            fila = [f"{apellido_pat} {apellido_mat}", nombres, dni] + asistencias_formateadas
            datos_tabla.append(fila)

        # Crear y estilizar la tabla
        tabla = Table(datos_tabla)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#4F81BD'),
            ('TEXTCOLOR', (0, 0), (-1, 0), '#FFFFFF'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#D0E0F0'),
            ('GRID', (0, 0), (-1, -1), 1, '#B5B5B5'),
        ]))

        contenido.append(tabla)
        contenido.append(PageBreak())  # Agregar salto de página entre semanas

    # Eliminar el último salto de página si existe
    if contenido[-1] == PageBreak():
        del contenido[-1]

    # Cerrar conexión a la base de datos
    conn.close()

    # Generar el documento PDF
    doc.build(contenido)
    print(f"Datos exportados a {archivo}.")

# Llamada de ejemplo a la función
exportar_datos_mes_pdf(7, 2024)  # Ejemplo de llamada para julio de 2024
