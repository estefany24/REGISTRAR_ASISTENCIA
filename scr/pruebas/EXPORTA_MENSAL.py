import sqlite3
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime, timedelta, date
from calendar import monthrange
import os

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

def obtener_asistencias(cursor, persona_id, fecha_inicio, fecha_fin):
    """Obtiene las asistencias para una persona en un rango de fechas."""
    cursor.execute("""
        SELECT fecha FROM asistencia 
        WHERE lista_id = ? AND fecha BETWEEN ? AND ?
    """, (persona_id, fecha_inicio, fecha_fin))
    asistencias = cursor.fetchall()
    return {datetime.strptime(a[0], '%Y-%m-%d').day for a in asistencias}

def exportar_datos_mensual_pdf(mes, anio):
    """Función principal para exportar el reporte de asistencia mensual a PDF."""
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

    # Nombre del archivo PDF
    archivo = filedialog.asksaveasfilename(defaultextension=".pdf",
                                           filetypes=[("PDF Files", "*.pdf")],
                                           title="Guardar reporte de asistencia",
                                           initialfile=f"reporte_asistencia_{mes}_{anio}.pdf")

    if not archivo:
        print("No se seleccionó ningún archivo.")
        conn.close()
        return

    # Crear el documento PDF
    doc = SimpleDocTemplate(archivo, pagesize=landscape(letter))
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

    contenido.append(Paragraph(f"Reporte de Asistencia del {mes} de {anio}", style=titulo_style))

    # Generar el rango de fechas
    fecha_inicio = date(anio, mes, 1)
    _, num_days = monthrange(anio, mes)
    fecha_fin = date(anio, mes, num_days)
    dias = [fecha_inicio + timedelta(days=i) for i in range(num_days)]

    # Preparar los datos para la tabla
    encabezados = ['Apellido Pat', 'DNI'] + [dia.strftime('%d') for dia in dias]
    datos_tabla = [encabezados]

    # Obtener los datos de asistencia
    for persona in personas:
        persona_id = persona[0]
        apellido_pat = persona[1]
        dni = persona[4]

        # Obtener asistencias para la persona en el rango de fechas
        asistencias = obtener_asistencias(cursor, persona_id, fecha_inicio, fecha_fin)
        asistencia_formateada = ['✓' if dia.day in asistencias else '' for dia in dias]
        datos_tabla.append([apellido_pat, dni] + asistencia_formateada)

    # Crear la tabla
    tabla = Table(datos_tabla)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#D0E0F0")),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    contenido.append(tabla)

    # Cerrar conexión a la base de datos
    conn.close()

    # Generar el documento PDF
    doc.build(contenido)
    messagebox.showinfo("Éxito", f"Datos exportados a {archivo}.")

# Ejemplo de llamada a la función
mes = 7
anio = 2024
exportar_datos_mensual_pdf(mes, anio)
