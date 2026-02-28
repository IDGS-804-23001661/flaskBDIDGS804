from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Alumnos(db.Model):
    __tablename__ = 'alumnos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

class Maestros(db.Model):
    __tablename__ = 'maestros'

    matricula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    especialidad = db.Column(db.String(50))
    email = db.Column(db.String(100))