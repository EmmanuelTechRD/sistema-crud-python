from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_PORT'] = 3308
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema_crud_python'
mysql.init_app(app)

@app.route('/')
def index():

    sql = "INSERT INTO `empleados` (`id`, `nombre`, `telefono`, `correo`, `cedula`, `fecha_de_nacimiento`) VALUES (NULL, 'Emmanuel', '1-829-555-1111', 'enicolassotop@gmail.com', '001-2345678-9', '01 de Enero del 1234');"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    return render_template('empleados/index.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)