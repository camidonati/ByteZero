from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/consulta', methods=['POST'])

def ejecutar_script():
    sel = request.form.get('script')
 
    if sel== 'script1':
        try:
            result = subprocess.check_output(['python', 'C:\\Users\\delfe\\Desktop\\BSoup\\scrap\\front\\front.py'], text=True)
        except subprocess.CalledProcessError as e:
            result = f"Error: {e}"
    elif sel== 'script2':
        try:
            result = subprocess.check_output(['python', 'C:\\Users\\delfe\\Desktop\\BSoup\\scrap\\front\\frontin.py'], text=True)
        except subprocess.CalledProcessError as e:
            result = f"Error: {e}"
    else:
        result = "Script no válido"

    return render_template('inicio.html', resultado=result)

if __name__ == '__main__':
    app.run()
