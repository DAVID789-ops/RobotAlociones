import os
import shutil
import mysql.connector
import openpyxl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Configuración de la base de datos
conn = mysql.connector.connect(
    host='50.87.172.242',
    user='kjycupmy_david',
    password='tF)4l&[;_cV2',
    database='kjycupmy_crm2',
    port=3306
)
cursor = conn.cursor()

# Configuración del correo
email_remitente = 'alociones@gmail.com'
email_receptor = 'alociones@gmail.com'
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'alociones@gmail.com'
smtp_password = 'oemg qonh vqra kcuo'

# Rutas de directorio
directorio_entrada = 'G:/reportes'
directorio_ejecutado = 'G:/ejecutado'

# Obtener todos los archivos .xlsx en el directorio de entrada
archivos_xlsx = [f for f in os.listdir(directorio_entrada) if f.endswith('.xlsx')]

# Procesar cada archivo .xlsx
errores_totales = []
for archivo in archivos_xlsx:
    ruta_archivo = os.path.join(directorio_entrada, archivo)
    
    # Procesar el archivo Excel
    try:
        libro = openpyxl.load_workbook(ruta_archivo)
        pestaña = libro["GT_EnvioaclientesCODLiquidacion"]

        # Extraer números de guía, asegurándose de que no haya valores None
        numeros_guia = [pestaña.cell(row=i, column=2).value for i in range(11, 20)]
        numeros_guia = [guia for guia in numeros_guia if guia is not None]

        # Procesar y actualizar la base de datos
        errores = []
        for numero_guia in numeros_guia:
            cursor.execute("SELECT numero_guia FROM ventas_clientes WHERE numero_guia = %s", (numero_guia,))
            resultado = cursor.fetchone()

            if resultado:
                cursor.execute("UPDATE ventas_clientes SET pagado = 1 WHERE numero_guia = %s", (numero_guia,))
            else:
                errores.append(numero_guia)

        conn.commit()

        # Registrar errores totales
        errores_totales.extend(errores)
        
    except Exception as e:
        errores_totales.append(f"Error al procesar el archivo {archivo}: {str(e)}")
    finally:
        # Intentar mover el archivo después de un pequeño retraso
        time.sleep(2)  # Retraso para asegurar que el archivo se libere

        # Mover archivo a la carpeta de ejecutado
        destino_archivo = os.path.join(directorio_ejecutado, archivo)
        try:
            shutil.move(ruta_archivo, destino_archivo)
        except Exception as e:
            errores_totales.append(f"Error al mover el archivo {archivo}: {str(e)}")

# Enviar correo con resumen de errores
msg = MIMEMultipart()
msg['From'] = email_remitente
msg['To'] = email_receptor
msg['Subject'] = 'Estado del Proceso de Actualización de Guías'

cuerpo = "El proceso de actualización se completó exitosamente para todos los archivos.\n\n"
if errores_totales:
    cuerpo += "Errores encontrados:\n"
    # Asegurarse de que todos los elementos en errores_totales sean cadenas
    errores_totales = [str(error) if error is not None else "Error desconocido" for error in errores_totales]
    cuerpo += "\n".join(errores_totales)
else:
    cuerpo += "Todas las guías se actualizaron correctamente."

msg.attach(MIMEText(cuerpo, 'plain'))

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(email_remitente, email_receptor, msg.as_string())
    print("Correo enviado con éxito.")
except Exception as e:
    print(f"Error al enviar el correo: {e}")

# Cerrar conexión
cursor.close()
conn.close()
