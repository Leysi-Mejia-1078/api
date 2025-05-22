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
        "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/main/anillo5.png"
    }
]

# Función para insertar o actualizar productos
def insertar_productos():
=======
# Modelo de Producto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    rating = db.Column(db.Float)
    thumbnail = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "rating": self.rating,
            "thumbnail": self.thumbnail
        }

# Crear productos de ejemplo si no existen
def insert_sample_products():
    if Producto.query.first():
        return  # Ya existen productos
    sample_products = sample_products = [
  {
    "title": "Anillo de oro",
    "description": "Anillo elegante de oro de 18 quilates.",
    "price": 250.00,
    "rating": 4.8,
    "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/main/anillo5.png"
  },
  {
    "title": "Collar de perlas",
    "description": "Collar de perlas de alta calidad.",
    "price": 150.00,
    "rating": 4.5,
    "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/main/anillo5.png"
  },
  {
    "title": "Pulsera de plata",
    "description": "Pulsera de plata fina con diseño moderno.",
    "price": 90.00,
    "rating": 4.6,
    "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/main/anillo5.png"
  },
  {
    "title": "Reloj de lujo",
    "description": "Reloj de lujo con correa de cuero.",
    "price": 300.00,
    "rating": 4.9,
    "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/main/anillo5.png"
  },
  {
    "title": "Aretes de diamantes",
    "description": "Aretes de diamantes brillantes y elegantes.",
    "price": 500.00,
    "rating": 5.0,
    "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/main/anillo5.png"
  },
  {
    "title": "Anillo de plata",
    "description": "Anillo de plata con diseño único.",
    "price": 120.00,
    "rating": 4.7,
    "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/main/anillo5.png"
  },
  {
    "title": "Cadenas de oro",
    "description": "Cadenas de oro 24 quilates, ideales para cualquier ocasión.",
    "price": 400.00,
    "rating": 4.8,
    "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/main/anillo5.png"
  },
  {
    "title": "Brazalete de acero",
    "description": "Brazalete de acero inoxidable con diseño minimalista.",
    "price": 70.00,
    "rating": 4.4,
    "thumbnail": "https://raw.githubusercontent.com/Leysi-Mejia-1078/imagenes/main/anillo5.png"
  }
]


>>>>>>> 272fc3d65b433cb03b3aa6001cfb7de640a7b4b8
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
<<<<<<< HEAD

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
=======
# Ruta para agregar un nuevo producto
@app.route('/api/products', methods=['POST'])
def add_product():
    for p in sample_products:
        existente = Producto.query.filter_by(title=p["title"]).first()
        if existente:
            # Actualiza campos si el producto ya existe
            existente.description = p["description"]
            existente.price = p["price"]
            existente.rating = p["rating"]
            existente.thumbnail = p["thumbnail"]
        else:
            # Inserta nuevo si no existe
            nuevo = Producto(**p)
            db.session.add(nuevo)
>>>>>>> 272fc3d65b433cb03b3aa6001cfb7de640a7b4b8
    db.session.commit()
    return jsonify(nuevo.to_dict()), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
