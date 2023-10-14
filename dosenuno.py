import os
import requests
from bs4 import BeautifulSoup
import csv
import mysql.connector

# Definir la ruta completa donde deseas guardar el archivo CSV
ruta_completa = r'ruta completa de guardado del archivo CSV'

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

        # Extraer los datos y almacenarlos en las listas correspondientes
        year = columns[0].text.strip()
        men = columns[1].text.strip().replace('.', '')
        women = columns[2].text.strip().replace('.', '')
        total = columns[3].text.strip().replace('.', '')
        

        years.append(year)
        emigration_men.append(men)
        emigration_women.append(women)
        total_emigration.append(total)
        

    # Crear un archivo CSV en la ubicación especificada y escribir los datos en él
    csv_filename = os.path.join(ruta_completa, 'argentina_emigrantes_totales_tabla1.csv')
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Year', 'Emigration Men', 'Emigration Women', 'Total Emigration', 'Percentage Emigration']
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


#creacion de la conexion con el servidor con try an except
try:
    connection = mysql.connector.connect(
        host= '127.0.0.1',
        port= '3306',
        user = 'root',
        password= 'root',    
        db= 'scrap'
    )
    if connection.is_connected():
        print("Conexion exitosa")

except Exception as ex:
    print (ex)

#Creacion del cursor para recorrer la base
cursor = connection.cursor()

# Crear una tabla si no existe
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

#print("Datos insertados en la base de datos SQL.")
cursor.execute("SELECT * FROM scrap.emigracion")
result1 = cursor.fetchall()
print(result1)
#cerrar la conexión
connection.close()
