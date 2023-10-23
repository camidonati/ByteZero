import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
from tabulate import tabulate


# Definir la ruta completa donde deseas guardar el archivo CSV
ruta_completa = os.path.dirname(os.path.realpath(__file__))

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
    # Crear un DataFrame con los datos
data = {
    'Year': years,
    'Emigration Men': emigration_men,
    'Emigration Women': emigration_women,
    'Total Emigration': total_emigration
}
df = pd.DataFrame(data)

# Realizar análisis con Pandas
# Por ejemplo, calcular estadísticas descriptivas
statistics = df.describe()

# Guardar el DataFrame en un archivo CSV
df.to_csv('emigration_data.csv', index=False)

# Imprimir el DataFrame como una tabla
print(tabulate(df, headers='keys', tablefmt='pretty'))
    




# Creación de la conexión con el servidor
try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='Franco4567'
    )

    if connection.is_connected():
        print("Conexión exitosa")

    # Crear o eliminar la base de datos según tus necesidades
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
        password='Franco4567',
        database='emigra'
    )
    if connection.is_connected():
        print("Conexión a la base de datos exitosa")

except Exception as ex:
    print(ex)

# Creación del cursor para recorrer la base
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
print("Datos insertados en la base de datos SQL.")



# Cerrar la conexión
connection.close()

# Encontrar el año con la mayor emigración total
max_emigration_year = df['Total Emigration'].idxmax()
print(f"Año con la mayor emigración: {df['Year'][max_emigration_year]}")

# Crear un gráfico de línea
plt.figure(figsize=(10, 6))
plt.plot(df['Year'], df['Total Emigration'], marker='o')
plt.xlabel('Año')
plt.ylabel('Total Emigración')
plt.title('Emigración Anual de Argentina')
plt.grid(True)
plt.show()
