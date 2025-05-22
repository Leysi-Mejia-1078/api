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
    sample_products = [
  {
    "title": "Lápices HB (paquete de 12)",
    "description": "Lápices de grafito con borrador",
    "price": 30.00,
    "rating": 4.4,
    "thumbnail": "https://raw.githubusercontent.com/Angel-Perez-1086/imagenes_github/main/pack%20lapiz.jpg"
  },
  {
    "title": "Marcatextos fluorescentes",
    "description": "Set de 6 colores neón",
    "price": 65.00,
    "rating": 4.6,
    "thumbnail": "https://raw.githubusercontent.com/Angel-Perez-1086/imagenes_github/main/marcatextos.jpg"
  },
  {
    "title": "Regla plástica 30 cm",
    "description": "Regla transparente de plástico",
    "price": 10.00,
    "rating": 4.2,
    "thumbnail": "https://raw.githubusercontent.com/Angel-Perez-1086/imagenes_github/main/regla.jpg"
  },
  {
    "title": "Borrador blanco",
    "description": "Borrador suave para lápiz",
    "price": 5.00,
    "rating": 4.5,
    "thumbnail": "https://raw.githubusercontent.com/Angel-Perez-1086/imagenes_github/main/borrador.jpg"
  },
  {
    "title": "Tijeras escolares",
    "description": "Tijeras de punta redonda para niños",
    "price": 15.00,
    "rating": 4.1,
    "thumbnail": "https://raw.githubusercontent.com/Angel-Perez-1086/imagenes_github/main/tijeras.jpg"
  },
  {
    "title": "Pegamento en barra",
    "description": "Pegamento no tóxico, fácil de usar",
    "price": 18.50,
    "rating": 4.3,
    "thumbnail": "https://raw.githubusercontent.com/Angel-Perez-1086/imagenes_github/main/pegamento.jpg"
  },
  {
    "title": "Cartulina blanca",
    "description": "Cartulina tamaño carta (paquete de 10)",
    "price": 22.00,
    "rating": 4.6,
    "thumbnail": "https://raw.githubusercontent.com/Angel-Perez-1086/imagenes_github/main/cartulina.jpg"
  },
  {
    "title": "Notas adhesivas",
    "description": "Notas amarillas (paquete de 3 bloques)",
    "price": 12.00,
    "rating": 4.4,
    "thumbnail": "https://raw.githubusercontent.com/Angel-Perez-1086/imagenes_github/main/notas.jpg"
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
