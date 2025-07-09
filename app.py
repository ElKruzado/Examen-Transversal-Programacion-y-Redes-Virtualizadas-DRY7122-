from flask import Flask, request, redirect, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Lista de usuarios válidos (nombres de los integrantes)
USUARIOS_VALIDOS = ["Samuel", "Cristobal", "Manuel"]

# Inicializar la app Flask
app = Flask(__name__)

# Crear base de datos y tabla si no existen
def init_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Ruta principal
@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = ""
    if request.method == "POST":
        nombre = request.form["nombre"]
        password = request.form["password"]

        if nombre in USUARIOS_VALIDOS:
            password_hash = generate_password_hash(password)
            conn = sqlite3.connect("usuarios.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, password_hash))
            conn.commit()
            conn.close()
            mensaje = "Usuario registrado correctamente."
        else:
            mensaje = "Nombre no válido."

    return render_template_string("""
        <h2>Registro de Usuario</h2>
        <form method="post">
            Nombre: <input type="text" name="nombre"><br>
            Contraseña: <input type="password" name="password"><br>
            <input type="submit" value="Registrar">
        </form>
        <p>{{ mensaje }}</p>
    """, mensaje=mensaje)

if __name__ == "__main__":
    init_db()
    app.run(port=5800)
