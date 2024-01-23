from flask import Flask, url_for
from flask import render_template, request, redirect, flash
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key="EmmanuelX1"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_PORT'] = 3308
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema_crud_python'
mysql.init_app(app)

@app.route('/')
def index():

    sql = "SELECT * FROM `empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    empleados = cursor.fetchall()
    print(empleados)

    conn.commit()

    return render_template('empleados/index.html', empleados = empleados)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM `empleados` WHERE `empleados`.`id` = %s;", id)
    conn.commit()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `empleados` WHERE `empleados`.`id` = %s;", id)
    empleados = cursor.fetchall()
    conn.commit()

    return render_template('empleados/edit.html', empleados = empleados)

@app.route('/actualizar', methods=['POST'])
def actualizar():

    _nombre = request.form['txtNombre']
    _telefono = request.form['txtTelefono']
    _correo = request.form['txtCorreo']
    _cedula = request.form['txtCedula']
    _fecha_de_nacimiento = request.form['txtFechadeNacimiento']
    _id = request.form['txtID']

    sql = "UPDATE `empleados` SET `nombre` = %s, `telefono` = %s, `correo` = %s, `cedula` = %s, `fecha_de_nacimiento` = %s WHERE `empleados`.`id` = %s;"

    datos = (_nombre, _telefono, _correo, _cedula, _fecha_de_nacimiento, _id)

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/crear')
def create():

    return render_template('empleados/create.html')

@app.route('/almacenar', methods=['POST'])
def storage():

    _nombre = request.form['txtNombre']
    _telefono = request.form['txtTelefono']
    _correo = request.form['txtCorreo']
    _cedula = request.form['txtCedula']
    _fecha_de_nacimiento = request.form['txtFechadeNacimiento']

    if _nombre == '' or _telefono == '' or _correo == '' or _cedula == '' or _fecha_de_nacimiento == '':
        flash('Para agregar un empleado exitosamente, recuerda llenar todos los campos.')
        return redirect(url_for('create'))

    sql = "INSERT INTO `empleados` (`id`, `nombre`, `telefono`, `correo`, `cedula`, `fecha_de_nacimiento`) VALUES (NULL, %s, %s, %s, %s, %s);"
    datos = (_nombre, _telefono, _correo, _cedula, _fecha_de_nacimiento)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return render_template('empleados/create.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)