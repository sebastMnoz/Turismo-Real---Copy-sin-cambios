from dbm import dumb
from email import message
from itertools import count
from sqlite3 import Cursor
# es requerido instalar todo pip install flask --no-warn-script-location # pip install Flask-Mysqldb(Puede qu este no) #pip install flask-MySQL #pip install jinja2
from flask import Flask
from flask import render_template, request, redirect, url_for, session, flash
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = "Duoooc"


# Conexion a la base de datos

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'turismo_real'
mysql.init_app(app)

# Links de paginas

@app.route('/')
def lista_departamento():
    sql = "SELECT * FROM `departamento`"
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    cursor.execute(sql)  # verificar si la sentencia es exitosa
    departamento = cursor.fetchall()
    print(departamento)
    cursor.execute("SELECT * FROM `servicio_asociado`")
    servicio_asociado = cursor.fetchall()
    print(servicio_asociado)
    conn.commit()
    return render_template('pagina_inicio.html', departamento=departamento, servicio_asociado=servicio_asociado)

@app.route('/pag_admin')
def pag_admin():
    sql = "SELECT * FROM `departamento`"
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    cursor.execute(sql)  # verificar si la sentencia es exitosa
    departamento = cursor.fetchall()
    print(departamento)
    cursor.execute("SELECT * FROM `servicio_asociado`")
    servicio_asociado = cursor.fetchall()
    print(servicio_asociado)
    conn.commit()
    return render_template('pag_admin.html', departamento=departamento, servicio_asociado=servicio_asociado)

@app.route('/registrar_depto')
def registrar_depto():
    return render_template("registrar_depto.html")

@app.route('/editar_depto_link')
def editar_depto_link():
    return render_template("editar_depto.html")

@app.route('/inicio')
def inicio():
    return render_template('login.html')


@app.route('/cerrar_sesion')
def cerrar_sesion():
    flash("Sesion cerrada correctamente.", "success")
    return redirect('/inicio')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/departamentos')
def departamentos():
    return render_template('departamento.html')

@app.route('/login')
def loggear():
    return redirect("/inicio")

@app.route('/calendario')
def calendario():
    sql = "SELECT * FROM `reserva_depto` ;"
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    cursor.execute(sql)  # verificar si la sentencia es exitosa
    reserva_depto = cursor.fetchall()
    print(reserva_depto)
    conn.commit()
    return render_template('calendario.html', reserva_depto = reserva_depto)


 #Inicio de sesion
@app.route('/login', methods=["GET", "POST"])  # login
def login():

    if request.method == 'POST':
        _usuario = request.form['txtUsuario']
        _password = request.form['txtPasswordI']

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM `cliente` WHERE usuario = %s", (_usuario))
        cliente = cur.fetchone()
        print(cliente)
        cur.execute("SELECT * FROM `empleado` WHERE `usuario` = %s", (_usuario))
        empleado = cur.fetchone()
        print(empleado)
        cur.close()
        if cliente is None and empleado is None:
            flash('Usuario o contraseña no validos.', "error")
            print('usuario incorrecto')
            return redirect("/inicio")

        if cliente is not None:
            if len(cliente) > 0:
                passwd = cliente[9]
            if _password == passwd:
                if cliente[7] == 1:
                    print("Cliente")
                    flash('Sesion iniciada correctamente.', "success")
                    return redirect("/pag_cliente")
                elif cliente[7] == 2:
                    print("admin")
                    flash(
                        'Sesion iniciada como administrador correctamente.', "success")
                    return redirect("pag_admin")

            else:
                flash('Usuario o contraseña no validos.', "error")
                print('contraseña incorrecta ')
                return redirect("/inicio")
        else:
            passwd = empleado[11]
            if _password == passwd:
                if empleado[9] == 1:
                    print("Cliente")
                    flash('Sesion iniciada correctamente.', "success")
                    return redirect("/pag_cliente")
                elif empleado[9] == 2:
                    print("admin")
                    flash(
                        'Sesion iniciada como administrador correctamente.', "success")
                    return redirect("pag_admin")
            else:
                flash('Usuario o contraseña no validos.', "error")
                print('contraseña incorrecta ')
                return redirect("/inicio")

            return redirect("/registro")
#Fin Inicio de sesion

