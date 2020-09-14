from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    male = db.Column(db.Boolean, nullable=True)
    image = db.Column(db.String(32), nullable=True)
    score = db.Column(db.SmallInteger, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('types.id')) #TODO: поменять в базе данных наименование product_id на type_id
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    sizes = db.Column(db.String(64), nullable=True)
    colors = db.Column(db.String(256), nullable=True)


class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    products = db.relationship('Product', backref='type')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    products = db.relationship('Product', backref='category')


class Color:
    name = "default_color"
