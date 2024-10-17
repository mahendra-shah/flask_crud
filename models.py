from flask_sqlalchemy import SQLAlchemy
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f'<Product {self.name}>'

