import mysql.connector

# Configuración de la conexión a la base de datos
db_config = {
    'host': '50.87.172.242',
    'user': 'kjycupmy_david',
    'password': 'tF)4l&[;_cV2',
    'database': 'kjycupmy_crm2',
    'port': 3306
}

try:
    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Buscar coincidencias en las tablas eliminar y ventas_clientes
    select_query = """
    SELECT vc.*
    FROM ventas_clientes vc
    JOIN eliminar e ON vc.numero_guia = e.numero_guia
    """
    cursor.execute(select_query)
    coincidencias = cursor.fetchall()

    if coincidencias:
        # Transferir las coincidencias a la tabla pedidos_retenidos
        insert_query = """
        INSERT INTO pedidos_retenidos (
            id_cliente, monto, fecha, descripcion, tamaño, cantidad, ganancia,
            nombres_perfumes, mensajero, precio_envio, direccion_envio, hecho,
            entregado, pagado, numero_guia, telefono, monto_pagado, departamento
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        for fila in coincidencias:
            # Insertar el registro en pedidos_retenidos
            cursor.execute(insert_query, (
                fila[1],  # id_cliente
                fila[2],  # monto
                fila[3],  # fecha
                fila[4],  # descripcion
                fila[5],  # tamaño
                fila[6],  # cantidad
                fila[7],  # ganancia
                fila[8],  # nombres_perfumes
                fila[9],  # mensajero
                fila[10],  # precio_envio
                fila[11],  # direccion_envio
                fila[12],  # hecho
                fila[13],  # entregado
                fila[14],  # pagado
                fila[15],  # numero_guia
                fila[16],  # telefono
                fila[17],  # monto_pagado
                fila[18]   # departamento
            ))

            # Eliminar el registro de ventas_clientes después de insertarlo en pedidos_retenidos
            delete_query = """
            DELETE FROM ventas_clientes WHERE numero_guia = %s
            """
            cursor.execute(delete_query, (fila[15],))  # fila[15] es numero_guia

        conn.commit()
        print("Coincidencias transferidas y eliminadas de 'ventas_clientes'.")
    else:
        print("No se encontraron coincidencias.")

except mysql.connector.Error as e:
    print(f"Error al conectar a la base de datos: {e}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexión a la base de datos cerrada.")
