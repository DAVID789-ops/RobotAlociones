import mysql.connector

# Configuración de la conexión a la base de datos
db_config = {
    'host': '50.87.172.242',
    'user': 'kjycupmy_david',
    'password': 'tF)4l&[;_cV2',
    'database': 'kjycupmy_crm2',
    'port': 3306
}

def connect_to_db():
    """Conecta a la base de datos y devuelve la conexión y el cursor."""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    return connection, cursor

def fetch_devoluciones_temporal(cursor):
    """Obtiene los números de guía de la tabla devoluciones_temporal."""
    cursor.execute("SELECT numero_guia FROM devoluciones_temporal")
    return [row[0] for row in cursor.fetchall()]

def move_records(cursor, guia):
    """Mueve los registros de ventas_clientes a devoluciones si coinciden con el número de guía."""
    # Insertar registro en devoluciones
    insert_query = """
        INSERT INTO devoluciones (id_cliente, monto, fecha, descripcion, tamaño, cantidad,
                                  ganancia, nombres_perfumes, mensajero, precio_envio,
                                  direccion_envio, hecho, entregado, pagado, numero_guia,
                                  telefono, monto_pagado, departamento)
        SELECT id_cliente, monto, fecha, descripcion, tamaño, cantidad,
               ganancia, nombres_perfumes, mensajero, precio_envio,
               direccion_envio, hecho, entregado, pagado, numero_guia,
               telefono, monto_pagado, departamento
        FROM ventas_clientes
        WHERE numero_guia = %s
    """
    cursor.execute(insert_query, (guia,))
    
    # Eliminar registro de ventas_clientes
    delete_query = "DELETE FROM ventas_clientes WHERE numero_guia = %s"
    cursor.execute(delete_query, (guia,))

def main():
    """Función principal que ejecuta el proceso."""
    connection, cursor = connect_to_db()
    
    try:
        # Obtener números de guía de devoluciones_temporal
        guias_devoluciones = fetch_devoluciones_temporal(cursor)
        
        # Procesar cada número de guía
        for guia in guias_devoluciones:
            move_records(cursor, guia)
        
        # Confirmar los cambios en la base de datos
        connection.commit()
        print("Registros movidos exitosamente.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        # Cerrar la conexión
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
