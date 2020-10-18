from app import db


class Item(db.Model):
    __tablename__ = 'lots'
    id = db.Column(db.Integer, primary_key=True)
    product_info_id = db.Column(db.Integer, db.ForeignKey('products_info.id'))
    quantity = db.Column(db.Integer, nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'))
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'))


class Product(db.Model):
    __tablename__ = 'products_info'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    product_name = db.Column(db.String(64), unique=True)
    image_link = db.Column(db.String(32), nullable=True)
    score = db.Column(db.SmallInteger, nullable=True)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    fandom_id = db.Column(db.Integer, db.ForeignKey('fandom.id'))


class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    products = db.relationship('Product', backref='type')


class Fandom(db.Model):
    __tablename__ = 'fandom'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    products = db.relationship('Product', backref='fandom')


class Color(db.Model):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)


class Size(db.Model):
    __tablename__ = 'sizes'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(64), unique=True, nullable=False)


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    name = db.Column(db.String(32))
    date = db.Column(db.Date)
    comment = db.Column(db.String(500))
    rating = db.Column(db.Integer)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    mail = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)


class ProductInfo:
    product_info_id = 0
    size_id = 0
    color_id = 0