#Seccion departamento
@app.route('/registrar_departamento', methods=['POST'])
def registrar_departamento():

    _direccion = request.form['txtDireccion']
    _region = request.form['txtRegion']
    _comuna = request.form['txtComuna']
    _banno = request.form['txtBannos']
    _dormitorio = request.form['txtdormitorios']
    _noche = request.form['txtnoche']
    _foto1 = request.form['txtFotografia1']
    _foto2 = request.form['txtFotografia2']
    _foto3 = request.form['txtFotografia3']
    _foto4 = request.form['txtFotografia4']
    _dividendo = request.form['txtdividendo']
    _contribuciones = request.form['txtcontribuciones']
    __servicio = request.values['txtServicio']
    _nombre= request.form['txtweb']
    _mapa = request.form['txtMapa']

    if _direccion == "" or _region == "" or _comuna == "" or _banno == "" or _dormitorio == "" or _noche == "" or __servicio == "" or _foto1 == "" or _foto2 == "" or _foto3 == "" or _foto4 == "" or _dividendo == "" or _contribuciones == "" or _nombre == "" or _mapa == "":
        print('wea')
        flash(
            'Hay datos vacios, no olvide ingresar correctamente todos los datos.', "error")
        return redirect("/")
    else:
        sql = "INSERT INTO `departamento` (`id`, `direccion`, `region`, `comuna`, `banno`, `dormitorio`, `valor`, `fotografia_1`, `fotografia_2`, `fotografia_3`, `fotografia_4`, `gastos_dividendo`, `contribuciones`, `id_servicio_asociado`, `id_reparacion`, `titulo`, `mapa`) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, NULL, %s,%s); "
        datos = (_direccion, _region, _comuna, _banno,_dormitorio, _noche, _foto1,
                _foto2,_foto3,_foto4, _dividendo, _contribuciones, __servicio, _nombre, _mapa)
        flash('Departamento añadido correctamente.', "success")
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
        pass
        return redirect('/')

@app.route('/update_depto', methods=['POST'])  # funcion actualizar datos empleado
def update_depto():
    _direccion = request.form['txtDireccion']
    _region = request.form['txtRegion']
    _comuna = request.form['txtComuna']
    _banno = request.form['txtBannos']
    _dormitorio = request.form['txtdormitorios']
    _noche = request.form['txtnoche']
    _foto1 = request.form['txtFotografia1']
    _foto2 = request.form['txtFotografia2']
    _foto3 = request.form['txtFotografia3']
    _foto4 = request.form['txtFotografia4']
    _dividendo = request.form['txtdividendo']
    _contribuciones = request.form['txtcontribuciones']
    __servicio = request.values['txtServicio']
    _nombre= request.form['txtweb']
    _mapa = request.form['txtMapa']
    __id = request.form['txtID']

    sql ="UPDATE `departamento` SET `direccion` = %s, `region` = %s, `comuna` = %s,`banno` = %s, `dormitorio` = %s, `valor` = %s, `fotografia_1` = %s, `fotografia_2` = %s, `fotografia_3` =%s, `fotografia_4` = %s, `gastos_dividendo` = %s, `contribuciones` = %s, `id_servicio_asociado` = %s,`titulo` = %s, `mapa` =%s WHERE `departamento`.`id` = %s; "    
    datos = (_direccion, _region, _comuna, _banno,_dormitorio, _noche, _foto1,
            _foto2,_foto3,_foto4, _dividendo, _contribuciones,__servicio,  _nombre, _mapa, __id)
    print(__servicio)
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(sql, datos)
    print(cursor)
    flash('Departamento modificado correctamente.', "success")

    conn.commit()
    return redirect('/pag_admin')



@app.route('/eliminarDepto/<int:id>')  # funcion eliminar departamento
def eliminarDepto(id):
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion

    cursor.execute("DELETE FROM departamento WHERE id=%s", (id))
    flash('Departamento eliminado correctamente.', "success")
    conn.commit()
    return redirect('/pag_admin')

#@app.route('/editar_depto/<int:id>')
#def editar_depto(id):
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    # verificar si la sentencia es exitosa
    cursor.execute("SELECT * FROM departamento WHERE id=%s", (id))
    departamento = cursor.fetchall()
    conn.commit()
    return render_template('editar_depto.html', departamento=departamento)

@app.route('/editar_depto/<int:id>')
def editar_depto(id):
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    # verificar si la sentencia es exitosa
    cursor.execute("SELECT * FROM departamento WHERE id=%s", (id))
    departamento = cursor.fetchall()
    cursor.execute("SELECT `id_servicio_asociado` FROM `departamento` WHERE id=%s", (id))
    servicio_A = cursor.fetchall()
    cursor.execute(
        "SELECT * FROM `servicio_asociado` WHERE id = %s;", (servicio_A))
    servicio_asociado = cursor.fetchall()
    cursor.execute(
        "SELECT * FROM `inventario` WHERE `id_departamento` = %s", (id))
    inventario = cursor.fetchall()
    print(inventario)
    conn.commit()
    return render_template('editar_depto.html', departamento=departamento, servicio_asociado=servicio_asociado, inventario=inventario)


