from flask import Flask, render_template, redirect, request, url_for
from flaskext.mysql import MySQL
import hashlib as hb


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

class usuario():
    nombre=''
    id=0
    ver=True

    def guardar (self,a,b):
        self.nombre=a
        self.id=b
  

person = usuario()

@app.route('/', methods = ['POST','GET'])
def inicio():
    person.ver=True
    return render_template('inicio.html')


@app.route('/menu', methods = ['GET','POST'])
def ver_menu():
    if person.ver==True:
        if request.method == 'POST':
            app.logger.info('Entro al post')
            nombre = request.form['usuario']
            clave = request.form['clave']
            cursor.execute("SELECT usu_clave FROM usuarios WHERE usu_nombre='"+nombre+"';")
            persona = cursor.fetchone()
            app.logger.info(persona)
            if (nombre=="Admin" and clave=="Admin"):
                person.guardar("1",1)
                return render_template('menuadmin.html')
            else:
                if persona == None:
                    return render_template('error.html')
                else:
                    persona2 = ''.join(persona)
                    if persona2 == clave:
                        cursor.execute("SELECT usu_id FROM usuarios WHERE usu_nombre='"+nombre+"';")     
                        persona = cursor.fetchone()
                        person.guardar(nombre,int(''.join(map(str,persona))))
                        cursor.execute("SELECT DISTINCT T.cit_id, concat(concat(C.con_nombre, ' '),C.con_apellido), T.cit_lugar, T.cit_fecha, T.cit_hora, T.cit_descripcion from citas T, contactos C, usuarios U WHERE C.usu_id='"+str(person.id)+"' AND C.con_id=T.con_id;")
                        data = cursor.fetchall() 
                        return render_template('menu.html', citas = data)
                    else:
                        return render_template('error.html')
        else:
            return render_template('inicio.html')
    else:    
        return render_template('menu.html')
@app.route('/menuusu', methods = ['GET','POST'])
def ver_menuusu():
    person.ver=False
    cursor.execute("SELECT DISTINCT concat(concat(C.con_nombre, ' '),C.con_apellido), T.cit_lugar, T.cit_fecha, T.cit_hora, T.cit_descripcion from citas T, contactos C, usuarios U WHERE C.usu_id='"+str(person.id)+"' AND C.con_id=T.con_id;")
    data = cursor.fetchall()
    return render_template('menuusu.html',citas = data)

@app.route('/usuarios')
def ver_usuarios():
    person.ver=False
    cursor.execute("SELECT * from usuarios")
    data = cursor.fetchall()
    return render_template('usuarios.html',usuarios = data)


@app.route('/contactos')
def ver_contactos():
    person.ver=False
    cursor.execute("SELECT * from contactos WHERE usu_id='"+str(person.id)+"';")
    data = cursor.fetchall()
    return render_template('contactos.html',contactos = data)


@app.route('/citas')
def ver_citas():
    person.ver=False
    cursor.execute("SELECT DISTINCT concat(concat(C.con_nombre, ' '),C.con_apellido), T.cit_lugar, T.cit_fecha, T.cit_hora, T.cit_descripcion from citas T, contactos C, usuarios U WHERE C.usu_id='"+str(person.id)+"' AND C.con_id=T.con_id;")
    data = cursor.fetchall() #, citas = data
    return render_template('citas.html',citas = data)


@app.route('/todos')
def ver_todos():
    person.ver=False
    cursor.execute("SELECT usu_nombre, con_nombre, con_apellido, con_telefono, cit_lugar, cit_fecha "+
                    "FROM usuarios as usu " +
                    "LEFT JOIN contactos as con on (usu.usu_id = con.usu_id) " +
                    "LEFT JOIN citas as cit on (con.con_id = cit.con_id)")
    data = cursor.fetchall()
    return render_template('todos.html', citas = data)


@app.route('/agregarusuario', methods = ['POST','GET'])
def agregar_usuario():
    person.ver=True
    app.logger.info('Entro al agregaru')
    if request.method == 'POST':
        app.logger.info('Entro al post')
        nombre = request.form["nombre"]
        clave = request.form["clave"]
        cursor.execute("INSERT INTO `usuarios`( `usu_nombre`, `usu_clave`) VALUES (%s, %s)",(nombre,clave))
        conn.commit()
        return redirect(url_for('inicio'))
    else:
        return render_template('agregaru.html')


