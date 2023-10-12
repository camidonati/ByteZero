import os
import requests
from bs4 import BeautifulSoup
import csv

# Definir la ruta completa donde deseas guardar el archivo CSV
ruta_completa = r'D:\Escritorio\CIBICI, ISPC, CODER\Año 2023\Ciencia de Datos e Inteligencia artificial\Primer año\Programación 1\Proyecto integrador'

# URL de la página
url = 'https://datosmacro.expansion.com/demografia/migracion/inmigracion/argentina#:~:text=Aumenta%20el%20n%C3%BAmero%20de%20inmigrantes%20en%20Argentina&text=La%20inmigraci%C3%B3n%20femenina%20es%20superior,%2C%20que%20son%20el%2046.56%25'

# Realizar la solicitud GET
response = requests.get(url)

# Parsear el contenido HTML con BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar la tabla por su ID
table = soup.find('table', id='tb2_17115')

# Verificar si la tabla se ha encontrado
if table:
    # Inicializar listas para almacenar los datos
    paises = []
    inmigrantes = []

    # Encontrar todas las filas de datos en la tabla
    rows = table.find_all('tr')

    # Iterar a través de las filas, comenzando desde la segunda fila (índice 1) para omitir el encabezado
    for row in rows[1:]:
        # Encontrar todas las columnas de datos en la fila
        columns = row.find_all('td')

        # Extraer los datos y almacenarlos en las listas correspondientes
        pais = columns[0].text.strip()
        inmigrante = columns[1].text.strip().replace('.', '')

        paises.append(pais)
        inmigrantes.append(inmigrante)

    # Crear un archivo CSV en la ubicación especificada y escribir los datos en él
    csv_filename = os.path.join(ruta_completa, 'datos_inmigrantes_2020_tabla2.csv')
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['País', 'Inmigrantes']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(paises)):
            writer.writerow({
                'País': paises[i],
                'Inmigrantes': inmigrantes[i]
            })
else:
    print("La tabla no se encontró en la página.")

print("Datos extraídos y guardados en el archivo CSV en la ubicación especificada:", csv_filename)

