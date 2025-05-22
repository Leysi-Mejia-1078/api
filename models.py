from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(250))
    precio = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    imagen = db.Column(db.String(250))  # URL o ruta a imagen

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "rating": self.rating,
            "imagen": self.imagen
        }
