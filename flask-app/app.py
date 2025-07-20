from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Cambia estos datos por los tuyos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="TU_PASSWORD",
    database="flaskdb"
)

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return render_template("index.html", usuarios=usuarios)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    email = request.form['email']
    cursor = db.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, email) VALUES (%s, %s)", (nombre, email))
    db.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        cursor.execute("UPDATE usuarios SET nombre=%s, email=%s WHERE id=%s", (nombre, email, id))
        db.commit()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()
        return render_template("editar.html", usuario=usuario)

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/api/usuarios', methods=['GET'])
def api_usuarios():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return jsonify(usuarios)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
