import mysql.connector
from mysql.connector import Error

def abrir_base():
    host = "localhost"
    user = "root"
    password = "Franco4567"
    database = "ByteZero"
    port = 3306

    try:
        # Conectar a la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

