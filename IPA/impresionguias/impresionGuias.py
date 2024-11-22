import os
import win32print
import win32api
import shutil

def listar_archivos(carpeta):
    """Lista todos los archivos PDF en la carpeta dada."""
    return [f for f in os.listdir(carpeta) if f.endswith('.pdf')]

def imprimir_archivo(archivo):
    """Imprime el archivo PDF utilizando Adobe Acrobat Reader."""
    # Ruta al ejecutable de Adobe Acrobat Reader
    acrobat_path = r'C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe'

    if os.path.exists(acrobat_path):
        win32api.ShellExecute(
            0,
            "open",
            acrobat_path,
            f'/t "{archivo}" "Canon E400 series Printer"',
            None,
            0
        )
    else:
        print("No se encontró Adobe Acrobat Reader en la ruta especificada.")

def copiar_archivos(carpeta_origen, carpeta_destino):
    """Copia los archivos de la carpeta de origen a la carpeta de destino."""
    archivos = listar_archivos(carpeta_origen)

    for archivo in archivos:
        archivo_completo = os.path.join(carpeta_origen, archivo)
        destino_completo = os.path.join(carpeta_destino, archivo)
        shutil.copy(archivo_completo, destino_completo)  # Copia el archivo
        print(f"Copiando: {archivo_completo} a {destino_completo}")

def imprimir_informes(carpeta_informes, carpeta_antigua):
    """Imprime todos los archivos PDF en la carpeta especificada y luego los copia."""
    archivos = listar_archivos(carpeta_informes)
    
    if archivos:
        print(f"Imprimiendo {len(archivos)} archivos en la impresora Canon E400 series Printer...")
        for archivo in archivos:
            archivo_completo = os.path.join(carpeta_informes, archivo)
            print(f"Imprimiendo: {archivo_completo}")
            imprimir_archivo(archivo_completo)

        # Copiar archivos a la carpeta antigua después de imprimir
        copiar_archivos(carpeta_informes, carpeta_antigua)
    else:
        print("No se encontraron archivos PDF en la carpeta.")

if __name__ == '__main__':
    carpeta_informes = r'E:\RobotAlociones\AlmacenIPA\GuiaMototaxi'
    carpeta_antigua = r'E:\RobotAlociones\AlmacenIPA\guiasMototaxiAntiguo'
    
    imprimir_informes(carpeta_informes, carpeta_antigua)
