import os
import requests
from bs4 import BeautifulSoup
import csv
import mysql.connector

# Definir la ruta completa donde deseas guardar el archivo CSV
ruta_completa = os.path.dirname(os.path.realpath(__file__))

# URL de la página
url = 'https://datosmacro.expansion.com/demografia/migracion/inmigracion/argentina'

# Realizar la solicitud GET
response = requests.get(url)

# Parsear el contenido HTML con BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar la tabla por su clase
table = soup.find('table', class_='tabledat')

# Verificar si la tabla se ha encontrado
if table:
    # Inicializar listas para almacenar los datos
    years = []
    inmigration_men = []
    inmigration_women = []
    total_inmigration = []

    # Encontrar todas las filas de datos en la tabla
    rows = table.find_all('tr')

    # Iterar a través de las filas, comenzando desde la segunda fila (índice 1) para omitir el encabezado
    for row in rows[1:]:
        # Encontrar todas las columnas de datos en la fila
        columns = row.find_all('td')

        # Extraer los datos y almacenarlos en las listas correspondientes
        year = columns[0].text.strip()
        men = columns[1].text.strip().replace('.', '')
        women = columns[2].text.strip().replace('.', '')
        total = columns[3].text.strip().replace('.', '')

        years.append(year)
        inmigration_men.append(men)
        inmigration_women.append(women)
        total_inmigration.append(total)

    # Crear archivo CSV 
    csv_filename = os.path.join(ruta_completa, 'argentina_inmigrantes_totales_tabla1.csv')
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Year', 'Inmigration Men', 'Inmigration Women', 'Total Inmigration']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(years)):
            writer.writerow({
                'Year': years[i],
                'Inmigration Men': inmigration_men[i],
                'Inmigration Women': inmigration_women[i],
                'Total Inmigration': total_inmigration[i],
            })
else:
    print("La tabla no se encontró en la página.")

print("Datos extraídos y guardados en el archivo CSV en la ubicación especificada:", csv_filename)

# Creación de la conexión con el servidor
try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='root'
    )

    if connection.is_connected():
        print("Conexión exitosa")

    # Crear o eliminar la base de datos según tus necesidades
    cursor = connection.cursor()
    delete_database_query = "DROP DATABASE IF EXISTS inmigra"
    cursor.execute(delete_database_query)
    create_database_query = "CREATE DATABASE inmigra"
    cursor.execute(create_database_query)
    cursor.close()

    # Reconectar a la nueva base de datos
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='root',
        database='inmigra'
    )
    if connection.is_connected():
        print("Conexión a la base de datos Inmigracion correcta")

except Exception as ex:
    print(ex)

# Creación del cursor para recorrer la base
cursor = connection.cursor()

# Crear una tabla si no existe
create_table_query = """
CREATE TABLE IF NOT EXISTS inmigracion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    inmigration_men INT,
    inmigration_women INT,
    total_inmigration INT
)
"""
cursor.execute(create_table_query)

# Insertar datos en la tabla
insert_query = """
INSERT INTO inmigracion (year, inmigration_men, inmigration_women, total_inmigration)
VALUES (%s, %s, %s, %s)
"""

for i in range(len(years)):
    data = (
        years[i],
        int(inmigration_men[i]),
        int(inmigration_women[i]),
        int(total_inmigration[i]),
    )
    cursor.execute(insert_query, data)

# Commit los cambios
connection.commit()
print("Datos insertados en la base de datos SQL.")
cursor.execute("SELECT * FROM inmigracion")
res = cursor.fetchall()

# Realiza una consulta SQL
query = "SELECT id, year, inmigration_men, inmigration_women, total_inmigration FROM inmigracion"
cursor.execute(query)

# Resultados de la consulta
res = cursor.fetchall()

# Encabezados de la tabla
def printo():
    print("{:<5} {:<8} {:<25} {:<25} {:<25}".format("Id", "Año", "Inmigración Hombres", "Inmigración Mujeres", "Total Inmigración"))
    print("-" * 90)
    print("-" * 90)

# Imprime tabla con formato desde la base
    for row in res:
        id, year, men, women, total = row
        print("{:<5} {:<8} {:<25} {:<25} {:<25}".format(id, year, men, women, total))


    print("-" * 90)
    print("-" * 90)

