from flask import Flask, render_template, redirect, request, url_for
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
def agregar_usuario():
    if request.method == 'POST':
        nombre = request.form["nombre"]
        clave = request.form["clave"]
        cursor.execute("INSERT INTO `usuarios`( `usu_nombre`, `usu_clave`) VALUES (%s, sha1(%s))",(nombre,clave))
        conn.commit()
        return redirect(url_for('ver_usuarios'))
    else:
        return render_template('agregaru.html')

@app.route('/modusuario', methods = ['GET','POST'])
def mod_usuario():
    if request.method == 'POST':
        id = request.form["id"]
        nombre = request.form["nombre"]
        clave = request.form["clave"]
        cursor.execute("UPDATE `usuarios` SET  `usu_nombre`=%s, `usu_clave`=sha1(%s) WHERE `usu_id`=%s",(nombre,clave,id))
        conn.commit()
        return redirect(url_for('ver_usuarios'))
    else:
        id = request.args["id"]
        cursor.execute("SELECT usu_id, usu_nombre FROM usuarios WHERE usu_id = "+ id)
        usuario = cursor.fetchone()
        return render_template('modusu.html', usuario = usuario)

@app.route('/eliminarusuario')
def eliminar_usuario():
    if request.method == 'GET':
        id = request.args["id"]
        cursor.execute("DELETE FROM `usuarios` WHERE usu_id = "+ id)
        conn.commit()
        return redirect(url_for('ver_usuarios'))

@app.route('/agregarcontacto', methods = ['GET','POST'])
def agregar_contacto():
    if request.method == 'POST':
        usuid = request.form["usuid"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"] 
        email = request.form["email"] 
        cursor.execute("INSERT INTO `contactos`(`usu_id`, `con_nombre`, `con_apellido`, `con_direccion`, `con_telefono`, `con_email`)" +
                    "VALUES (%s,%s,%s,%s,%s,%s)",(usuid,nombre,apellido,direccion,telefono,email))
        conn.commit()
        return redirect(url_for('ver_contactos'))
    else:
        return render_template('agregarcon.html')


@app.route('/modcontacto', methods = ['GET','POST'])
def mod_contacto():
    if request.method == 'POST':
        id = request.form["id"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"] 
        email = request.form["email"] 
        cursor.execute("UPDATE `contactos` SET `con_nombre`=%s,`con_apellido`=%s,`con_direccion`=%s,`con_telefono`=%s,`con_email`=%s WHERE `con_id`=%s",(nombre,apellido,direccion,telefono,email,id))
        conn.commit()
        return redirect(url_for('ver_contactos'))
    else:
        id = request.args["id"]
        cursor.execute("SELECT `usu_id`,`con_nombre`,`con_apellido`,`con_direccion`,`con_telefono`,`con_email` FROM contactos WHERE con_id = "+id)
        contacto = cursor.fetchone()
        return render_template('modcon.html', contacto = contacto)

@app.route('/eliminarcontacto')
def eliminar_contacto():
    if request.method == 'GET':
        id = request.args["id"]
        cursor.execute("DELETE FROM `contactos` WHERE con_id = "+ id)
        conn.commit()
        return redirect(url_for('ver_contactos'))


@app.route('/agregarcita', methods = ['GET','POST'])
def agregarcita():
    if request.method == 'POST':
        conid = request.form["conid"]
        lugar = request.form["lugar"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        descripcion = request.form["descripcion"] 
        cursor.execute("INSERT INTO `citas`(`con_id`, `cit_lugar`, `cit_fecha`, `cit_hora`, `cit_descripcion`)" +
                    "VALUES (%s,%s,%s,%s,%s,%s)",(conid,lugar,fecha,hora,descripcion))
        conn.commit()
        return redirect(url_for('ver_citas'))
    else:
        return render_template('agregarcit.html')


@app.route('/modcit', methoss = ['GET','POST'])
def modcit():
    if request.method == 'POST':
        id = request.form["id"]
        lugar = request.form["lugar"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        descripcion = request.form["descripcion"] 
        cursor.execute("UPDATE `citas` SET `cit_lugar`=%s,`cit_fecha`=%s,`cit_hora`=%s,`con_descripcion`=%s WHERE `cit_id`=%s",(lugar,fecha,hora,descripcion,id))
        conn.commit()
        return redirect(url_for('ver_citas'))
    else:
        id = request.args["id"]
        cursor.execute("SELECT 'con_id' , 'cit-lugar' , 'cit_fecha' , 'cit_hora' , 'cit_descripcion' FROM citas WHERE cit_id = "+id)
        citas = cursor.fetchone()
        return render_template('modcita.html', citas = citas)


@app.route('/eliminarcita')
def eliminar_cita():
    if request.method == 'GET':
        id = request.args["id"]
        cursor.execute("DELETE FROM `citas` WHERE cit_id = "+ id)
        conn.commit()
        return redirect(url_for('ver_citas'))

if __name__ == '__main__':
    app.run(debug=True)


