import os
import requests
from bs4 import BeautifulSoup
import csv
import mysql.connector

# Definir la ruta completa donde deseas guardar el archivo CSV
ruta_completa = r'C:\Users\delfe\Desktop\BSoup\scrap'

# URL de la página
url = 'https://datosmacro.expansion.com/demografia/migracion/emigracion/argentina'

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
    emigration_men = []
    emigration_women = []
    total_emigration = []

    # Encontrar todas las filas de datos en la tabla
    rows = table.find_all('tr')

    # Iterar a través de las filas, comenzando desde la segunda fila (índice 1) para omitir el encabezado
    for row in rows[1:]:
        # Encontrar todas las columnas de datos en la fila
        columns = row.find_all('td')

        # Extraer los datos y almacenarlos
        year = columns[0].text.strip()
        men = columns[1].text.strip().replace('.', '')
        women = columns[2].text.strip().replace('.', '')
        total = columns[3].text.strip().replace('.', '')

        years.append(year)
        emigration_men.append(men)
        emigration_women.append(women)
        total_emigration.append(total)

    # Archivo CSV
    csv_filename = os.path.join(ruta_completa, 'argentina_emigrantes_totales_tabla1.csv')
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Year', 'Emigration Men', 'Emigration Women', 'Total Emigration']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(years)):
            writer.writerow({
                'Year': years[i],
                'Emigration Men': emigration_men[i],
                'Emigration Women': emigration_women[i],
                'Total Emigration': total_emigration[i],
            })
else:
    print("La tabla no se encontró en la página.")

print("Datos extraídos y guardados en el archivo CSV en la ubicación especificada:", csv_filename)

# Conexión con el servidor
try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='root'
    )

    if connection.is_connected():
        print("Conexión exitosa")

    # Crear y eliminar la base de datos
    cursor = connection.cursor()
    delete_database_query = "DROP DATABASE IF EXISTS emigra"
    cursor.execute(delete_database_query)
    create_database_query = "CREATE DATABASE emigra"
    cursor.execute(create_database_query)
    cursor.close()

    # Reconectar a la nueva base de datos
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='root',
        database='emigra'
    )
    if connection.is_connected():
        print("Conexión a la base de datos Emigracion correcta")

except Exception as ex:
    print(ex)

# Cursor para recorrer la base
cursor = connection.cursor()

# Crear tabla si no existe
create_table_query = """
CREATE TABLE IF NOT EXISTS emigracion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    emigration_men INT,
    emigration_women INT,
    total_emigration INT
)
"""
cursor.execute(create_table_query)

# Insertar datos en la tabla
insert_query = """
INSERT INTO emigracion (year, emigration_men, emigration_women, total_emigration)
VALUES (%s, %s, %s, %s)
"""

for i in range(len(years)):
    data = (
        years[i],
        int(emigration_men[i]),
        int(emigration_women[i]),
        int(total_emigration[i]),
    )
    cursor.execute(insert_query, data)

# Commit los cambios
connection.commit()
print("Datos insertados en la base de datos SQL.")
cursor.execute("SELECT * FROM emigracion")
result1 = cursor.fetchall()


# Realiza una consulta SQL
query = "SELECT id, year, emigration_men, emigration_women, total_emigration FROM emigracion"
cursor.execute(query)

# Resultados de la consulta
results = cursor.fetchall()

# Encabezados de la tabla
def printo():
    print("{:<5} {:<8} {:<25} {:<25} {:<25}".format("Id", "Año", "Emigración Hombres", "Emigración Mujeres", "Total Emigración"))
    print("-" * 90)
    print("-" * 90)

# Imprime tabla con formato desde la base
    for row in results:
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
        id_a_consultar = int(input("Ingresa el ID del registro que deseas consultar: "))
        cursor.execute("SELECT * FROM emigracion WHERE id = %s", (id_a_consultar,))
        res = cursor.fetchone()

        if res:
            print("\nRegistro encontrado:")
            print("{:<5} {:<8} {:<25} {:<25} {:<25}".format("Id", "Año", "Emigración Hombres", "Emigración Mujeres", "Total Emigración"))
            print("-" * 90)
            id, year, men, women, total = res
            print("{:<5} {:<8} {:<25} {:<25} {:<25}".format(id, year, men, women, total))
            print("-" * 90)
        else:
            print(f"No se encontró ningún registro con ID {id_a_consultar}")

    elif opcion == "2":
        # Agrega registro por ID        
        anio_nuevo = int(input("Ingresa el nuevo año: "))
        emigra_h = int(input("Ingresa la cantidad emigratoria de hombres: "))
        emigra_w = int(input("Ingresa la cantidad emigratoria de mujeres: "))

        insert_query = """
            INSERT INTO emigracion (year, emigration_men, emigration_women, total_emigration)
            VALUES (%s, %s, %s, %s)
            """
        # Calcular el valor de total_emigration
        total_emigration = emigra_h + emigra_w

        data = (
            
            anio_nuevo,
            emigra_h,
            emigra_w,
            total_emigration,
        )

        try:
            cursor.execute(insert_query, data)
            connection.commit()
            print("Registro agregado correctamente.")
        except Exception as ex:
            print("Error al agregar el registro:", ex)
     

    elif opcion == "3":
        # Modifica registro por ID
        id_a_modificar = int(input("Ingresa el ID del registro que deseas modificar: "))
        anio_nuevo = input("Ingresa el nuevo año: ")
        emigra_h = int(input("Ingresa la nueva cantidad emigratoria de hombres: "))
        emigra_w = int(input("Ingresa la nueva cantidad emigratoria de mujeres: "))
        # Calcular el valor de total_inmigration
        total_emigration = emigra_h + emigra_w

        data = (
        
            anio_nuevo,
            emigra_h,
            emigra_w,
            total_emigration,
        )
        cursor.execute("UPDATE emigracion SET year = %s, emigration_men = %s, emigration_women = %s, total_emigration = %s WHERE id = %s", (anio_nuevo, emigra_h, emigra_w, total_emigration, id_a_modificar))
        cursor.fetchone()
        connection.commit()      
        print("Registro modificado correctamente.")

    elif opcion == "4":
        # Eliminar registro por ID
        id_a_eliminar = int(input("Ingresa el ID del registro que deseas eliminar: "))
        cursor.execute("DELETE FROM emigracion WHERE id = %s", (id_a_eliminar,))
        connection.commit()
        print("Registro eliminado correctamente.")

    elif opcion == "5":
        # Imprimir toda la base de datos ACTUALIZADA.
        cursor.execute(query)
        results = cursor.fetchall()
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

