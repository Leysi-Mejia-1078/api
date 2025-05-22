import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Usando SQLite para el ejemplo
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    "title": "Anillo de compromiso de oro blanco",
    "description": "Anillo de oro blanco con diamante central",
    "price": 1500.00,
    "rating": 4.8,
    "thumbnail": ""
  },
  {
    "title": "Collar de perlas",
    "description": "Collar de perlas naturales con cierre de plata",
    "price": 350.00,
    "rating": 4.7,
    "thumbnail": ""
  },
  {
    "title": "Pendientes de plata con esmeraldas",
    "description": "Pendientes de plata 925 con esmeraldas verdes",
    "price": 220.00,
    "rating": 4.5,
    "thumbnail": ""
  },
  {
    "title": "Pulsera de cuero y acero inoxidable",
    "description": "Pulsera unisex de cuero trenzado con detalles de acero inoxidable",
    "price": 45.00,
    "rating": 4.4,
    "thumbnail": ""
  },
  {
    "title": "Anillo de plata con zirconia",
    "description": "Anillo de plata con zirconia cúbica en forma de corazón",
    "price": 75.00,
    "rating": 4.6,
    "thumbnail": ""
  },
  {
    "title": "Brazalete de oro rosa",
    "description": "Brazalete delicado de oro rosa con diseño minimalista",
    "price": 250.00,
    "rating": 4.9,
    "thumbnail": ""
  },
  {
    "title": "Reloj de pulsera de lujo",
    "description": "Reloj de pulsera de lujo con correa de cuero negro y esfera de acero",
    "price": 1200.00,
    "rating": 4.7,
    "thumbnail": ""
  },
  {
    "title": "Anillo de oro con rubí",
    "description": "Anillo de oro amarillo con rubí ovalado central",
    "price": 950.00,
    "rating": 4.8,
    "thumbnail": ""
  }
]

    for p in sample_products:
        db.session.add(Producto(**p))
    db.session.commit()

# Crear la base de datos y cargar productos de ejemplo
with app.app_context():
    db.create_all()
    insert_sample_products()

# Ruta raíz
@app.route('/')
def index():
    return "Product API is running!"

# Ruta para obtener productos
@app.route('/api/products', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify({"products": [p.to_dict() for p in productos]})
# Ruta para agregar un nuevo producto
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Producto(
        title=data['title'],
        description=data.get('description', ''),
        price=data['price'],
        rating=data.get('rating', 0.0),
        thumbnail=data.get('thumbnail', '')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

# Configuración del puerto y host
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
