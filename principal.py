from flask import Flask, render_template, redirect
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'agenda'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/usuarios')
def ver_usuarios():
    cursor.execute("SELECT * from usuarios")
    data = cursor.fetchall()
    return render_template('usuarios.html',usuarios = data)

@app.route('/contactos')
def ver_contactos():
    cursor.execute("SELECT * from contactos")
    data = cursor.fetchall()
    return render_template('contactos.html',contactos = data)

@app.route('/citas')
def ver_citas():
    cursor.execute("SELECT * from citas")
    data = cursor.fetchall()
    return render_template('citas.html',citas = data)

@app.route('/todos')
def ver_todos():
    cursor.execute("SELECT usu_nombre, con_nombre, con_apellido, con_telefono, cit_lugar, cit_fecha "+
                    "FROM usuarios as usu " +
                    "LEFT JOIN contactos as con on (usu.usu_id = con.usu_id) " +
                    "LEFT JOIN citas as cit on (con.con_id = cit.con_id)")
    data = cursor.fetchall()
    return render_template('todos.html', citas = data)

@app.route('/agregaru')
def agregaru():
    return render_template('agregaru.html')

@app.route('/agregar')
def agregar(name):
    cursor.execute("INSERT INTO 'usuarios' ( 'usu_nombre', 'usu_clave') VALUES (name)")
    data = cursor.fetchall()
    return redirect("/ver_usuarios")


if __name__ == '__main__':
    app.run(debug=True)


