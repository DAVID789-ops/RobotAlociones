import imaplib
import email
from email.header import decode_header
import os

# Configuración del correo
EMAIL_USER = "alociones@gmail.com"
EMAIL_PASS = "oemg qonh vqra kcuo"
IMAP_SERVER = "imap.gmail.com"

# Carpeta donde se guardarán los archivos adjuntos
DOWNLOAD_FOLDER = "G:/reportes"

# Crear la carpeta si no existe
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Función para conectar al correo
def conectar_correo():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    return mail

# Función para renombrar archivos duplicados
def renombrar_si_existe(filepath):
    base, extension = os.path.splitext(filepath)
    contador = 1

    # Renombrar si el archivo ya existe
    while os.path.exists(filepath):
        filepath = f"{base}_{contador}{extension}"
        contador += 1

    return filepath

# Función para descargar los adjuntos
def descargar_adjuntos():
    mail = conectar_correo()
    mail.select("inbox")

    # Buscar correos no leídos con archivos adjuntos
    status, messages = mail.search(None, 'UNSEEN')
    
    # Obtener los IDs de los mensajes
    email_ids = messages[0].split()

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = decode_header(msg["subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()

                print(f"Procesando correo con asunto: {subject}")

                # Iterar sobre cada parte del mensaje
                for part in msg.walk():
                    if part.get_content_disposition() == "attachment":
                        filename = part.get_filename()

                        if filename:
                            filepath = os.path.join(DOWNLOAD_FOLDER, filename)

                            # Renombrar archivo si ya existe
                            filepath = renombrar_si_existe(filepath)

                            # Descargar el archivo
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            print(f"Archivo descargado: {filepath}")

    # Cerrar la conexión
    mail.close()
    mail.logout()

if __name__ == "__main__":
    descargar_adjuntos()
