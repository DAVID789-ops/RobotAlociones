import os
import pyexcel as p
import mysql.connector

# Datos de la conexión a la base de datos
DB_HOST = '50.87.172.242'
DB_USER = 'kjycupmy_david'
DB_PASSWORD = 'tF)4l&[;_cV2'
DB_NAME = 'kjycupmy_crm2'

# Conectar a la base de datos
def conectar_db():
    conexion = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conexion

# Función para actualizar la base de datos
def actualizar_bd(numero_guia, monto_pagado):
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Comprobar si el número de guía existe en la tabla ventas_clientes
    # Elimina el sufijo "-1" de los números de guía en la base de datos para hacer la comparación
    query_comprobar = """
    SELECT numero_guia FROM ventas_clientes 
    WHERE REPLACE(numero_guia, '-1', '') = %s
    """
    cursor.execute(query_comprobar, (numero_guia,))
    resultado = cursor.fetchone()

    if resultado:
        # Si existe, actualizar las columnas "pagado", "entregado" y "monto_pagado"
        query_actualizar = """
        UPDATE ventas_clientes
        SET pagado = 1, entregado = 1, monto_pagado = %s
        WHERE REPLACE(numero_guia, '-1', '') = %s
        """
        cursor.execute(query_actualizar, (monto_pagado, numero_guia))
        conexion.commit()
        print(f"Actualizado número de guía {numero_guia} con monto {monto_pagado}.")
    else:
        print(f"Número de guía {numero_guia} no encontrado en la base de datos.")

    cursor.close()
    conexion.close()

# Función para procesar un archivo .xls
def procesar_excel(ruta_archivo):
    hoja = p.get_sheet(file_name=ruta_archivo)
    
    for fila in hoja.row:
        # La columna B (índice 1) tiene los números de guía
        if isinstance(fila[1], str) and fila[1].startswith('FD'):
            numero_guia = fila[1]  # Número de guía en la columna B
            monto_pagado = fila[32]  # Monto pagado en la columna AG
            actualizar_bd(numero_guia, monto_pagado)

# Función para procesar todos los archivos .xls de la carpeta
def procesar_archivos_carpeta(ruta_carpeta):
    for archivo in os.listdir(ruta_carpeta):
        if archivo.endswith('.xls'):
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            print(f"Procesando archivo: {ruta_archivo}")
            procesar_excel(ruta_archivo)

# Ruta de la carpeta donde están los archivos .xls
ruta_carpeta = 'G:\\reportes'

# Procesar todos los archivos en la carpeta
procesar_archivos_carpeta(ruta_carpeta)
