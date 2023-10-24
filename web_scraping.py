import os
import requests
from bs4 import BeautifulSoup
import csv
import mysql.connector

def web_scraping ():

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
        date_men = []
        date_women = []
        total_date = []

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
            date_men.append(men)
            date_women.append(women)
            total_date.append(total)

        # Crear archivo CSV 
        csv_filename = os.path.join(ruta_completa, 'argentina_inmigrantes_totales_tabla1.csv')
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Year', 'Inmigration Men', 'Inmigration Women', 'Total Inmigration']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for i in range(len(years)):
                writer.writerow({
                    'Year': years[i],
                    'Inmigration Men': date_men[i],
                    'Inmigration Women': date_women[i],
                    'Total Inmigration': total_date[i],
                })
    else:
        print("La tabla no se encontró en la página.")

    print("Datos extraídos y guardados en el archivo CSV en la ubicación especificada:", csv_filename)
    
web_scraping ()  