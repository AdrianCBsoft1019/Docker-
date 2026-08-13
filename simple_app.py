from flask import Flask, request, render_template, redirect, url_for
import pymysql

app = Flask(__name__)

DB_CONFIG = {
    'host': 'servidor-bd',          
    'user': 'root',
    'password': 'sena123',
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
    init_db() 
    
    db_status = ""
    aprendices = []

    try:
        conn = get_db_connection()
        db_status = "¡Conexión exitosa a la BD!"
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM aprendices ORDER BY creado_en DESC")
            aprendices = cursor.fetchall()
            
        conn.close()
    except Exception as e:
        db_status = f"Error en la conexión: {e}"

    return render_template("index.html", db_status=db_status, aprendices=aprendices, puerto="5050")

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)