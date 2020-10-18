from flask import render_template, session, redirect, url_for, request
from . import main
from ..models import Product, Fandom, Type
from .forms import ContactForm, HowManyProducts, SortingForm, ShippingForm, ReviewForm, DeliveryandPaymentForm, SelectSizeandColorForm
import json


@main.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@main.route('/product')
@main.route('/product/<int:product_id>')
def product(product_id):
    review_form = ReviewForm()
    product_info = Product.query.filter(Product.id == product_id).first_or_404() #изменить на Product.product_id == id.all()
    product_info.price = int(product_info.price)
    session['url'] = request.path
    sizes = []
    colors = []
    if product_info.size_id: #здесь
        sizes.append(product_info.size_id)
    else:
        sizes = []
    if product_info.color_id: #здесь
        colors.append(product_info.color_id)
    else:
        colors = []
    if not review_form.validate():
        print(review_form.errors)
        #now = datetime.datetime.now()
        #review = Review(product_id=id, date=now.strftime("%d-%m-%Y"), name=review_form.name.data, comment=review_form.enquiry.data, rating=review_form.rating.data)
        #db.session.add(review)
        #print(db.session)
    return render_template('single-product.html', form=review_form, product=product_info, sizes=sizes, colors=colors)


@main.route('/shop', methods=['GET', 'POST'])
@main.route('/shop/<int:page>', methods=['GET', 'POST'])
def shop(page=1, items_per_page=3):
    howManyProducts_form = HowManyProducts()
    sorting_form = SortingForm()

    types = Type.query.all()
    fandoms = Fandom.query.all()
    session['url'] = request.path
    if request.method == 'POST':
        fandoms_info = fandoms
        types_info = types

        checked_fandoms = request.form.getlist('fandom')
        if checked_fandoms:
            fandoms_info = Fandom.query.filter(Fandom.name.in_(checked_fandoms)).all()

        checked_types = request.form.getlist('type')
        if checked_types:
            types_info = Type.query.filter(Type.name.in_(checked_types)).all()

        print(types_info)
        print(fandoms_info)

        products_by_types_ids = list()
        products_by_fandoms_ids = list()

        for type_info in types_info:
            for item in type_info.products:
                products_by_types_ids.append(item.id)

        for fandom_info in fandoms_info:
            for item in fandom_info.products:
                products_by_fandoms_ids.append(item.id)

        products_ids = list(set(products_by_types_ids) & set(products_by_fandoms_ids))

        if len(products_ids) < items_per_page:
            page = 0

        print(products_ids)
        products = Product.query.dictinct(Product.name).filter(Product.id.in_(products_ids)).paginate(page, items_per_page, False) #здесь
        print(products)
    else:
        products = Product.query\
            .paginate(page, items_per_page, False)

    return render_template('shop.html', types=types, fandoms=fandoms, products=products,
                           form1=howManyProducts_form, form2=sorting_form)


@main.route('/cart')
def cart():
    form = SelectSizeandColorForm()
    if 'cart' not in session:
        session['cart'] = []
        return render_template('shopping-cart.html', cart=session['cart'])
    else:
        subtotal = 0
        product_names_prices = {}
        for item in session['cart']:
            id = list(item.keys())
            product = Product.query.filter(Product.id == int(id[0])).first() #(Product.product_id==int(id[0])).all()
            qty = list(item.values())
            product_names_prices.update({product.id: [product.name, int(product.price), qty[0]]})
            subtotal += int(product.price) * qty[0]
        print(session)
        return render_template('shopping-cart.html', products=product_names_prices, cart=session['cart'],
                               subtotal=subtotal)


@main.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    product_id = int(request.form['product_id'])
    if request.form['quantity'] == '#qtybutton.value':
        qty = 1
    else:
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
            item.update({str(id): qty_was + qty})
            break
    else:
        cart_list.append({product_id: qty})
    session['cart'] = cart_list
    # flash('Товар {0} успешно добавлен в корзину!', product.name)
    return redirect(session['url'])


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
    Deliveryform = DeliveryandPaymentForm(request.form)

    product_names_prices = {}
    subtotal = 0

    for item in session['cart']:
        id = list(item.keys())
        product = Product.query.filter(Product.id == int(id[0])).first() #(Product.product_id==int(id[0])).all()
        qty = list(item.values())
        product_names_prices.update({product.id: [product.name, int(product.price), qty[0], int(product.price * qty[0])]})
        subtotal += int(product.price) * qty[0]

    if Deliveryform.validate_on_submit():
        session['deliverychoice'] = Deliveryform.deliverychoice.data
        session['paymentchoice'] = Deliveryform.paymentchoice.data
        return redirect(url_for('main.name_address'))
    return render_template('checkout.html', form=Deliveryform, cart=session['cart'],
                           products=product_names_prices, subtotal=subtotal)


@main.route('/shipping', methods=['GET', 'POST'])
def name_address():
    formShip = ShippingForm()

    DELIVERYPRICE = {"Самовывоз": 0, "Почтой": 250, "Курьером": 350}
    product_names_prices = {}
    subtotal = 0

    for item in session['cart']:
        id = list(item.keys())
        product = Product.query.filter(Product.id == int(id[0])).first() #(Product.product_id==int(id[0])).all()
        qty = list(item.values())
        product_names_prices.update({product.id: [product.name, int(product.price), qty[0], int(product.price * qty[0])]})
        subtotal += int(product.price) * qty[0]

    if formShip.validate_on_submit():
        return redirect(url_for('main.thanks'))

    return render_template('name_address.html', form=formShip, cart=session['cart'], delivery=session['deliverychoice'],
                           payment=session['paymentchoice'], products=product_names_prices, subtotal=subtotal, prices=DELIVERYPRICE)


@main.route('/thanks')
def thanks():
    return render_template('thanks.html')
