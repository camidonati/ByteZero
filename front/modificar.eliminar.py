from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

modeli = Flask(__name__)

# Conexión a la base
db = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='root',
    database='emigra'
)

@modeli.route('/')
def index():
    return render_template('baseactual.html')

@modeli.route('/vertabla', methods=['GET', 'POST'])

def ver_tabla():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM emigracion")
    result = cursor.fetchall()

    if request.method == 'POST':
        action = request.form['action']
        if action == 'modificar':
            # Modificar registro
            id_to_modify = request.form['id_to_modify']
            new_year = request.form['new_year']
            new_emigration_men = request.form['new_emigration_men']
            new_emigration_women = request.form['new_emigration_women']
            new_total_emigration = request.form['new_total_emigration']

            # Actualiza la base de datos
            cursor.execute("UPDATE emigracion SET year=%s, emigration_men=%s, emigration_women=%s, total_emigration=%s WHERE id=%s",
                           (new_year, new_emigration_men, new_emigration_women, new_total_emigration, id_to_modify))
            db.commit()
            return redirect(url_for('ver_tabla'))

        elif action == 'eliminar':
            id_to_delete = request.form['id_to_delete']
            # Eliminar registro
            cursor.execute(f"DELETE FROM emigracion WHERE id = {id_to_delete}")
            db.commit()
            return redirect(url_for('ver_tabla'))

    return render_template('baseactual.html', result=result)


if __name__ == '__main__':
    modeli.run()
