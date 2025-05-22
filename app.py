import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Producto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Usando SQLite para el ejemplo
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Crear productos de ejemplo si no existen
def insertar_productos():
    if Producto.query.first():
        return  # Ya existen productos
    productos_demo = [
        {
            "nombre": "Cuaderno profesional",
            "descripcion": "Cuaderno de 100 hojas, rayado",
            "precio": 25.50,
            "rating": 4.7,
            "imagen": "https://raw.githubusercontent.com/Angel-Perez-1086/imagenes_github/main/pack%20lapiz.jpg"
        },
        {
            "nombre": "Bolígrafos azul (pack x10)",
            "descripcion": "Bolígrafos de tinta azul, punta fina",
            "precio": 40.00,
            "rating": 4.3,
            "imagen": "https://raw.githubusercontent.com/Angel-Perez-1086/imagenes_github/main/pack%20lapiz.jpg"
        },
        # Agrega más productos si lo deseas
    ]

    for p in productos_demo:
        db.session.add(Producto(**p))
    db.session.commit()

# Crear la base de datos y cargar productos de ejemplo
with app.app_context():
    db.create_all()
    insertar_productos()

# Ruta raíz
@app.route('/')
def index():
    return "¡La API de productos está funcionando!"

# Ruta para obtener productos
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify([p.to_dict() for p in productos])

# Ruta para agregar un nuevo producto
@app.route('/api/productos', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    nuevo = Producto(
        nombre=data['nombre'],
        descripcion=data.get('descripcion', ''),
        precio=data['precio'],
        rating=data.get('rating', 0.0),
        imagen=data.get('imagen', '')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201

# Configuración del puerto y host
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
