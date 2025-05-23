from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'Localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ronny2003'
app.config['MYSQL_DB'] = 'LoginBD'
BD = MySQL(app)

@app.route('/')
def Index():
    cur = BD.connection.cursor()
    cur.execute("SELECT id, nombre, apellido, email, fecha_creacion FROM usuarios_logueados ORDER BY fecha_creacion DESC")
    usuarios = cur.fetchall()  
    cur.close()
    return render_template('Login.html', usuarios=usuarios)

@app.route('/agregar', methods=['POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']
        cur = BD.connection.cursor()
        cur.execute('INSERT INTO usuarios_logueados (nombre, apellido, email, password) VALUES (%s, %s, %s, %s);', (nombre, apellido, email, password))
        BD.connection.commit()
        return redirect(url_for('Index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = BD.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']

        cur.execute('UPDATE usuarios_logueados SET nombre=%s, apellido=%s, email=%s, password=%s WHERE id=%s',
                    (nombre, apellido, email, password, id))
        BD.connection.commit()
        cur.close()
        return redirect(url_for('Index'))

    else:
        cur.execute('SELECT * FROM usuarios_logueados WHERE id = %s', (id,))
        usuario = cur.fetchone()
        cur.close()
        if usuario:
            return render_template('editar_usuario.html', usuario=usuario)
        else:
            return "Usuario no encontrado", 404

@app.route('/eliminar/<int:id>', methods=['POST'])
def delete(id):
    cur = BD.connection.cursor()
    cur.execute("DELETE FROM usuarios_logueados WHERE id = %s", (id,))
    BD.connection.commit()
    cur.close()
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
    