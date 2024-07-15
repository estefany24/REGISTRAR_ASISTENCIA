import os
import sqlite3
from tkinter import Tk, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
import calendar

# Configura las rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Carpeta modulos
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')  # Carpeta data
DB_PATH = os.path.join(DATA_DIR, 'asistencia.db')

def conectar_bd():
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def exportar_datos_pdf(fecha):
    # Conectar a la base de datos
    conn = conectar_bd()
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return

    cursor = conn.cursor()
    # Obtener datos de la base de datos
    query = """
        SELECT asistencia.id, lista_persona.nombres, lista_persona.apellido_pat, lista_persona.apellido_mat, lista_persona.dni, asistencia.hora_entrada, asistencia.fecha
        FROM asistencia
        INNER JOIN lista_persona ON asistencia.lista_id = lista_persona.ID
        WHERE asistencia.fecha = ?
        ORDER BY asistencia.fecha ASC;  -- Ordenar por fecha ascendente
    """
    cursor.execute(query, (fecha,))
    resultados = cursor.fetchall()
    conn.close()

    # Crear una instancia de Tkinter para usar el diálogo de selección de archivo
    root = Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter
    
    # Abrir un diálogo para seleccionar el archivo PDF de destino
    archivo_pdf = filedialog.asksaveasfilename(defaultextension=".pdf",
                                              filetypes=[("PDF Files", "*.pdf")],
                                              title="Guardar archivo como",
                                              initialfile=f"reporte_asistencia_{fecha}.pdf")

    if not archivo_pdf:
        print("No se seleccionó ningún archivo. La exportación se canceló.")
        return

    # Crear el documento PDF
    doc = SimpleDocTemplate(archivo_pdf, pagesize=letter)
    elements = []

    # Estilos para el PDF
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='Title',
        fontSize=16,
        alignment=1,
        spaceAfter=12,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#003366")  # Dark Blue color
    )
    header_style = ParagraphStyle(
        name='Header',
        fontSize=12,
        alignment=1,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#FFFFFF"),  # White color
        backColor=colors.HexColor("#003366")  # Dark Blue color
    )
    table_header_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),  # Dark Blue color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#FFFFFF")),  # White color
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F0F0F0")),  # Light Grey color
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#D0D0D0")),  # Light Grey color for grid
    ])

    # Agregar el título del reporte
    title = Paragraph(f'Reporte de Asistencia para el {fecha}', title_style)
    elements.append(title)

    # Crear los datos de la tabla
    data = [['ID', 'Nombres', 'Apell. Paterno', 'Apell. Materno', 'DNI', 'Hora Entrada', 'Fecha']]
    for row in resultados:
        data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

    # Crear la tabla
    table = Table(data)
    table.setStyle(table_header_style)
    elements.append(table)

    # Crear el documento PDF
    doc.build(elements)
    print(f'El archivo PDF se ha creado con éxito: {archivo_pdf}')
# Asegúrate de tener esta función de conexión a la BD


 # Asegúrate de tener esta función de conexión a la BD

