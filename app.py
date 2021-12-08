from flask import Flask
from flask import render_template, request, redirect, url_for
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'si'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA']= CARPETA

@app.route('/')
def index():
    sql = "SELECT * FROM `bebidas`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    bebidas = cursor.fetchall()

    conn.commit()

    sql2 = "SELECT * FROM `botana`;"
    conn2 = mysql.connect()
    cursor2 = conn.cursor()
    cursor2.execute(sql2)

    botanas = cursor2.fetchall()

    conn2.commit()
    

    return render_template('Bebidas/index.html', bebidas=bebidas, botanas=botanas)

@app.route('/createbebidas')
def createbebidas():
    return render_template('Bebidas/create.html')

@app.route('/createbotanas')
def createbotanas():
    return render_template('botana/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtdescripcion']
    _tipo = request.form['listtipo']
    _cantidad = request.form['txtcantidad']
    _precio = request.form['txtprecio']
    _imagen = request.files['txtFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _imagen.filename != '':
        nuevoNombre = tiempo + _imagen.filename
        _imagen.save("uploads/"+nuevoNombre)

    sql = "insert into `bebidas` (`Id`, `Nombre`, `Descripcion`, `Tipo`, `Cantidad`, `Precio`, `Imagen`) VALUES(NULL, %s, %s, %s, %s, %s, %s);"
    datos = (_nombre, _descripcion,_tipo,_cantidad,_precio, nuevoNombre)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')

@app.route('/store2', methods=['POST'])
def storage2():
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtdescripcion']
    _precio = request.form['txtprecio']
    _imagen = request.files['txtFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _imagen.filename != '':
        nuevoNombre = tiempo + _imagen.filename
        _imagen.save("uploads/"+nuevoNombre)

    sql = "insert into `botana` (`Id`, `Nombre`, `Descripcion`, `Precio`, `Imagen`) VALUES(NULL, %s, %s, %s, %s);"
    datos = (_nombre, _descripcion,_precio, nuevoNombre)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')

@app.route('/destroybebidas/<int:id>')
def destroybebidas(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT Imagen FROM bebidas WHERE Id=%s", (id))
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM bebidas WHERE id=%s", (id))
    conn.commit()
    return redirect('/')

@app.route('/destroybotana/<int:id>')
def destroybotana(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT Imagen FROM botana WHERE Id=%s", (id))
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM botana WHERE Id=%s", (id))
    conn.commit()
    return redirect('/')

@app.route('/editbebidas/<int:id>')
def editbebidas(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bebidas WHERE id=%s", (id))
    bebidas = cursor.fetchall()
    conn.commit()
    return render_template('bebidas/edit.html', bebidas=bebidas)

@app.route('/editbotana/<int:id>')
def editbotana(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM botana WHERE Id=%s", (id))
    botanas = cursor.fetchall()
    conn.commit()
    return render_template('botana/edit.html', botanas=botanas)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtdescripcion']
    _tipo = request.form['listtipo']
    _cantidad = request.form['txtcantidad']
    _precio = request.form['txtprecio']

    _foto = request.files['txtFoto']
    id = request.form['txtID']

    sql = "UPDATE bebidas SET Nombre=%s, Descripcion=%s, Tipo=%s, Cantidad=%s, Precio=%s WHERE Id=%s;"

    datos = (_nombre, _descripcion, _tipo, _cantidad, _precio, id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    now = datetime.now()
    hora = now.strftime("%Y%H%M%S")

    if _foto.filename !='':
        nuevoNombre = hora + _foto.filename
        _foto.save('uploads/'+nuevoNombre)
        cursor.execute("SELECT Imagen FROM bebidas WHERE Id=%s", id)
        fila = cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE bebidas SET Imagen=%s WHERE Id=%s", (nuevoNombre, id))
        conn.commit()

    return redirect('/')

@app.route('/updatebotana', methods=['POST'])
def updatebotana():
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtdescripcion']
    _precio = request.form['txtprecio']

    _foto = request.files['txtFoto']
    id = request.form['txtID']

    sql = "UPDATE botana SET Nombre=%s, Precio=%s, Descripcion=%s WHERE Id=%s;"

    datos = (_nombre, _precio, _descripcion, id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    now = datetime.now()
    hora = now.strftime("%Y%H%M%S")

    if _foto.filename !='':
        nuevoNombre = hora + _foto.filename
        _foto.save('uploads/'+nuevoNombre)
        cursor.execute("SELECT Imagen FROM botana WHERE Id=%s", id)
        fila = cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE botana SET Imagen=%s WHERE Id=%s", (nuevoNombre, id))
        conn.commit()

    return redirect('/')

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

if __name__ == '__main__':
    app.run(debug=True)