import pandas as pd
import mysql.connector
from config import get_database_connection
import os

def process_excel_file(file_path, conn):
    print(f"Procesando archivo: {file_path}")
    
    try:
        # Leer el archivo Excel
        df = pd.read_excel(file_path, header=None)
    except PermissionError:
        print(f"Permiso denegado para el archivo: {file_path}")
        return
    
    # Mostrar las primeras filas para revisar el contenido
    print(df.head(10))  
    
    # Encontrar la fila que contiene "ENVIO LIQUIDACION CLIENTE"
    header_row = df[df.iloc[:, 3].str.contains('ENVIO LIQUIDACION CLIENTE', na=False)].index
    if not header_row.empty:
        header_row = header_row[0]
        print(f"Encabezado encontrado en la fila: {header_row}")
        df.columns = df.iloc[header_row]
        df = df[header_row + 1:]
    else:
        print("No se encontró la fila de encabezado esperada.")
        return
    
    df.reset_index(drop=True, inplace=True)
    print(df.head(10))  # Mostrar las primeras filas después de ajustar el encabezado
    
    # Recorrer las filas del archivo
    for index, row in df.iterrows():
        try:
            # Evitar filas vacías o que no contengan datos válidos
            guia = str(row[df.columns[2]]).strip()  # Ajustar el índice si es necesario
            monto_str = str(row[df.columns[14]]).strip()  # Ajustar la columna del monto
            print(f"Procesando fila {index}: Guía = {guia}, Monto = {monto_str}")

            # Intentar convertir el monto a float, saltar la fila si no es posible
            try:
                monto = float(monto_str.replace(',', '').replace('$', ''))  # Limpiar posibles símbolos como $ o comas
                print(f"Número de guía: {guia}, Monto: {monto}")
                
                # Comparar con la base de datos
                cursor = conn.cursor()
                query = """
                    SELECT id FROM ventas1
                    WHERE guia = %s AND monto = %s
                """
                cursor.execute(query, (guia, monto))
                result = cursor.fetchone()
                if result:
                    print(f"Se encontró coincidencia en la base de datos para la guía {guia} con monto {monto}.")
                else:
                    print(f"No se encontró coincidencia en la base de datos para la guía {guia} con monto {monto}.")
                cursor.close()

            except ValueError:
                print(f"Valor de monto no válido en la fila {index}: {monto_str}, saltando fila.")
                continue

        except KeyError as e:
            print(f"Error: Columna {e} no encontrada en el archivo {file_path}. Verifica la estructura del archivo.")
            break

def process_all_excels():
    # Obtener conexión a la base de datos
    conn = get_database_connection()

    # Ruta donde están los archivos Excel
    directory = r'G:\reportes'

    # Procesar todos los archivos Excel en el directorio
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx") and not filename.startswith("~$"):
            file_path = os.path.join(directory, filename)
            process_excel_file(file_path, conn)
    
    # Cerrar la conexión a la base de datos
    conn.close()

if __name__ == "__main__":
    process_all_excels()
