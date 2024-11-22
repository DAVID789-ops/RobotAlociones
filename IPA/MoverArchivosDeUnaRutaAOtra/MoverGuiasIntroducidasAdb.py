import shutil
import os

# Ruta de origen y destino
ruta_origen = r"F:\IPA GESTION CLIENTES"
ruta_destino = r"E:\RobotAlociones\AlmacenIPA\GuiasProcesadas"

# Verificar si la ruta destino existe, si no, crearla
if not os.path.exists(ruta_destino):
    os.makedirs(ruta_destino)

# Listar los archivos en la carpeta de origen
archivos = os.listdir(ruta_origen)

# Mover los archivos de origen a destino
for archivo in archivos:
    archivo_origen = os.path.join(ruta_origen, archivo)
    archivo_destino = os.path.join(ruta_destino, archivo)

    # Verificar que sea un archivo y no una carpeta
    if os.path.isfile(archivo_origen):
        # Mover el archivo
        shutil.move(archivo_origen, archivo_destino)
        print(f"Archivo {archivo} movido a {ruta_destino}")

print("Todos los archivos han sido movidos.")
