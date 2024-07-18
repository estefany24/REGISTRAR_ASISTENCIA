import os
import sqlite3
from tkinter import filedialog
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import calendar
from datetime import datetime

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
    dias_formateados = ', '.join([f"'{dia.strftime('%Y-%m-%d')}'" for dia in dias_validos])
    cursor.execute(f"""
        SELECT strftime('%d', fecha)
        FROM asistencia
        WHERE lista_id = ? AND fecha IN ({dias_formateados})
    """, (persona_id,))
    asistencias = cursor.fetchall()
    return [int(dia[0]) for dia in asistencias]

def dividir_lista(lista):
    """Función para dividir una lista en dos partes aproximadamente iguales."""
    mitad = len(lista) // 2
    return lista[:mitad], lista[mitad:]

def exportar_datos_mensual_pdf(mes, anio):
    """Función principal para exportar el reporte de asistencia a PDF en un mes específico."""
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

    # Generar el rango de fechas para el mes y año especificados
    dias = [datetime(anio, mes, dia) for dia in range(1, calendar.monthrange(anio, mes)[1] + 1)]
    dias_1, dias_2 = dividir_lista(dias)

    # Nombre del archivo PDF
    nombre_mes = calendar.month_name[mes]
    archivo = filedialog.asksaveasfilename(defaultextension=".pdf",
                                           filetypes=[("PDF Files", "*.pdf")],
                                           title="Guardar reporte de asistencia",
                                           initialfile=f"reporte_asistencia_{nombre_mes}_{anio}.pdf")

    if not archivo:
        print("No se seleccionó ningún archivo.")
        conn.close()
        return

    # Crear el documento PDF en orientación horizontal
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

    contenido.append(Paragraph(f"Reporte de Asistencia de {nombre_mes} de {anio}", style=titulo_style))

    def crear_tabla(personas, dias):
        encabezados = ['Apellido Pat', 'Apellido Mat', 'Nombres', 'DNI'] + [dia.strftime('%d') for dia in dias]
        datos_tabla = [encabezados]

        for persona in personas:
            persona_id = persona[0]
            apellido_pat = persona[1]
            apellido_mat = persona[2]
            nombres = persona[3]
            dni = persona[4]

            asistencias = obtener_asistencias(cursor, persona_id, dias)
            asistencia_formateada = ['✓' if dia.day in asistencias else ' ' for dia in dias]
            datos_tabla.append([apellido_pat, apellido_mat, nombres, dni] + asistencia_formateada)

        # Ajustar los anchos de las columnas
        tabla = Table(datos_tabla, colWidths=[2.5 * cm, 2.5 * cm, 3 * cm, 2.5 * cm] + [0.75 * cm] * len(dias))
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#D0E0F0")),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        return tabla

    # Crear y agregar las dos tablas al contenido del PDF
    contenido.append(crear_tabla(personas, dias_1))
    contenido.append(PageBreak())
    contenido.append(crear_tabla(personas, dias_2))

    # Cerrar conexión a la base de datos
    conn.close()

    # Generar el documento PDF
    doc.build(contenido)
    print(f"Datos exportados a {archivo}.")

# Ejemplo de llamada a la función
exportar_datos_mensual_pdf(7, 2024)  # Ejemplo para julio de 2024
