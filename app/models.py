from app import db


class Color(db.Model):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)


class Size(db.Model):
    __tablename__ = 'sizes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)


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
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    fandom_id = db.Column(db.Integer, db.ForeignKey('fandom.id'))
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'))
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'))
    product_id = db.Column(db.Integer)


class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    products = db.relationship('Product', backref='type')


class Fandom(db.Model):
    __tablename__ = 'fandom'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    products = db.relationship('Product', backref='category')


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    name = db.Column(db.String(32))
    date = db.Column(db.Date)
    comment = db.Column(db.String(500))
    rating = db.Column(db.Integer)
