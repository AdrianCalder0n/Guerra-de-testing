import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, UserMixin, login_required, login_user,
                         logout_user)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave secreta segura
login_manager = LoginManager(app)


# Configuración de la conexión a la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Usuario de MySQL
app.config['MYSQL_PASSWORD'] = ''  # Contraseña de MySQL
app.config['MYSQL_DB'] = 'inventario'  # Nombre de la base de datos


# Función para conectar a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )


# Conjunto para almacenar mensajes flash
flash_messages = set()

# Clase de ejemplo para un producto
class Product:
    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

@app.route('/productos')
@login_required
def productos():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM productos')
    products = []
    for (id, nombre, precio, stock) in cursor:
        product = Product(id, nombre, precio, stock)
        products.append(product)
    cursor.close()
    db.close()
    return render_template('productos.html', products=products)


# Rutas para agregar, sacar, editar y eliminar productos
@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)', (name, price, stock))
    db.commit()
    cursor.close()
    db.close()
    flash('Producto agregado correctamente.', 'success')
    return redirect(url_for('productos'))

@app.route('/remove_product/<int:product_id>', methods=['GET'])
@login_required
def remove_product(product_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('DELETE FROM productos WHERE id = %s', (product_id,))
    db.commit()
    cursor.close()
    db.close()
    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('productos'))


@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = %s', (product_id,))
    product_data = cursor.fetchone()
    cursor.close()
    db.close()

    if product_data:
        product = Product(product_data[0], product_data[1], product_data[2], product_data[3])
        if request.method == 'POST':
            # Procesar los datos del formulario para editar el producto
            name = request.form['name']
            price = float(request.form['price'])
            stock = int(request.form['stock'])
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute('UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id = %s', (name, price, stock, product_id))
            db.commit()
            cursor.close()
            db.close()
            flash('Producto editado correctamente.', 'success')
            return redirect(url_for('productos'))
        else:
            # Mostrar el formulario prellenado para editar el producto
            return render_template('editar_producto.html', product=product)
    else:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('productos'))


# Clase de ejemplo para un usuario
class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password

# Lista de usuarios de ejemplo
users = {'root': User('root', 'root')}

@login_manager.user_loader
def load_user(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuarios WHERE username = %s', (user_id,))
    user_data = cursor.fetchone()  # Leer los resultados de la consulta
    cursor.close()
    db.close()

    if user_data:
        return User(user_data['username'], user_data['password'])
    else:
        return None



@app.route('/', methods=['GET', 'POST'])
def index():
    # Limpiar el conjunto de mensajes flash al inicio de cada solicitud
    flash_messages.clear()
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE username = %s', (username,))
        user_data = cursor.fetchone()
        cursor.close()
        db.close()

        if user_data and user_data['password'] == password:
            user = User(user_data['username'], user_data['password'])
            login_user(user)
            return redirect(url_for('productos'))  # Redirigir a la página de productos
            
        flash('Nombre de usuario o contraseña incorrectos', 'error')
        return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/agregar_producto')
@login_required
def agregar_producto():
    return render_template('agregar_producto.html')

if __name__ == '__main__':
    app.run(debug=True)