@app.route('/listar_departamentos/<int:id>')
def listar_departamentos(id):
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    # verificar si la sentencia es exitosa
    cursor.execute("SELECT * FROM departamento WHERE id=%s", (id))
    departamento = cursor.fetchall()
    cursor.execute("SELECT `id_servicio_asociado` FROM `departamento` WHERE id=%s", (id))
    servicio_A = cursor.fetchall()
    cursor.execute("SELECT * FROM `servicio_asociado` WHERE id = %s;", (servicio_A))
    servicio_asociado = cursor.fetchall()
    cursor.execute(
        "SELECT * FROM `inventario` WHERE `id_departamento` = %s", (id))
    inventario = cursor.fetchall()
    print(inventario)
    return render_template('departamento.html', departamento=departamento, servicio_asociado=servicio_asociado, inventario=inventario)





#Fin Seccion departamento

#Seccion empleado

@app.route('/registro_empleados')
def registro_empleados():
    return render_template('registrar_empleado.html')


@app.route('/listar_empleados')  # listar empleados
def fg():
    sql = "SELECT * FROM `empleado` WHERE `id_tipo_usuario` = 2 ; "
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    cursor.execute(sql)  # verificar si la sentencia es exitosa
    empleado = cursor.fetchall()
    print(empleado)
    conn.commit()
    return render_template('listar_empleados.html', empleado=empleado)


@app.route('/registrar_empleado', methods=['POST'])
def registrar_empleado():

    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _rut = request.form['txtRut']
    _celular = request.form['txtNumero']
    _direccion = request.form['txtDireccion']
    _Comuna = request.form['txtComuna']
    _Region = request.form['txtRegion']
    _correo = request.form['txtCorreo']
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']

    if _nombre == "" or _apellido == "" or _rut == "" or _celular == "" or _direccion == "" or _Comuna == "" or _Region == "" or _correo == "" or _usuario == "" or _password == "":
        print('wea')
        flash(
            'Hay datos vacios, no olvide ingresar correctamente todos los datos.', "error")
        return redirect("/registro")
    else:
        sql = "INSERT INTO `empleado` (`id`, `nombre`, `apellido`, `rut`, `telefono`, `direccion`, `comuna`, `region`, `correo_electronico`, `id_tipo_usuario`, `usuario`, `password`) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s, '2',%s,%s); "

        datos = (_nombre, _apellido, _rut, _celular, _direccion,
                 _Comuna, _Region, _correo, _usuario, _password)
        flash('Empleado registrado correctamente.', "success")
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
        pass
        return redirect('/listar_empleados')


@app.route('/updateEmp', methods=['POST'])  # funcion actualizar datos empleado
def updateEmp():
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _rut = request.form['txtRut']
    _celular = request.form['txtNumero']
    _direccion = request.form['txtDireccion']
    _comuna = request.form['txtComuna']
    _region = request.form['txtRegion']
    _correo = request.form['txtCorreo']
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']
    id = request.form['txtID']

    sql = "UPDATE `empleado` SET `nombre`=%s,`apellido`=%s,`rut`=%s,`telefono`=%s,`direccion`=%s,`comuna`=%s,`region`=%s,`correo_electronico`=%s,id_tipo_usuario = '2',`usuario`=%s,`password`=%s WHERE id = %s;"
    datos = (_nombre, _apellido, _rut, _celular, _direccion, _comuna, _region,
             _correo, _usuario, _password, id)
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(sql, datos)
    print(cursor)
    flash('Empleado modificado correctamente.', "success")

    conn.commit()
    return redirect('/listar_empleados')



@app.route('/editarEmp/<int:id>')  # funcion editar empleado
def editarEmp(id):

    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    # verificar si la sentencia es exitosa
    cursor.execute("SELECT * FROM empleado WHERE id=%s", (id))
    empleado = cursor.fetchall()
    conn.commit()
    return render_template('editar_empleado.html', empleado=empleado)



@app.route('/eliminarEmp/<int:id>')  # funcion eliminar empleado
def eliminarEmp(id):
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion

    cursor.execute("DELETE FROM empleado WHERE id=%s", (id))
    flash('Empleado eliminado correctamente.', "success")
    conn.commit()
    return redirect('/listar_empleados')


#fin seccion empleado

#Seccion Cliente
@app.route('/pag_cliente')
def pag_cliente():
    return render_template("pag_cliente.html")


@app.route('/listar_clientes')  # Listar clientes
def listar_clientes():

    sql = "select * from `cliente`; "
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    cursor.execute(sql)  # verificar si la sentencia es exitosa

    cliente = cursor.fetchall()
    print(cliente)

    conn.commit()
    return render_template('listar.html', cliente=cliente)


@app.route('/eliminar/<int:id>')  # funcion eliminar
def eliminar(id):
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion

    cursor.execute("DELETE FROM cliente WHERE id=%s", (id))
    flash('Usuario eliminado correctamente.', "success")
    conn.commit()
    return redirect('/listar_clientes')


