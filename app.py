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

# render  las paginas


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


@app.route('/pag_cliente')
def pag_cliente():
    return render_template("pag_cliente.html")


@app.route('/pag_admin')
def pag_admin():
    return render_template("pag_admin.html")


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


@app.route('/registro_empleados')
def registro_empleados():
    return render_template('registrar_empleado.html')


@app.route('/departamentos')
def departamentos():
    return render_template('departamento.html')

# render de las paginas


@app.route('/login')
def loggear():
    return redirect("/inicio")


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


@app.route('/listar_empleados')  # listar empleados
def f_pag():
    sql = "SELECT * FROM `empleado` WHERE `id_tipo_usuario` = 2 ; "
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    cursor.execute(sql)  # verificar si la sentencia es exitosa
    empleado = cursor.fetchall()
    print(empleado)
    conn.commit()
    return render_template('listar_empleados.html', empleado=empleado)


# @app.route('/lista_departamento2')
# def lista_departamento2():
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
    return render_template('departamento.html', departamento=departamento, servicio_asociado=servicio_asociado)


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

    




@app.route('/listar_departamentos/<int:id>')
def listar_departamentos(id):
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    # verificar si la sentencia es exitosa
    cursor.execute("SELECT * FROM departamento WHERE id=%s", (id))
    departamento = cursor.fetchall()
    cursor.execute(
        "SELECT `id_servicio_asociado` FROM `departamento` WHERE id=%s", (id))
    servicio_A = cursor.fetchall()
    cursor.execute(
        "SELECT * FROM `servicio_asociado` WHERE id = %s;", (servicio_A))
    servicio_asociado = cursor.fetchall()
    cursor.execute(
        "SELECT * FROM `inventario` WHERE `id_departamento` = %s", (id))
    inventario = cursor.fetchall()
    print(inventario)
    return render_template('departamento.html', departamento=departamento, servicio_asociado=servicio_asociado, inventario=inventario)


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


@app.route('/eliminar/<int:id>')  # funcion eliminar
def eliminar(id):
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion

    cursor.execute("DELETE FROM cliente WHERE id=%s", (id))
    flash('Usuario eliminado correctamente.', "success")
    conn.commit()
    return redirect('/listar_clientes')


@app.route('/eliminarEmp/<int:id>')  # funcion eliminar empleado
def eliminarEmp(id):
    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion

    cursor.execute("DELETE FROM empleado WHERE id=%s", (id))
    flash('Empleado eliminado correctamente.', "success")
    conn.commit()
    return redirect('/listar_empleados')


@app.route('/editar/<int:id>')  # funcion editar
def editar(id):

    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    # verificar si la sentencia es exitosa
    cursor.execute("SELECT * FROM cliente WHERE id=%s", (id))
    cliente = cursor.fetchall()
    conn.commit()
    return render_template('actualizar.html', cliente=cliente)


@app.route('/editarEmp/<int:id>')  # funcion editar empleado
def editarEmp(id):

    conn = mysql.connect()  # conectarse a la base de datos
    cursor = conn.cursor()  # almacenar informacion
    # verificar si la sentencia es exitosa
    cursor.execute("SELECT * FROM empleado WHERE id=%s", (id))
    empleado = cursor.fetchall()
    conn.commit()
    return render_template('editar_empleado.html', empleado=empleado)


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


if __name__ == '__main__':
    app.run(debug=True)
