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
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    rating = db.Column(db.Float)
    image = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "rating": self.rating,
            "image": self.image
        }

# Crear productos de ejemplo si no existen
def insert_sample_products():
    if Producto.query.first():
        return  # Ya existen productos
    sample_products = [
        {
            "name": "Professional Notebook",
            "description": "100-page lined notebook",
            "price": 25.50,
            "rating": 4.7,
            "image": "https://raw.githubusercontent.com/Angel-Perez-1086/imagenes_github/main/pack%20lapiz.jpg"
        },
        {
            "name": "Blue Pens (pack of 10)",
            "description": "Blue ink pens, fine tip",
            "price": 40.00,
            "rating": 4.3,
            "image": "https://raw.githubusercontent.com/Angel-Perez-1086/imagenes_github/main/pack%20lapiz.jpg"
        },
        # Agrega más productos si lo deseas
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
def get_products():
    products = Producto.query.all()
    return jsonify({"products": [p.to_dict() for p in products]})

# Ruta para agregar un nuevo producto
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Producto(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        rating=data.get('rating', 0.0),
        image=data.get('image', '')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

# Configuración del puerto y host
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
