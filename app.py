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
        "title": "Anillo Princesa Zafiro Celeste",
        "description": "Este elegante anillo presenta un deslumbrante zafiro azul genuino de corte princesa como pieza central.",
        "price": 45000.00,
        "rating": 4.8,
        "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/refs/heads/main/anillo.jpg"
    },
    {
        "title": "Arracadas "Dorado Chic"",
        "description": "Su forma redondeada y voluminosa los convierte en una pieza llamativa, perfecta para añadir un toque de glamour a cualquier atuendo.",
        "price": 5,000.00,
        "rating": 4.6,
        "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/refs/heads/main/aretes.jpg"
    },
    {
        "title": "Brazalete "Luz de Aurora"",
        "description": "Pulsera artesanal ajustable con cuentas",
        "price": 8000.00,
        "rating": 4.5,
        "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/refs/heads/main/pulsera.jpg"
    },
    {
        "title": "Collar "Círculo Eterno de Luz"",
        "description": "Este delicado collar presenta una cadena fina de oro de 14k que sostiene un encantador colgante en forma de círculo.",
        "price": 7500.00,
        "rating": 4.7,
        "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/refs/heads/main/collar2.jpg"
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
