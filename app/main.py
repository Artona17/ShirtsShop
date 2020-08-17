import os

from flask import Flask, render_template, redirect
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
manager = Manager(app)


# noinspection PyUnresolvedReferences
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
    product_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


# noinspection PyUnresolvedReferences
class Type(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    products = db.relationship('Product', backref='type')


# noinspection PyUnresolvedReferences
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    products = db.relationship('Product', backref='category')


@app.route('/')
def index():
    #db.create_all()
    return render_template('index.html')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/shop')
def shop():
    categories = Category.query.all()
    products = Product.query.all()
    types = Type.query.all()
    return render_template('shop.html', types=types, categories=categories, products=products)


@app.route('/profile')
def my_account():
    return redirect('/')


@app.route('/cart')
def cart():
    return redirect('/')


@app.route('/contact')
def contact():
    return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if '__main__' == __name__:
    app.run(debug=True)
    manager.run()
