import os
import win32print
import win32api

def listar_archivos(carpeta):
    """Lista todos los archivos PDF en la carpeta dada."""
    archivos = [f for f in os.listdir(carpeta) if f.endswith('.pdf')]
    return archivos

def imprimir_archivo(archivo):
    """Imprime el archivo PDF utilizando Adobe Acrobat Reader."""
    # Ruta al ejecutable de Adobe Acrobat Reader
    acrobat_path = r'C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe'

    if os.path.exists(acrobat_path):
        # Enviar el archivo a la impresora utilizando Adobe Acrobat Reader
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

def imprimir_informes(carpeta):
    """Imprime todos los archivos PDF en la carpeta especificada utilizando Adobe Acrobat Reader."""
    archivos = listar_archivos(carpeta)
    
    if archivos:
        print(f"Imprimiendo {len(archivos)} archivos en la impresora Canon E400 series Printer...")
        for archivo in archivos:
            archivo_completo = os.path.join(carpeta, archivo)
            print(f"Imprimiendo: {archivo_completo}")
            imprimir_archivo(archivo_completo)
    else:
        print("No se encontraron archivos PDF en la carpeta.")

if __name__ == '__main__':
    carpeta_informes = r'E:\RobotAlociones\AlmacenIPA\Informes'
    
    imprimir_informes(carpeta_informes)
