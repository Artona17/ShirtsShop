from flask import render_template, session, redirect, url_for, request
# -*- coding: utf-8 -*-
from . import main
from ..models import Product, Fandom, Type, Item, Size, Order
from .forms import ContactForm, HowManyProducts, SortingForm, ShippingForm, ReviewForm, DeliveryandPaymentForm, SelectSizeForm
from app import db


@main.route('/product')
@main.route('/product/<int:product_id>')
def product(product_id):
    review_form = ReviewForm()
    product_info = Product.query.filter(Product.id == product_id).first_or_404()
    product_info.price = int(product_info.price)
    items = Item.query.filter(Item.product_info_id == product_id).all()
    quantity = 0

    if len(items) == 0:
        # redirect to the page where it says that products is not at the stock now
        pass

    session['url'] = request.path
    size_ids = []

    for item in items:
        size_ids.append(item.size_id)
        quantity += item.quantity

    sizes = Size.query.filter(Size.id.in_(set(size_ids))).all()

    if not review_form.validate():
        print(review_form.errors)
        # now = datetime.datetime.now()
        # review = Review(product_id=id, date=now.strftime("%d-%m-%Y"), name=review_form.name.data, comment=review_form.enquiry.data, rating=review_form.rating.data)
        # db.session.add(review)
        # print(db.session)
    return render_template('single-product.html', form=review_form,
                           product=product_info, sizes=sizes, quantity=quantity)


@main.route('/shop', methods=['GET', 'POST'])
@main.route('/shop/<int:page>', methods=['GET', 'POST'])
def shop(page=1, items_per_page=3):
    howManyProducts_form = HowManyProducts()
    sorting_form = SortingForm()

    session['products_shop'] = []
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
        products = Product.query.filter(Product.id.in_(products_ids)).paginate(page, items_per_page, False)  # ИЗМЕНИТЬ здесь
        session['products_shop'] = products_ids
        print(products)
        print(session['products_shop'])
    elif session['products_shop']:
        products = Product.query.filter(Product.id.in_(session['products_shop'])).paginate(page, items_per_page, False)
    else:
        products = Product.query.paginate(page, items_per_page, False)

    return render_template('shop.html', types=types, fandoms=fandoms, products=products,
                           form1=howManyProducts_form, form2=sorting_form)


@main.route('/cart')
def cart():
    form = SelectSizeForm()
    if 'cart' not in session:
        session['cart'] = {}
        return render_template('shopping-cart.html', cart=session['cart'])
    else:
        subtotal = 0
        product_names_prices = {}
        all_sizes = {}
        for item in session['cart']:
            id = list(item)
            sizes = [Size.query.filter(Size.id == i.size_id).first().size for i in Item.query.filter(Item.product_info_id == int(id[0])).all()]
            print(tuple(sizes))
            product = Product.query.filter(Product.id == int(id[0])).first()
            qty = session['cart'][item][0]
            product_names_prices.update({product.id: [product.product_name, int(product.price), qty,
                                                      int(product.price * qty), Size.query.filter(Size.id == int(session['cart'][item][1])).first().size]})
            subtotal += int(product.price) * qty
            all_sizes.update({int(id[0]): sizes})
        print(all_sizes)

        return render_template('shopping-cart.html', products=product_names_prices, cart=session['cart'],
                               subtotal=subtotal, sizes=all_sizes)


@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    Deliveryform = DeliveryandPaymentForm(request.form)

    product_names_prices = {}
    subtotal = 0

    for item in session['cart']:
        id = list(item)
        product = Product.query.filter(Product.id == int(id[0])).first()
        qty = session['cart'][item][0]
        product_names_prices.update({product.id: [product.product_name, int(product.price), qty, int(product.price * qty), int(session['cart'][item][1])]})
        subtotal += int(product.price) * qty

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
        id = list(item)
        product = Product.query.filter(Product.id == int(id[0])).first()
        qty = session['cart'][item][0]
        product_names_prices.update({product.id: [product.product_name, int(product.price), qty, int(product.price * qty), int(session['cart'][item][1])]})
        subtotal += int(product.price) * qty

    total = subtotal + DELIVERYPRICE[session['deliverychoice']]

    if formShip.validate_on_submit():
        if session['deliverychoice'] == 'Самовывоз':
            order = Order(surname=formShip.LastName.data, name=formShip.FirstName.data, mail=formShip.Email.data, phone=formShip.phone.data, products=str(product_names_prices), sum=total)
            db.session.add(order)
            db.session.commit()
        elif session['deliverychoice'] == 'Почтой':
            order = Order(surname=formShip.LastName.data, name=formShip.FirstName.data, mail=formShip.Email.data,
                          phone=formShip.phone.data, address=formShip.town.data, postcode=str(product_names_prices), products=product_names_prices, sum=total)
            db.session.add(order)
            db.session.commit()
        else:
            order = Order(surname=formShip.LastName.data, name=formShip.FirstName.data, mail=formShip.Email.data,
                          phone=formShip.phone.data, address=formShip.town.data, products=str(product_names_prices), sum=total)
            db.session.add(order)
            db.session.commit()
        order = Order.query.filter(Order.surname == order.surname, Order.phone == order.phone, Order.products == order.products).first()
        return redirect(url_for('main.thanks', order_id=order.id))

    return render_template('name_address.html', form=formShip, cart=session['cart'], delivery=session['deliverychoice'],
                           payment=session['paymentchoice'], products=product_names_prices, subtotal=subtotal,
                           prices=DELIVERYPRICE, total=total)


@main.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    product_id = int(request.form['product_id'])
    if int(request.form['size']):
        size_id = int(request.form['size'])
    else:
        size_id = 1

    #if request.form['quantity'] == '#qtybutton.value':
    qty = 1
    #else:
    #    qty = int(request.form['quantity'])
    print(session)
    if 'cart' not in session:
        session['cart'] = {}
    cart_list = session['cart']
    for item in cart_list:
        print(item)
        id = int(item)
        qty_was = session['cart'][item][0]
        size = session['cart'][item][1]
        if id == product_id and size == size_id:
            session['cart'].update({str(id): [qty_was + qty, size]})
            break
    else:
        cart_list.update({str(product_id): [qty, size_id]})
    session['cart'] = cart_list
    # flash('Товар {0} успешно добавлен в корзину!', product.name)
    return redirect(session['url'])


@main.route("/remove_from_cart", methods=['POST'])
def remove_from_cart():
    product_id = int(request.form['product_id'])
    size_id = request.form['size_id']
    cart_list = session['cart'].copy()
    for item in session['cart']:
        id = int(item)
        size = session['cart'][item][1]
        if id == product_id and size == size_id:
            del cart_list[item]
    session['cart'] = cart_list
    print(session)
    return redirect(url_for('main.cart'))


@main.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@main.route('/thanks/<int:order_id>')
def thanks(order_id):
    del session['cart']
    return render_template('thanks.html', order_id=order_id)


@main.route('/contact')
def contact():
    form = ContactForm()
    return render_template('contact.html', form=form)

# @main.route("/how_much", methods=['POST'])
# def how_much():
#    qty = int(request.form.get('quantity'))
#    print(qty)
#    product_id = int(request.form['product_id'])
#    print(product_id)
#    print(session)
#    cart_list = session['cart']
#    session['cart'] = cart_list
#    print(session)
#    return redirect(url_for('main.cart'))
