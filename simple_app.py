from flask import Flask, request, render_template, redirect, url_for
import os
import pymysql

app = Flask(__name__)

MYSQL_PASSWORD = "super_secret_123"

DB_CONFIG = {
    'host': 'servidor-bd',          
    'user': 'root',
    'password': os.getenv('DB_PASSWORD'),
    'database': 'adso_db',              
    'connect_timeout': 3  
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

def init_db():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql_create = """
            CREATE TABLE IF NOT EXISTS aprendices (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_completo VARCHAR(100) NOT NULL,
                numero_documento VARCHAR(20) NOT NULL,
                ficha VARCHAR(20) NOT NULL,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(sql_create)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error al verificar la tabla: {e}")

@app.route("/")
def home():

    return "Error interno del servidor", 500

@app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form.get("nombre_completo")
    documento = request.form.get("numero_documento")
    ficha = request.form.get("ficha")

    if nombre and documento and ficha:
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql_insert = """
                INSERT INTO aprendices (nombre_completo, numero_documento, ficha) 
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql_insert, (nombre, documento, ficha))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al registrar: {e}")

    return redirect(url_for("home"))

@app.route("/version", methods=["GET"])
def version():
    return "<h2>hola ya puedes ingresar, verificacion completa, todo bien pa la buena</h2>", 200

if __name__ == '__main__':
 
    app.run(host="0.0.0.0", port=5050, debug=True)