@app.route('/registrar_cliente', methods=['POST'])
def storage():

    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _rut = request.form['txtRut']
    _celular = request.form['txtNumero']
    _correo = request.form['txtCorreo']
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']

    if _nombre == "" or _apellido == "" or _rut == "" or _celular == "" or _correo == "" or _usuario == "" or _password == "":
        print('wea')
        flash(
            'Hay datos vacios, no olvide ingresar correctamente todos los datos.', "error")
        return redirect("/registro")
    else:

        sql = "INSERT INTO `cliente` (`id`, `nombre`, `apellido`, `rut`, `nro_celular`, `correo_electronico`, `id_acompannate`, `id_tipo_usuario`, `usuario`, `password`) VALUES (NULL, %s, %s, %s, %s, %s, NULL, '1', %s,%s);  "

        datos = (_nombre, _apellido, _rut, _celular,
                 _correo, _usuario, _password)
        flash('Usuario creado correctamente.', "success")
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)
        conn.commit()
        pass
        return render_template('login.html')


@app.route('/editar/<int:id>')  # funcion editar
def editar(id):

    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    # verificar si la sentencia es exitosa
    cursor.execute("SELECT * FROM cliente WHERE id=%s", (id))
    cliente = cursor.fetchall()
    conn.commit()
    return render_template('actualizar.html', cliente=cliente)




@app.route('/update', methods=['POST'])  # funcion actualizar datos cliente
def update():
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _rut = request.form['txtRut']
    _celular = request.form['txtNumero']
    _correo = request.form['txtCorreo']
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']
    id = request.form['txtID']

    sql = "UPDATE cliente SET nombre = %s, apellido = %s, rut = %s, nro_celular = %s, correo_electronico = %s, id_tipo_usuario = '1', usuario = %s, password = %s WHERE id = %s; "
    datos = (_nombre, _apellido, _rut, _celular,
             _correo, _usuario, _password, id)
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(sql, datos)
    print(cursor)
    flash('Usuario modificado correctamente.', "success")

    conn.commit()
    return redirect('/listar_clientes')



#fin seccion cliente

#Seccion inventario

@app.route('/editar_inventario/<int:id>')
def editar_inventario(id):
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    # verificar si la sentencia es exitosa
    cursor.execute("SELECT * FROM inventario WHERE id=%s", (id))
    inventario = cursor.fetchall()
    conn.commit()
    return render_template("/editar_inventario", inventario=inventario)

@app.route('/inventario/<int:id>')
def inventario(id):
    sql = "SELECT * FROM `departamento` "
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    cursor.execute(sql)  # verificar si la sentencia es exitosa
    departamento = cursor.fetchall()
    print(departamento)
    cursor.execute("SELECT * FROM `inventario` WHERE `id_departamento` = %s", (id))  # verificar si la sentencia es exitosa
    inventario = cursor.fetchall()
    print(inventario)
    conn.commit()
    return render_template('inventario.html', departamento=departamento, inventario=inventario)

@app.route('/eliminar_inventario/<int:id>')  # funcion eliminar departamento
def eliminar_inventario(id):
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion

    cursor.execute("DELETE FROM inventario WHERE id=%s", (id))
    flash('Objeto eliminado correctamente del inventario.', "success")
    conn.commit()
    return redirect('/pag_admin')


@app.route('/update_inventario', methods=['POST'])  # funcion actualizar datos cliente
def update_inventario():
    _descripcion = request.form['txtDescripcion']
    _marca = request.form['txtMarca']
    _nro_serie = request.form['txtNro_serie']
    _valor = request.form['txtValor']
    id = request.form['txtID_I']

    sql = "UPDATE `inventario` SET `descripcion` = %s, `marca` = %s, `nro_serie` = %s, `valor` = %s WHERE `inventario`.`id` = %s; "
    datos = (_descripcion, _marca, _nro_serie, _valor, id)
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(sql, datos)
    print(cursor)
    flash('Inventario modificado correctamente.', "success")

    conn.commit()
    return redirect('/pag_admin')


@app.route('/registrar_inventario', methods=['POST'])
def registrar_inventario():

    _id_depto = request.form['txtid_depto']
    _descripcion = request.form['txtDesccripcion']
    _marca = request.form['txtMarca']
    _nro_serie = request.form['txtNro_serie']
    _valor = request.form['txtValor']
    sql = "INSERT INTO `inventario` (`id`, `descripcion`, `marca`, `nro_serie`, `valor`, `id_departamento`) VALUES (NULL, %s , %s,%s, %s, %s); "
    datos = (_descripcion, _marca, _nro_serie, _valor, _id_depto)
    flash('Inventario registrado registrado correctamente.', "success")
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    pass
    return redirect('/pag_admin')

#Fin seccion inventario

if __name__ == '__main__':
    app.run(debug=True)