def exportar_datos_rango_pdf(fecha_inicio, fecha_fin):
    # Conectar a la base de datos
    conn = conectar_bd()
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return

    cursor = conn.cursor()
    cursor.execute("""
        SELECT asistencia.id, lista_persona.nombres, lista_persona.apellido_pat, lista_persona.apellido_mat, lista_persona.dni, asistencia.hora_entrada, asistencia.fecha
        FROM asistencia
        INNER JOIN lista_persona ON asistencia.lista_id = lista_persona.ID
        WHERE fecha BETWEEN ? AND ?
        ORDER BY asistencia.fecha ASC;  -- Ordenar por fecha ascendente
    """, (fecha_inicio, fecha_fin))
    datos = cursor.fetchall()
    conn.close()

    # Verificar que hay datos disponibles
    if not datos:
        print(f"No hay datos de asistencia para el rango de fechas {fecha_inicio} a {fecha_fin}.")
        return

    # Abrir un diálogo para seleccionar la carpeta de destino y el nombre del archivo
    archivo = filedialog.asksaveasfilename(defaultextension=".pdf",
                                          filetypes=[("PDF Files", "*.pdf")],
                                          title="Guardar archivo como",
                                          initialfile=f"reporte_asistencia_{fecha_inicio}_a_{fecha_fin}.pdf")
    if not archivo:
        print("No se seleccionó ningún archivo.")
        return

    # Crear el archivo PDF
    doc = SimpleDocTemplate(archivo, pagesize=letter)
    contenido = []

    # Obtener los estilos
    styles = getSampleStyleSheet()

    # Crear un estilo para el título
    titulo_style = ParagraphStyle(
        name='CustomTitle',
        fontSize=16,
        alignment=1,
        spaceAfter=12,
        parent=styles['Title']  # Usar 'Title' como base para el nuevo estilo
    )

    # Agregar el título del reporte
    contenido.append(Paragraph(f"Reporte de Asistencia del {fecha_inicio} al {fecha_fin}", style=titulo_style))

    # Preparar los datos para la tabla
    encabezados = ["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "DNI", "Hora Entrada", "Fecha"]
    datos_tabla = [encabezados] + [list(dato) for dato in datos]

    # Crear una tabla
    tabla = Table(datos_tabla)

    # Estilizar la tabla
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

    # Agregar la tabla al contenido del PDF
    contenido.append(tabla)

    # Construir el PDF
    doc.build(contenido)
    print(f"Datos exportados a {archivo}.")



def exportar_datos_mes_pdf(fecha_inicio, fecha_fin, mes, anio):
    # Conectar a la base de datos
    conn = conectar_bd()
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return

    cursor = conn.cursor()
    cursor.execute("""
        SELECT asistencia.id, lista_persona.nombres, lista_persona.apellido_pat, lista_persona.apellido_mat, lista_persona.dni, asistencia.hora_entrada, asistencia.fecha
        FROM asistencia
        INNER JOIN lista_persona ON asistencia.lista_id = lista_persona.ID
        WHERE strftime('%Y-%m', fecha) = ?
        ORDER BY asistencia.fecha ASC;  -- Ordenar por fecha ascendente
    """, (f"{anio}-{mes:02d}",))
    datos = cursor.fetchall()
    conn.close()

    # Verificar que hay datos disponibles
    if not datos:
        print(f"No hay datos de asistencia para el mes {mes}/{anio}.")
        return

    # Abrir un diálogo para seleccionar la carpeta de destino y el nombre del archivo
    archivo = filedialog.asksaveasfilename(defaultextension=".pdf",
                                          filetypes=[("PDF Files", "*.pdf")],
                                          title="Guardar archivo como",
                                          initialfile=f"reporte_asistencia_{mes}_{anio}.pdf")
    if not archivo:
        print("No se seleccionó ningún archivo.")
        return

    # Crear el archivo PDF
    doc = SimpleDocTemplate(archivo, pagesize=letter)
    contenido = []

    # Obtener los estilos
    styles = getSampleStyleSheet()

    # Crear un estilo para el título
    titulo_style = ParagraphStyle(
        name='CustomTitle',
        fontSize=16,
        alignment=1,
        spaceAfter=12,
        parent=styles['Title']  # Usar 'Title' como base para el nuevo estilo
    )

    # Agregar el título del reporte
    contenido.append(Paragraph(f"Reporte de Asistencia del {calendar.month_name[mes]} de {anio}", style=titulo_style))

    # Preparar los datos para la tabla
    encabezados = ["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "DNI", "Hora Entrada", "Fecha"]
    datos_tabla = [encabezados] + [list(dato) for dato in datos]

    # Crear una tabla
    tabla = Table(datos_tabla)

    # Estilizar la tabla
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

    # Agregar la tabla al contenido del PDF
    contenido.append(tabla)

    # Construir el PDF
    doc.build(contenido)
    print(f"Datos exportados a {archivo}.")
