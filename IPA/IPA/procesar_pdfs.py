import os
import mysql.connector
from extraer_datos import extraer_datos_pdf

# Configuración de la base de datos
conn = mysql.connector.connect(
    host='50.87.172.242',
    user='kjycupmy_david',
    password='tF)4l&[;_cV2',
    database='kjycupmy_crm2',
    port=3306
)
cursor = conn.cursor()

# Directorio de PDFs
DIRECTORIO_PDFS = r'F:\IPA GESTION CLIENTES'

# Función para insertar datos en la base de datos
def insertar_en_base_datos(datos):
    # Verificar si ya existe una entrada con el mismo número de guía y fecha
    cursor.execute("SELECT * FROM ventas_clientes WHERE numero_guia = %s AND fecha = %s", (datos['numero_guia'], datos['fecha']))
    resultado = cursor.fetchone()

    if resultado:
        print(f"Registro con Guía No. {datos['numero_guia']} ya existe en la base de datos. No se procesará.")
        return

    # Insertar los datos en la tabla 'clientes'
    cursor.execute("""
        INSERT INTO clientes (nombre, departamento, direccion, telefono, fecha_registro)
        VALUES (%s, %s, %s, %s, %s)
    """, (datos['contacto'], datos['departamento'], datos['direccion'], datos['telefono'], datos['fecha']))
    conn.commit()
    
    id_cliente = cursor.lastrowid

    # Insertar los datos en la tabla 'ventas_clientes'
    cursor.execute("""
        INSERT INTO ventas_clientes (id_cliente, ganancia, monto, fecha, precio_envio, tamaño, descripcion, cantidad, mensajero, numero_guia, telefono, direccion_envio, municipio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (id_cliente, datos['ganancia'], datos['monto'], datos['fecha'], datos['precio_envio'], datos['tamaño'], datos['descripcion'], datos['cantidad'], datos['mensajero'], datos['numero_guia'], datos['telefono'], datos['direccion'], datos['municipio']))
    conn.commit()

    print(f"Datos del cliente {datos['contacto']} insertados correctamente.")

# Procesar todos los archivos PDF en el directorio
def procesar_pdfs():
    for archivo in os.listdir(DIRECTORIO_PDFS):
        if archivo.endswith(".pdf"):
            ruta_pdf = os.path.join(DIRECTORIO_PDFS, archivo)
            print(f"Procesando {ruta_pdf}...")
            datos_list = extraer_datos_pdf(ruta_pdf)
            for datos in datos_list:
                if datos:
                    insertar_en_base_datos(datos)
                else:
                    print(f"No se pudo extraer datos de {ruta_pdf}")

# Ejecutar el procesamiento
if __name__ == "__main__":
    procesar_pdfs()
    cursor.close()
    conn.close()
