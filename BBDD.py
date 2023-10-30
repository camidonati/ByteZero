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
    
def crear_base_de_datos_si_no_existe():
    try:
        # Conectarse al servidor de MySQL (asegúrate de proporcionar los valores correctos)
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Franco4567"
        )

        # Crear un objeto cursor para ejecutar comandos SQL
        cursor = conexion.cursor()

        # Nombre de la base de datos que deseas crear
        database_name = "ByteZero"

        # Verificar si la base de datos ya existe
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor]

        if database_name not in databases:
            # La base de datos no existe, así que la creamos
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Base de datos '{database_name}' creada con éxito.")
        else:
            print(f"La base de datos '{database_name}' ya existe.")
            
         # Seleccionar la base de datos
        cursor.execute(f"USE {database_name}")

        # Verificar si la tabla de usuarios ya existe
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor]

        if "usuarios" not in tables:
            # La tabla de usuarios no existe, así que la creamos
            create_table_query = """
            CREATE TABLE usuarios (
                id INT AUTO_INCREMENT,
                usuario VARCHAR(50) NOT NULL,
                contraseña VARCHAR(100) NOT NULL,
                nombre VARCHAR(50) NOT NULL,
                apellido VARCHAR(50) NOT NULL,
                PRIMARY KEY (id)
            )
            """
            cursor.execute(create_table_query)
            print("Tabla 'usuarios' creada con éxito.")
        else:
            print("La tabla 'usuarios' ya existe.")

        # Cerrar la conexión a MySQL
        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        print(f"Error: {error}")

