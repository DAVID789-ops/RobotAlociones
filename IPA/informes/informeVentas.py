import mysql.connector
from fpdf import FPDF
from datetime import datetime
import os

# Configuración de la base de datos
db_config = {
    'host': '50.87.172.242',
    'user': 'kjycupmy_david',
    'password': 'tF)4l&[;_cV2',
    'database': 'kjycupmy_crm2',
    'port': 3306
}

# Función para obtener la fecha del día anterior basado en la fecha actual del sistema
def obtener_fecha_anterior():
    conexion = mysql.connector.connect(**db_config)
    cursor = conexion.cursor()

    # Consulta para obtener la fecha más reciente (anterior a la actual) de la columna 'fecha'
    query_fecha = """
    SELECT MAX(
        CASE 
            WHEN fecha LIKE '____-__-__' THEN fecha  -- YYYY-MM-DD
            WHEN fecha LIKE '__/__/____' THEN STR_TO_DATE(fecha, '%d/%m/%Y')  -- DD/MM/YYYY
            ELSE NULL
        END
    ) AS fecha_anterior
    FROM ventas_clientes 
    WHERE 
        CASE 
            WHEN fecha LIKE '____-__-__' THEN fecha < CURDATE()  -- YYYY-MM-DD
            WHEN fecha LIKE '__/__/____' THEN STR_TO_DATE(fecha, '%d/%m/%Y') < CURDATE()  -- DD/MM/YYYY
            ELSE FALSE
        END
    """
    cursor.execute(query_fecha)
    fecha_anterior = cursor.fetchone()[0]
    
    conexion.close()

    if fecha_anterior:
        return fecha_anterior
    else:
        return None

# Función para obtener los datos del día anterior con JOIN para obtener nombre del cliente
def obtener_datos(fecha_anterior):
    conexion = mysql.connector.connect(**db_config)
    cursor = conexion.cursor()

    # Consulta para obtener los datos del día anterior en la tabla ventas_clientes y nombre del cliente
    query = f"""
    SELECT c.nombre, vc.fecha, vc.mensajero, vc.numero_guia, vc.monto 
    FROM ventas_clientes vc
    JOIN clientes c ON vc.id_cliente = c.id
    WHERE 
        (vc.fecha LIKE '____-__-__' AND vc.fecha = '{fecha_anterior}') 
        OR 
        (vc.fecha LIKE '__/__/____' AND STR_TO_DATE(vc.fecha, '%d/%m/%Y') = '{fecha_anterior}')
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    conexion.close()
    
    return resultados

# Función para generar el PDF
def generar_informe_pdf(datos, fecha_anterior):
    # Crear el PDF
    pdf = FPDF()
    pdf.add_page()

    # Agregar logo (ajustamos para que se vea bien en la parte superior)
    if os.path.exists('logo.png'):
        pdf.image('logo.png', 10, 8, 33)
    pdf.set_font('Arial', 'B', 12)
    pdf.ln(20)  # Añadimos un salto de línea para evitar que el logo se sobreponga con la tabla

    # Título con la fecha
    pdf.cell(0, 10, f'Informe de ventas del {fecha_anterior}', 0, 1, 'C')

    # Columnas del PDF
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(10, 10, 'Nº', 1)
    pdf.cell(40, 10, 'Nombre Cliente', 1)
    pdf.cell(30, 10, 'Fecha', 1)
    pdf.cell(40, 10, 'Mensajero', 1)
    pdf.cell(40, 10, 'No. Guía', 1)
    pdf.cell(30, 10, 'Monto (Q)', 1)  # Columna 'Monto' en la parte final
    pdf.ln()

    # Agregar datos
    pdf.set_font('Arial', '', 10)
    total_monto = 0
    for i, fila in enumerate(datos, 1):
        nombre, fecha, mensajero, numero_guia, monto = fila
        # Formatear la fecha para que se vea correctamente en el PDF
        try:
            fecha_formateada = datetime.strptime(fecha, '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            fecha_formateada = fecha  # Si el formato no es YYYY-MM-DD, usarlo como está

        pdf.cell(10, 10, str(i), 1)
        pdf.cell(40, 10, str(nombre), 1)
        pdf.cell(30, 10, str(fecha_formateada), 1)
        pdf.cell(40, 10, str(mensajero), 1)
        pdf.cell(40, 10, str(numero_guia), 1)
        pdf.cell(30, 10, f'Q{monto:.2f}', 1)  # Columna de Monto a la derecha
        pdf.ln()
        total_monto += monto

    # Agregar total del monto al final
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(160, 10, 'Total', 1)
    pdf.cell(30, 10, f'Q{total_monto:.2f}', 1)

    # Guardar el PDF en la ubicación especificada
    output_dir = r'E:\RobotAlociones\AlmacenIPA\Informes'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Crear el directorio si no existe

    output_path = os.path.join(output_dir, f'informe_ventas_{fecha_anterior}.pdf')
    pdf.output(output_path)
    print(f'Informe generado: {output_path}')

# Programa principal
if __name__ == '__main__':
    fecha_anterior = obtener_fecha_anterior()
    if fecha_anterior:
        datos = obtener_datos(fecha_anterior)
        if datos:
            generar_informe_pdf(datos, fecha_anterior)
        else:
            print('No se encontraron ventas para el día anterior.')
    else:
        print('No se pudo determinar la fecha anterior.')
