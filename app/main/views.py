from flask import render_template, session, redirect, url_for, request
from . import main
from ..models import Product, Category, Type
from .forms import ContactForm, HowManyProducts, SortingForm, ShippingForm, ReviewForm, DeliveryandPaymentForm
from app import db
import re


@main.route('/')
def index():
    #db.create_all()
    products = Product.query.all()
    return render_template('index.html', products=products)


@main.route('/thanks')
def thanks():
    return render_template('thanks.html')


@main.route('/product')
@main.route('/product/<int:id>')
def product(id):
    reviewForm = ReviewForm()
    product_info = Product.query.filter(Product.id == id).first_or_404()
    product_info.price = int(product_info.price)
    product_info.sizes = dict(product_info.sizes)
    return render_template('single-product.html', form=reviewForm, product=product_info)


@main.route('/shop')
@main.route('/shop/<int:page>')
def shop(page=1, items_per_page=1):
    form1 = HowManyProducts()
    form2 = SortingForm()
    categories = Category.query.all()
    products = Product.query.paginate(page, items_per_page, False)
    #if request.method == 'POST' and form1.validate():
     #   how_many = form1.data
    #    products = Product.query.paginate(page, how_many, False)
    types = Type.query.all()
    return render_template('shop.html', types=types, categories=categories, products=products, form1=form1, form2=form2)


@main.route('/shop', methods=['POST'])
@main.route('/shop/<int:page>', methods=['POST'])
def shop_forms(page=1, items_per_page=1):
    category = request.form['category']
    type = request.form['type']
    print(category)
    print(type)
    categories = Category.query.filter(Category.name == category).first()
    products = Product.query.paginate(page, items_per_page, False)
    #if request.method == 'POST' and form1.validate():
     #   how_many = form1.data
    #    products = Product.query.paginate(page, how_many, False)
    types = Type.query.all()
    return render_template('shop.html', types=types, categories=categories, products=products)


@main.route('/cart')
def cart():
    #product = Product.query.filter(Product.id == product_id).first()
    if 'cart' not in session:
        session['cart'] = []
        return render_template('shopping-cart.html', cart=session['cart'])
    else:
        #print(session)
        subtotal = 0
        product_names_prices = {}
        for item in session['cart']:
            id = list(item.keys())
            product = Product.query.filter(Product.id == int(id[0])).first()
            qty = list(item.values())
            product_names_prices.update({product.id: [product.name, int(product.price), qty[0]]})
            subtotal += int(product.price) * qty[0]
        print(session)
        return render_template('shopping-cart.html', products=product_names_prices, cart=session['cart'], subtotal=subtotal)


@main.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    product_id = int(request.form['product_id'])
    qty = int(request.form['quantity'])
    print(session)
    if 'cart' not in session:
        session['cart'] = []
    cart_list = session['cart']
    for item in cart_list:
        print(item)
        id = int(list(item.keys())[0])
        qty_was = list(item.values())[0]
        if id == product_id:
            item.update({str(id): qty_was+qty})
            break
    else:
        cart_list.append({product_id: qty})
    session['cart'] = cart_list
    #flash('Товар {0} успешно добавлен в корзину!', product.name)
    return redirect(url_for("main.shop"))


@main.route("/remove_from_cart", methods=['POST'])
def remove_from_cart():
    product_id = int(request.form['product_id'])
    cart_list = session['cart']
    for item in cart_list:
        print(item)
        id = int(list(item.keys())[0])
        print(id)
        if id == product_id:
            cart_list.remove(item)
    #cart_list.remove(product_id)
    session['cart'] = cart_list
    print(session)
    return redirect(url_for('main.cart'))


@main.route("/how_much", methods=['POST'])
def how_much():
    qty = int(request.form.get('quantity'))
    print(qty)
    product_id = int(request.form['product_id'])
    print(product_id)
    print(session)
    cart_list = session['cart']
    session['cart'] = cart_list
    print(session)
    return redirect(url_for('main.cart'))


@main.route('/contact')
def contact():
    form = ContactForm()
    return render_template('contact.html', form=form)


@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    formShip = ShippingForm()
    Deliveryform = DeliveryandPaymentForm()

    product_names_prices = {}
    subtotal = 0

    for item in session['cart']:
        print(item)
        id = list(item.keys())
        print(id)
        product = Product.query.filter(Product.id == int(id[0])).first()
        print(session)
        qty = list(item.values())
        product_names_prices.update({product.id: [product.name, int(product.price), qty[0], int(product.price*qty[0])]})
        subtotal += int(product.price)*qty[0]
    if request.method == 'POST' and Deliveryform.validate_on_submit():
        print('I LOVE MYSELF AND THIS CODE')
        return render_template('checkout.html')
    return render_template('checkout.html', form1=formShip, form2=Deliveryform, cart=session['cart'], products=product_names_prices, subtotal=subtotal)
