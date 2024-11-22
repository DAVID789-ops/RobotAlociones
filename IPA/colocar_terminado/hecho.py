import mysql.connector

# Configuración de la conexión a la base de datos
db_config = {
    'host': '50.87.172.242',
    'user': 'kjycupmy_david',
    'password': 'tF)4l&[;_cV2',
    'database': 'kjycupmy_crm2',
    'port': 3306
}

# Conectarse a la base de datos
try:
    connection = mysql.connector.connect(**db_config)
    
    # Cursor con buffering para asegurar que los resultados se lean completamente
    cursor = connection.cursor(buffered=True)

    # Consulta para obtener los valores de 'numero_guia' de la tabla 'terminado'
    cursor.execute("SELECT numero_guia FROM terminado")
    guias_terminado = cursor.fetchall()

    # Iterar por los números de guía obtenidos de 'terminado'
    for (numero_guia,) in guias_terminado:
        # Comprobar si el 'numero_guia' está en 'ventas_clientes'
        cursor.execute("SELECT numero_guia FROM ventas_clientes WHERE numero_guia = %s", (numero_guia,))
        
        # Leer el resultado antes de continuar
        resultado = cursor.fetchone()
        
        if resultado:
            # Si hay coincidencia, actualizar la columna 'hecho' a 1 en 'ventas_clientes'
            cursor.execute("UPDATE ventas_clientes SET hecho = 1 WHERE numero_guia = %s", (numero_guia,))
    
    # Confirmar cambios
    connection.commit()

    print("Actualización completada con éxito.")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión cerrada.")
