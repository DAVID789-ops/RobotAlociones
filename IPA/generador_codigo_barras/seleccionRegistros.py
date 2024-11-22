import mysql.connector
from datetime import datetime, timedelta

# Credenciales de la base de datos
db_config = {
    'host': '50.87.172.242',
    'user': 'kjycupmy_david',
    'password': 'tF)4l&[;_cV2',
    'database': 'kjycupmy_crm2',
    'port': 3306
}

# Conectar a la base de datos
def connect_to_database():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Formatear fecha
def format_date(date_str):
    # Intenta convertir desde el formato 'YYYY-MM-DD HH:MM:SS'
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        # Si falla, intenta el formato 'DD/MM/YYYY'
        return datetime.strptime(date_str, '%d/%m/%Y')

# Obtener las filas que cumplan con las condiciones
def fetch_records():
    conn = connect_to_database()
    if conn is None:
        return

    cursor = conn.cursor()
    
    # Calcular la fecha de hace 4 días
    four_days_ago = datetime.now() - timedelta(days=4)
    
    # Consulta SQL
    query = """
    SELECT id, mensajero, numero_guia 
    FROM ventas_clientes 
    WHERE fecha BETWEEN %s AND NOW() 
    AND mensajero = 'Mototaxi'
    AND numero_guia IS NULL
    """

    # Ejecutar la consulta
    cursor.execute(query, (four_days_ago.strftime('%Y-%m-%d 00:00:00'),))
    
    records = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return records

# Generar código de barras
def generate_barcode_id(id):
    return f"AD{id:08d}"  # Formato AD00000001

# Insertar en mototaxi y actualizar numero_guia
def insert_into_mototaxi_and_update_guia(id_cliente):
    conn = connect_to_database()
    if conn is None:
        return

    cursor = conn.cursor()
    
    # Generar el código de barras
    barcode_id = generate_barcode_id(id_cliente)
    
    # Insertar el nuevo registro en mototaxi
    insert_query = "INSERT INTO mototaxi (codigo_barras, id_cliente) VALUES (%s, %s)"
    cursor.execute(insert_query, (barcode_id, id_cliente))

    # Actualizar el numero_guia en ventas_clientes
    update_query = "UPDATE ventas_clientes SET numero_guia = %s WHERE id = %s"
    cursor.execute(update_query, (barcode_id, id_cliente))

    conn.commit()
    
    cursor.close()
    conn.close()

# Main
if __name__ == "__main__":
    records = fetch_records()
    
    if records:
        for record in records:
            id_cliente = record[0]  # Asumiendo que el ID del cliente es el primero
            print(f"Generando código de barras y actualizando número de guía para ID cliente: {id_cliente}")
            insert_into_mototaxi_and_update_guia(id_cliente)
    else:
        print("No hay registros que procesar.")
