import os
import pandas as pd
import mysql.connector

# Configuración de MySQL
DB_HOST = '50.87.172.242'
DB_USER = 'kjycupmy_david'
DB_PASSWORD = 'tF)4l&[;_cV2'
DB_NAME = 'kjycupmy_crm2'

# Configuración de la carpeta donde se guardan los archivos
DOWNLOAD_FOLDER = 'G:/reportes'

# Conectar a la base de datos MySQL
def conectar_mysql():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

# Procesar archivos y extraer datos
def procesar_archivos():
    # Conectar a la base de datos
    conn = conectar_mysql()
    if conn is None:
        return

    cursor = conn.cursor()

    # Listar archivos en la carpeta
    for archivo in os.listdir(DOWNLOAD_FOLDER):
        if archivo.endswith('.xls'):
            filepath = os.path.join(DOWNLOAD_FOLDER, archivo)
            print(f"Procesando archivo: {archivo}")

            # Leer archivo Excel
            try:
                df = pd.read_excel(filepath)

                # Asumiendo que 'C' es la columna 'GUIA' y 'H' es 'MONTO LIQUIDADO'
                if 'B' in df.columns and 'AG' in df.columns:
                    for index, row in df.iterrows():
                        guia = row['B']  # Ajustar al nombre de columna correcto
                        monto_liquidado = row['AG']  # Ajustar al nombre de columna correcto

                        # Insertar los datos en MySQL
                        query = "INSERT INTO guias (guia, monto_liquidado) VALUES (%s, %s)"
                        cursor.execute(query, (guia, monto_liquidado))
                        conn.commit()

                    print(f"Datos del archivo {archivo} insertados correctamente.")
                else:
                    print(f"Las columnas 'GUIA' o 'MONTO LIQUIDADO' no se encontraron en el archivo {archivo}.")
            except Exception as e:
                print(f"Error al procesar el archivo {archivo}: {e}")

    # Cerrar conexión a la base de datos
    cursor.close()
    conn.close()

if __name__ == "__main__":
    procesar_archivos()
