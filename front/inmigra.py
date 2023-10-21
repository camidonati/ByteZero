from flask import Flask, render_template, request
import mysql.connector

inmigra = Flask(__name__)

# Configura la conexión a la base de datos
db = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='root',
    database='inmigra'
)

@inmigra.route('/')
def index():
    return render_template('inmigra.html')

@inmigra.route('/consulta', methods=['POST'])

def consulta():
    cursor = db.cursor()
    year = request.form['year']
    cursor.execute(f"SELECT * FROM inmigracion WHERE year = {year}")
    result = cursor.fetchall()
    return render_template('consulta/consultai.html', result=result)

if __name__ == '__main__':
    inmigra.run()