'''@app.route('menuadmin')
def menu_admin():
    return render_template('menuadmin.html')
'''


@app.route('/modusuario', methods = ['GET','POST'])
def mod_usuario():
    person.ver=False
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
    person.ver=False
    if request.method == 'GET':
        id = request.args["id"]
        cursor.execute("DELETE FROM `usuarios` WHERE usu_id = "+ id)
        conn.commit()
        return redirect(url_for('ver_usuarios'))


@app.route('/agregarcontacto', methods = ['GET','POST'])
def agregar_contacto():
    person.ver=False
    if request.method == 'POST':
        """usuid = request.form["usuid"]"""
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"] 
        email = request.form["email"] 
        cursor.execute("INSERT INTO `contactos`(`usu_id`, `con_nombre`, `con_apellido`, `con_direccion`, `con_telefono`, `con_email`)" +
                    "VALUES (%s,%s,%s,%s,%s,%s)",(str(person.id),nombre,apellido,direccion,telefono,email))
        conn.commit()
        return redirect(url_for('ver_contactos'))
    else:
        return render_template('agregarcon.html')


@app.route('/modcontacto', methods = ['GET','POST'])
def mod_contacto():
    person.ver=False
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
        cursor.execute("SELECT `con_id`,`con_nombre`,`con_apellido`,`con_direccion`,`con_telefono`,`con_email` FROM contactos WHERE `con_id` = "+id)
        contacto = cursor.fetchone()
        return render_template('modcon.html', contacto = contacto)


@app.route('/eliminarcontacto')
def eliminar_contacto():
    person.ver=False
    if request.method == 'GET':
        id = request.args["id"]
        cursor.execute("DELETE FROM `contactos` WHERE con_id = "+ id)
        conn.commit()
        return redirect(url_for('ver_contactos'))


@app.route('/agregarcita', methods = ['GET','POST'])
def agregarcita():
    person.ver=False
    cursor.execute("SELECT con_id,concat(concat(con_nombre, ' '),con_apellido) from contactos WHERE usu_id='"+str(person.id)+"';")
    data = cursor.fetchall()
    if request.method == 'POST':
        conid = request.form["conid"]
        lugar = request.form["lugar"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        descripcion = request.form["descripcion"] 
        cursor.execute("INSERT INTO `citas`(`con_id`, `cit_lugar`, `cit_fecha`, `cit_hora`, `cit_descripcion`)" +
                    "VALUES (%s,%s,%s,%s,%s)",(conid,lugar,fecha,hora,descripcion))
        conn.commit()
        return redirect(url_for('ver_citas'))
    else:
        return render_template('agregarcit.html', contactos = data)


@app.route('/modcit', methods = ['GET','POST'])
def modcit():
    person.ver=False
    if request.method == 'POST':
        id = request.form["id"]
        lugar = request.form["lugar"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        descripcion = request.form["descripcion"] 
        cursor.execute("UPDATE `citas` SET `cit_lugar`=%s,`cit_fecha`=%s,`cit_hora`=%s,`cit_descripcion`=%s WHERE `cit_id`=%s",(lugar,fecha,hora,descripcion,id))
        conn.commit()
        return redirect(url_for('ver_citas'))
    else:
        id = request.args["id"]
        cursor.execute("SELECT `cit_id` , `con_id` , `cit_lugar` , `cit_fecha` , `cit_hora` , `cit_descripcion` FROM citas WHERE `cit_id` = "+id)
        citas = cursor.fetchone()
        return render_template('modcit.html', citas = citas)


@app.route('/eliminarcita')
def eliminar_cita():
    person.ver=False
    if request.method == 'GET':
        id = request.args["id"]
        cursor.execute("DELETE FROM `citas` WHERE cit_id = "+ id)
        conn.commit()
        return redirect(url_for('ver_citas'))


if __name__ == '__main__':
    app.run(debug=True)
