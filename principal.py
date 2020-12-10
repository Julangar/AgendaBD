from flask import Flask, render_template, redirect, request
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

@app.route('/agregarusuario', methods = ['GET','POST'])
def agregarusuario():
    if request.method == 'POST':
        nombre = request.form["nombre"]
        clave = request.form["clave"]
        cursor.execute("INSERT INTO `usuarios`( `usu_nombre`, `usu_clave`) VALUES ("+ nombre +", sha1("+ clave +"))")
        conn.commit()
        return redirect("/usuarios")
    else:
        return render_template('agregaru.html')

@app.route('/agregaru')
def agregaru():
    cursor.execute("INSERT INTO `usuarios`( `usu_nombre`, `usu_clave`) VALUES ('nombre', sha1('clave'))")
    data = cursor.fetchall()
    return redirect("/usuarios")

@app.route('/agregarcontacto')
def agregarcontacto():
    return render_template('agregarcon.html')

@app.route('/agregarcon')
def agregarcon():
    cursor.execute("INSERT INTO `contactos`(`usu_id`, `con_nombre`, `con_apellido`, `con_direccion`, `con_telefono`, `con_email`)" +
                    "VALUES (1,'Pepito','Perez','Cra 50 1g',3044050505, 'pepito@mail.com')")
    data = cursor.fetchall()
    return redirect("/contactos")

@app.route('/modcontacto')
def modcontacto():
    return render_template('modcon.html')

@app.route('/modcon')
def modcon():
    cursor.execute("UPDATE `contactos` SET `con_id`=[value-1],`usu_id`=[value-2],`con_nombre`=[value-3],`con_apellido`=[value-4],`con_direccion`=[value-5],`con_telefono`=[value-6],`con_email`=[value-7] WHERE 1")
    data = cursor.fetchall()
    return redirect("/contactos")

@app.route('/agregarcita')
def agregarcita():
    return render_template('agregarcit.html')

@app.route('/agregarcit')
def agregarcit():
    cursor.execute("INSERT INTO `citas`(`con_id`, `cit_lugar`, `cit_fecha`, `cit_hora`, `cit_descripcion`) "+ 
                    "VALUES (1,'lugar','DD/MM/AAAA','00:00:00','descripcion')")
    data = cursor.fetchall()
    return redirect("/citas")

@app.route('/modcita')
def modcita():
    return render_template('modcita.html')

@app.route('/modcit')
def modcit():
    cursor.execute("UPDATE `citas` SET `cit_id`= 1,`con_id`=1,`cit_lugar`='lugar',`cit_fecha`='00/00/0000',`cit_hora`= '00:00:00',`cit_descripcion`= 'descripcion' WHERE `cit_id` = 8")
    data = cursor.fetchall()
    return redirect("/citas")

if __name__ == '__main__':
    app.run(debug=True)


