from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app=Flask(__name__)

mysql=MySQL()

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_PORT']=3306
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='dbcrud'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/clientes')
def index_clientes():

    sql='SELECT * FROM clientes'

    conexion=mysql.connection
    cursor=conexion.cursor()
    cursor.execute(sql)
    clientes=cursor.fetchall()
    conexion.commit()
    return render_template('modulos/clientes/index.html', clientes=clientes)

@app.route('/clientes/create')
def reate():
    return render_template('modulos/clientes/create.html')

@app.route('/clientes/create/guardar', methods=['POST'])
def clientes_guardar():
    nombre=request.form['nombre']
    telefono=request.form['telefono']
    fecha=request.form['fecha']
    
    sql='INSERT INTO clientes(nombre, telefono, fecha) VALUES(%s, %s, %s)'
    datos=(nombre, telefono, fecha)
    conexion=mysql.connection
    cursor=conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect('/clientes')

@app.route('/clientes/edit/<int:id>')
def clientes_editar(id):
    conexion=mysql.connection
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id=%s",(id,))
    clientes=cursor.fetchone()
    conexion.commit()
    return render_template('modulos/clientes/edit.html',clientes=clientes)

@app.route('/clientes/edit/actualizar', methods=['POST'])
def clientes_actualizar():
    id=request.form['txtid']
    nombre=request.form['nombre']
    telefono=request.form['telefono']
    fecha=request.form['fecha']

    sql="UPDATE clientes SET nombre=%s, telefono=%s, fecha=%s WHERE id=%s"
    datos=(nombre, telefono, fecha, id)
    
    conexion=mysql.connection
    cursor=conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect('/clientes')

@app.route('/clientes/borrar/<int:id>')
def clientes_borrar(id):
    conexion=mysql.connection
    cursor=conexion.cursor()
    cursor.execute('DELETE FROM clientes WHERE id=%s',(id,))
    conexion.commit()
    return redirect('/clientes')

if __name__ == '__main__':
    app.run(debug=True)
