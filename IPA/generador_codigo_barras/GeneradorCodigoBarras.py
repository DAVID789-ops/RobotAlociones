import mysql.connector
from datetime import datetime, timedelta
import os
import barcode
from barcode.writer import ImageWriter
from fpdf import FPDF

# Configuración de la conexión a la base de datos
db_config = {
    'host': '50.87.172.242',
    'user': 'kjycupmy_david',
    'password': 'tF)4l&[;_cV2',
    'database': 'kjycupmy_crm2',
    'port': 3306
}

# Ruta donde se guardan los PDFs y la imagen del logo
output_pdf_path = "E:\\RobotAlociones\\AlmacenIPA\\GuiaMototaxi"
logo_path = "E:\\RobotAlociones\\IPA\\generador_codigo_barras\\LOGO\\LOCINES Logo.png"

def fetch_records():
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Obtener la fecha de hace 4 días
        four_days_ago = datetime.now() - timedelta(days=4)
        formatted_four_days_ago = four_days_ago.strftime('%Y-%m-%d')
        formatted_today = datetime.now().strftime('%Y-%m-%d')

        # Consulta SQL con JOIN
        query = """
            SELECT c.nombre, vc.monto, vc.direccion_envio, vc.telefono, vc.numero_guia, vc.id
            FROM ventas_clientes AS vc
            JOIN clientes AS c ON c.id = vc.id_cliente
            WHERE
                (vc.fecha >= %s OR 
                STR_TO_DATE(vc.fecha, '%d/%m/%Y') >= %s)
                AND vc.mensajero IN ('mototaxi', 'Mototaxi')
                AND EXISTS (
                    SELECT 1
                    FROM mototaxi AS m
                    WHERE m.id_cliente = vc.id
                    AND m.impreso = '0'
                )
        """
        
        cursor.execute(query, (formatted_today, formatted_four_days_ago))
        records = cursor.fetchall()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        return records

    except mysql.connector.Error as err:
        print(f"Error de conexión a la base de datos: {err}")
        return []

def update_impreso(id_cliente):
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Actualizar el estado impreso
        update_query = """
        UPDATE mototaxi
        SET impreso = '1'
        WHERE id_cliente = %s
        """
        cursor.execute(update_query, (id_cliente,))
        connection.commit()  # Realizar el commit de la actualización

        # Cerrar la conexión
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error al actualizar el estado impreso: {err}")

def generate_barcode(guia):
    barcode_image_path = os.path.join(os.getcwd(), guia)  # Guardar en la carpeta actual sin .png
    try:
        code128 = barcode.get('code128', guia, writer=ImageWriter())
        code128.save(barcode_image_path)  # Guardar el archivo PNG (sin .png adicional)
        return barcode_image_path + '.png'  # Devolver la ruta completa incluyendo la extensión
    except Exception as e:
        print(f"Error al generar el código de barras: {e}")
        return None

def wrap_address(address):
    # Función para dividir la dirección en líneas cada 6 palabras
    words = address.split()
    wrapped = []
    for i in range(0, len(words), 6):
        wrapped.append(" ".join(words[i:i+6]))
    return "\n".join(wrapped)

def generate_pdf(record):
    pdf = FPDF()
    pdf.add_page()

    # Agregar logo de la empresa centrado
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=(pdf.w - 30) / 2, y=10, w=21)  # Ajustar tamaño y centrar el logo
    else:
        print(f"No se encontró el logo en la ruta: {logo_path}")

    # Datos del cliente
    pdf.set_font("Arial", size=10)
    
    # Combinar nombre y monto en la misma línea
    pdf.cell(200, 10, f"Nombre: {record['nombre']}    Monto: {record['monto']}", ln=True)
    
    # Saltos de línea más reducidos
    pdf.cell(200, 5, f"Dirección:", ln=True)
    
    # Procesar dirección para agregar saltos de línea cada 6 palabras
    wrapped_address = wrap_address(record['direccion_envio'])
    pdf.multi_cell(0, 5, wrapped_address)  # Usar multi_cell para las direcciones
    
    # Colocar teléfono y "ALociones" en la misma línea
    pdf.cell(200, 5, f"Teléfono: {record['telefono']}    ALociones: 5470-0576", ln=True)
    
    # Ruta del código de barras que se guardará en el directorio donde se ejecuta el script
    barcode_image = os.path.join(os.getcwd(), f"{record['numero_guia']}.png")  # Usar la ruta del directorio actual

    # Verificar si el código de barras existe antes de agregarlo
    if os.path.exists(barcode_image):
        # Cambiar el ancho a 30 mm y mantener la altura en 10 mm
        pdf.image(barcode_image, x=10, y=pdf.get_y() + 10, w=90, h=30)  
    else:
        print(f"No se encontró el código de barras para el número de guía: {record['numero_guia']}")
    
    # Guardar el PDF en la ruta deseada
    pdf_file_path = os.path.join(output_pdf_path, f"{record['numero_guia']}.pdf")
    
    # Verificar si el PDF ya existe y renombrar si es necesario
    if os.path.exists(pdf_file_path):
        base, extension = os.path.splitext(pdf_file_path)
        counter = 1
        while os.path.exists(pdf_file_path):
            pdf_file_path = f"{base}_{counter}{extension}"
            counter += 1
    
    pdf.output(pdf_file_path)
    print(f"PDF generado para {record['nombre']}: {pdf_file_path}")

    # Eliminar el archivo de código de barras PNG
    if os.path.exists(barcode_image):
        os.remove(barcode_image)
        print(f"Eliminado el código de barras: {barcode_image}")
    else:
        print(f"No se encontró el código de barras para eliminar: {barcode_image}")

def main():
    # Obtener los registros
    records = fetch_records()

    if records:  # Solo proceder si hay registros
        for record in records:
            # Generar código de barras
            barcode_image_path = generate_barcode(record['numero_guia'])
            
            # Generar PDF
            generate_pdf(record)
            
            # Actualizar el estado de impreso en la base de datos
            update_impreso(record['id'])  # Usar el ID del registro de ventas_clientes
    else:
        print("No se encontraron registros para generar PDFs.")

if __name__ == "__main__":
    main()