print(" ")


#Realizar consulta / agregar/ modificacion / borrado por consola con menu
def opciones():
    print("Menú:")
    print("1. Consultar registro por Id")
    print("2. Agregar registro a la base")
    print("3. Modificar registro por Id")
    print("4. Eliminar registro por Id")
    print("5. Imprmir base de datos actualizada")
    print("6. Salir")

# Menu de seleccion
while True:
    opciones()
    opcion = input("Elige una opción (1/ 2/ 3/ 4/ 5/ 6): ")

    if opcion == "1":
        # Consulta registro por ID
        consulta_id = int(input("Ingresa el ID del registro que deseas consultar: "))
        cursor.execute("SELECT * FROM inmigracion WHERE id = %s", (consulta_id,))
        res = cursor.fetchone()
        
        if res:
            print("\nRegistro encontrado:")
            print("{:<5} {:<8} {:<25} {:<25} {:<25}".format("Id", "Año", "Inmigración Hombres", "Inmigración Mujeres", "Total Inmigración"))
            print("-" * 90)
            id, year, men, women, total = res
            print("{:<5} {:<8} {:<25} {:<25} {:<25}".format(id, year, men, women, total))
            print("-" * 90)
        else:
            print(f"No se encontró ningún registro con ID {consulta_id}")

    elif opcion == "2":
        # Agrega registro por ID        
        anio_nuevo = int(input("Ingresa el nuevo año: "))
        inmigra_h = int(input("Ingresa la cantidad inmigratoria de hombres: "))
        inmigra_w = int(input("Ingresa la cantidad inmigratoria de mujeres: "))

        insert_query = """
             INSERT INTO inmigracion (year, inmigration_men, inmigration_women, total_inmigration)
            VALUES (%s, %s, %s, %s)
         """
        # Calcular el valor de total_inmigration
        total_inmigration = inmigra_h + inmigra_w

        data = (
        
            anio_nuevo,
            inmigra_h,
            inmigra_w,
            total_inmigration,
        )

        try:
            cursor.execute(insert_query, data)
            connection.commit()
            res = cursor.fetchall()
            print("Registro agregado correctamente.")
        except Exception as ex:
            print("Error al agregar el registro:", ex)

     

    elif opcion == "3":
        # Modifica registro por ID
        id_a_modificar = int(input("Ingresa el ID del registro que deseas modificar: "))
        anio_nuevo = input("Ingresa el nuevo año: ")
        inmigra_h = int(input("Ingresa la nueva cantidad inmigratoria de hombres: "))
        inmigra_w = int(input("Ingresa la nueva cantidad inmigratoria de mujeres: "))
        # Calcular el valor de total_inmigration
        total_inmigration = inmigra_h + inmigra_w

        data = (
        
            anio_nuevo,
            inmigra_h,
            inmigra_w,
            total_inmigration,
        )
        cursor.execute("UPDATE inmigracion SET year = %s, inmigration_men = %s, inmigration_women = %s, total_inmigration = %s WHERE id = %s", (anio_nuevo, inmigra_h, inmigra_w, total_inmigration, id_a_modificar))
        cursor.fetchone()
        connection.commit()   

       
        print("Registro modificado correctamente.")

    elif opcion == "4":
        # Eliminar registro por ID
        id_a_eliminar = int(input("Ingresa el ID del registro que deseas eliminar: "))
        cursor.execute("DELETE FROM inmigracion WHERE id = %s", (id_a_eliminar,))
        connection.commit()
        print("Registro eliminado correctamente.")

    elif opcion == "5":
       # Imprimir toda la base de datos ACTUALIZADA.
        cursor.execute(query)
        res = cursor.fetchall()
        printo()


    elif opcion == "6":
        # Salir
        print("Saliendo...... ")
        print("Gracias por participar, hasta pronto! ")
        break

    else:
        print("Opción no válida. Por favor, elige 1, 2, 3, 4, 5 o 6.")

    continuar = input("¿Quieres continuar? (s/n): ")
    if continuar.lower() != "s":
        break

# Cierra la conexión
connection.close()
print("Conexión a la base cerrada")
