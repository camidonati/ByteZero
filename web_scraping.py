import os
import requests
from bs4 import BeautifulSoup
import csv
import BBDD


def web_scraping (datos):
    
    # URL de la página
    if datos == "inmigracion":
        url = 'https://datosmacro.expansion.com/demografia/migracion/inmigracion/argentina'
        # Borrar la tabla
        delete_table_query = "DROP TABLE IF EXISTS inmigracion"
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
        
        # Insertar datos en la tabla
        insert_query = """
        INSERT INTO inmigracion (year, inmigration_men, inmigration_women, total_inmigration)
        VALUES (%s, %s, %s, %s)
        """
        
        insert_data = "SELECT * FROM inmigracion"
    
    elif datos == "emigracion":
        url = 'https://datosmacro.expansion.com/demografia/migracion/emigracion/argentina'
        # Borrar la tabla
        delete_table_query = "DROP TABLE IF EXISTS emigracion"
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
        # Insertar datos en la tabla
        insert_query = """
        INSERT INTO emigracion (year, emigration_men, emigration_women, total_emigration)
        VALUES (%s, %s, %s, %s)
        """
        
        insert_data = "SELECT * FROM emigracion"


    # Definir la ruta completa donde deseas guardar el archivo CSV
    ruta_completa = os.path.dirname(os.path.realpath(__file__))

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
        data_men = []
        data_women = []
        total_data = []

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
            data_men.append(men)
            data_women.append(women)
            total_data.append(total)

        # Crear archivo CSV 
        csv_filename = os.path.join(ruta_completa, "argentina_"+datos+"_totales_tabla1.csv")
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Year', datos + " Men", datos + " Women", "Total " + datos]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for i in range(len(years)):
                
                writer.writerow({
                    'Year': years[i],
                    datos + " Men": data_men[i],
                    datos + " Women": data_women[i],
                    "Total " + datos: total_data[i],
                })
    else:
        print("La tabla no se encontró en la página.")

    print("Datos extraídos y guardados en el archivo CSV en la ubicación especificada:", csv_filename)
    
    # while True:
    #     choice = input("¿Deseas eliminar la base de datos existente? (s/n): ").strip().lower()
    #     if choice == 's':
    #         borrar = True
    #         break
    #     elif choice == 'n':
    #         borrar = False
    #         break
    #     else:
    #         print("Opción no válida. Por favor, elige 's' para eliminar o 'n' para no eliminar la base de datos.")
        
    
    # Iniciamos la base de datos
    conexion = BBDD.abrir_base()
    cursor = conexion.cursor()
    print("Conexión exitosa")
    
    

    #     # Eliminar la tabla de la base de datos si se selecciona
    #     cursor.execute(delete_table_query)
    
    # Consultar el esquema para verificar si la tabla existe
    cursor.execute("SHOW TABLES LIKE %s", (datos,))
    resultado = cursor.fetchone()

    if resultado is None:
        cursor.execute(create_table_query)
        for i in range(len(years)):
            data = (
                years[i],
                int(data_men[i]),
                int(data_women[i]),
                int(total_data[i]),
            )
            cursor.execute(insert_query, data)
            # Commit los cambios
            conexion.commit()
            print("Datos insertados en la base de datos SQL.")
        
    cursor.execute(insert_data)
    res = cursor.fetchall()

    # Commit los cambios
    conexion.commit()
    print("Tabla creada en la base de datos SQL.")
        
    #Cerramos la base de datos
    conexion.close()
        
    
    
    
