from flask import Flask, render_template, request
import mysql.connector

emigra = Flask(__name__)

# Configura la conexión a la base de datos
db = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='root',
    database='emigra'
)

@emigra.route('/')
def index():
    return render_template('emigra.html')

@emigra.route('/consulta', methods=['POST'])
def consulta():
    cursor = db.cursor()
    year = request.form['year']
    cursor.execute(f"SELECT * FROM emigracion WHERE year = {year}")
    result = cursor.fetchall()
    return render_template('consulta/consulta.html', result=result)

if __name__ == '__main__':
    emigra.run()
