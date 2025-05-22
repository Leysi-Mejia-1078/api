from flask import Flask, request, jsonify
from models import db, Producto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

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
        {
            "nombre": "Bolígrafos azul (pack x10)",
            "descripcion": "Bolígrafos de tinta azul, punta fina",
            "precio": 40.00,
            "rating": 4.3,
            "imagen": "/static/boligrafos.jpg"
        },
        {
            "nombre": "Marcadores fluorescentes",
            "descripcion": "Set de 6 marcadores de colores neón",
            "precio": 65.00,
            "rating": 4.6,
            "imagen": "/static/marcadores.jpg"
        },
        {
            "nombre": "Regla 30cm",
            "descripcion": "Regla de plástico transparente",
            "precio": 10.00,
            "rating": 4.2,
            "imagen": "/static/regla.jpg"
        },
        {
            "nombre": "Goma de borrar",
            "descripcion": "Goma blanca para lápiz",
            "precio": 5.00,
            "rating": 4.5,
            "imagen": "/static/goma.jpg"
        },
        {
            "nombre": "Lápices (pack x12)",
            "descripcion": "Lápices de madera HB con goma",
            "precio": 30.00,
            "rating": 4.4,
            "imagen": "/static/lapices.jpg"
        },
        {
            "nombre": "Tijeras escolares",
            "descripcion": "Tijeras de punta redonda para niños",
            "precio": 15.00,
            "rating": 4.1,
            "imagen": "/static/tijeras.jpg"
        },
        {
            "nombre": "Pritt barra adhesiva",
            "descripcion": "Pegamento en barra no tóxico",
            "precio": 18.50,
            "rating": 4.3,
            "imagen": "/static/pritt.jpg"
        },
        {
            "nombre": "Cartulina blanca",
            "descripcion": "Cartulina tamaño carta, paquete x10",
            "precio": 22.00,
            "rating": 4.6,
            "imagen": "/static/cartulina.jpg"
        }
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
    app.run(debug=True, host='0.0.0.0', port=5000)

