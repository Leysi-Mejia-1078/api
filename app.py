from flask import Flask, request, jsonify
from models import db, Producto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

# Ruta raíz
@app.route('/')
def home():
    return '¡La API de productos está funcionando!'

# Crear productos de ejemplo
def insertar_productos():
    if Producto.query.first():
        return  # Ya existen productos
    productos_demo = [
        {
            "nombre": "Cuaderno profesional",
            "descripcion": "Cuaderno de 100 hojas, rayado",
            "precio": 25.50,
            "rating": 4.7,
            "imagen": "/static/cuaderno.jpg"
        },
        # Otros productos aquí...
    ]

    for p in productos_demo:
        db.session.add(Producto(**p))
    db.session.commit()

# Crear la base de datos y cargar productos
with app.app_context():
    db.create_all()
    insertar_productos()

# Obtener todos los productos
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify([p.to_dict() for p in productos])

# Agregar nuevo producto
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

if __name__ == '__main__':
    app.run(debug=True)

