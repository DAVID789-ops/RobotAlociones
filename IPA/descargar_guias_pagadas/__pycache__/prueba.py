import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',  # Cambia esto si tu servidor de base de datos está en otro lugar
            user='tu_usuario',
            password='tu_contraseña',
            database='tu_base_de_datos'
        )
        if conn.is_connected():
            print("Conexión exitosa a la base de datos")
            conn.close()
        else:
            print("No se pudo conectar a la base de datos")
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")

if __name__ == "__main__":
    test_connection()
