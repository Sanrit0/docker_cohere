from flask import Flask, request, render_template
import cohere
import configparser
import pymysql

app = Flask(__name__)

def insert_into_database(question: str, answer: str):
    try:
        
        # Cargar el archivo de configuración
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Acceder a las configuraciones
        username = config['Credentials']['username']
        password = config['Credentials']['password']
        host = config['Credentials']['host']
        port = config['Credentials']['username']
        db = pymysql.connect(host = host,
                     user = username,
                     password = password,
                     cursorclass = pymysql.cursors.DictCursor
                    )

        # El objeto cursor es el que ejecutará las queries y devolverá los resultados

        cursor = db.cursor()
        # Para usar la BD  recien creada

        cursor.connection.commit()
        use_db = ''' USE ask_database'''
        cursor.execute(use_db)

        insert_data = '''
            INSERT INTO ask (question,answer)
            VALUES ('%s', '%s')
            ''' % (question,answer)

        cursor.execute(insert_data)

        # Confirmar los cambios y cerrar la conexión
        db.commit()
        cursor.close()
        db.close()
        print("Datos insertados correctamente usando pymysql.")
    except pymysql.Error as err:
        print(f"Error al insertar datos: {err}")

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    input_text = request.form['inputText']
    
    co = cohere.Client("N4EIFjMurRT4QGpcH5MViDIOtCuXAlFjDALgCfTV")
    response = co.chat(
	message=input_text,
    max_tokens=100
    )

    insert_into_database(input_text,response.text)

    return render_template('index.html', display_text=('Pregunta: '+input_text+':<br>'+'<br>'+'Respuesta: '+response.text))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)