import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Producto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Lista de productos a insertar desde el código (se sincroniza con la BD)
sample_products = [
    {
        "title": "Anillo de plata",
        "description": "Anillo ajustable de plata esterlina",
        "price": 150.00,
        "rating": 4.8,
        "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/main/anillo5.png"
    },
    {
        "title": "Collar dorado",
        "description": "Collar con dije de corazón chapado en oro",
        "price": 120.00,
        "rating": 4.6,
        "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/main/anillo5.png"
    },
    {
        "title": "Pulsera tejida",
        "description": "Pulsera artesanal ajustable con cuentas",
        "price": 80.00,
        "rating": 4.5,
        "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/main/anillo5.png"
    },
    {
        "title": "Aretes de perla",
        "description": "Aretes con perla blanca y broche de plata",
        "price": 95.00,
        "rating": 4.7,
        "thumbnail": ""
    }
]

# Función para insertar o actualizar productos
def insertar_productos():
    for p in sample_products:
        existente = Producto.query.filter_by(title=p["title"]).first()
        if existente:
            existente.description = p["description"]
            existente.price = p["price"]
            existente.rating = p["rating"]
            existente.thumbnail = p["thumbnail"]
        else:
            nuevo = Producto(**p)
            db.session.add(nuevo)
    db.session.commit()

# Inicialización de la base y carga de productos al iniciar
with app.app_context():
    db.create_all()
    insertar_productos()

@app.route('/')
def index():
    return "¡La API de productos está funcionando!"

@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify({"products": [p.to_dict() for p in productos]})

@app.route('/api/productos', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    nuevo = Producto(
        title=data['title'],
        description=data.get('description', ''),
        price=data['price'],
        rating=data.get('rating', 0.0),
        thumbnail=data.get('thumbnail', '')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
