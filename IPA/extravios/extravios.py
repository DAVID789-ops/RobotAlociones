import mysql.connector
from mysql.connector import Error
from fpdf import FPDF
from datetime import datetime, timedelta
import os

# Configuración de la base de datos
db_config = { 
    'host': '50.87.172.242',
    'user': 'kjycupmy_david',
    'password': 'tF)4l&[;_cV2',
    'database': 'kjycupmy_crm2',
    'port': 3306
}

class PDF(FPDF):
    def header(self):
        # Logo con espacio para evitar que se mezcle
        self.image('logo.png', x=10, y=8, w=33)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'PAQUETES EXTRAVIADOS', ln=True, align='C')
        self.ln(15)  # Espacio después del encabezado (aumentado)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def obtener_datos():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # Calcular la fecha de hace 7 días
            fecha_limite = datetime.now() - timedelta(days=7)

            # Consulta SQL
            query = """
            SELECT vc.fecha, vc.numero_guia, vc.monto, vc.telefono, c.nombre
            FROM ventas_clientes vc
            JOIN clientes c ON vc.id_cliente = c.id
            WHERE vc.fecha <= %s AND vc.hecho = 1 AND (vc.entregado = 0 OR vc.entregado IS NULL) AND (vc.revisado = 0 OR vc.revisado IS NULL)
            """
            cursor.execute(query, (fecha_limite,))
            resultados = cursor.fetchall()

            for row in resultados:
                row['fecha'] = datetime.strptime(row['fecha'], '%Y-%m-%d')

            return resultados

    except Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def generar_pdf(datos, total):
    pdf = PDF()
    pdf.set_margins(10, 10, 10)  # Márgenes de 10 mm
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # Espaciado en el PDF
    pdf.cell(0, 10, '', 0, 1)  # Espacio en blanco
    
    # Cabeceras de la tabla
    pdf.cell(30, 10, 'Fecha', 1)
    pdf.cell(30, 10, 'Número Guía', 1)
    pdf.cell(30, 10, 'Monto', 1)
    pdf.cell(60, 10, 'Cliente', 1)
    pdf.cell(30, 10, 'Teléfono', 1)  # Nueva columna Teléfono
    pdf.cell(0, 10, '', 0, 1)  # Nueva línea
    
    for index, row in enumerate(datos):
        pdf.cell(30, 10, row['fecha'].strftime('%Y-%m-%d'), 1)
        
        numero_guia = row['numero_guia'] if row['numero_guia'] is not None else "No disponible"
        pdf.cell(30, 10, numero_guia, 1)
        
        monto = str(row['monto']) if row['monto'] is not None else "0"
        pdf.cell(30, 10, monto, 1)
        
        cliente_nombre = row['nombre'] if row['nombre'] is not None else "No disponible"
        pdf.cell(60, 10, cliente_nombre.encode('latin-1', 'replace').decode('latin-1'), 1)
        
        telefono = row['telefono'] if row['telefono'] is not None else "No disponible"
        pdf.cell(30, 10, telefono.encode('latin-1', 'replace').decode('latin-1'), 1)
        pdf.cell(0, 10, '', 0, 1)  # Nueva línea

    pdf.cell(90, 10, 'Total:', 1)
    pdf.cell(30, 10, str(total), 1)

    # Generar un nombre único para el archivo PDF
    base_path = 'E:\\RobotAlociones\\AlmacenIPA\\PaquetesExtraviados\\'
    base_name = 'paquetes_extraviados.pdf'
    output_path = os.path.join(base_path, base_name)
    
    # Verificar si el archivo ya existe
    if os.path.exists(output_path):
        # Si existe, generar un nuevo nombre
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(base_path, f'paquetes_extraviados_{timestamp}.pdf')

    pdf.output(output_path)

def actualizar_revisado(datos):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            for row in datos:
                update_query = """
                UPDATE ventas_clientes
                SET revisado = 1
                WHERE (numero_guia = %s OR numero_guia IS NULL) 
                  AND (entregado = 0 OR entregado IS NULL) 
                  AND (revisado = 0 OR revisado IS NULL)
                """
                cursor.execute(update_query, (row['numero_guia'],))
            connection.commit()

    except Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    datos = obtener_datos()
    
    if datos:
        total = sum(row['monto'] for row in datos)
        generar_pdf(datos, total)
        actualizar_revisado(datos)  # Actualizar la columna revisado después de generar el PDF
        print("PDF generado y registros actualizados correctamente.")
    else:
        print("No se encontraron registros que cumplan con los criterios.")

if __name__ == "__main__":
    main()
