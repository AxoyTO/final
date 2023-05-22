from flask import render_template, Blueprint, redirect, url_for, request, flash
from menu import db
from sqlalchemy import func, text, desc
from menu.forms import CartForm
from menu.models import Menu, Cart, Orders, User

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    total_price = get_total_price()
    cart = Cart.query.all()
    cart_form = add_to_cart()
    return redirect(url_for('main.menu',
                            meals='kebabs'))

@main.route('/cart/', methods=['GET', 'POST'])
def cart():
    order_id = 0
    title = 'CART'
    if 'order_id' in request.args:
        order_id = request.args['order_id']
        title = "ORDER"
    cart_form = add_to_cart()
    total_price = get_total_price()

    query = text('select                                            \
                    count(cart.meal_id) as meal_count,              \
                    meal_id,                                        \
                    menu.meal,                                      \
                    menu.protein,                                   \
                    menu.fat,                                       \
                    menu.carbs,                                     \
                    menu.calory,                                    \
                    sum(menu.price) as total_price                  \
                from                                                \
                    cart as cart                                    \
                    join menu as menu on menu.id = cart.meal_id     \
                group by                                            \
                    meal_id;')
    
    total_cart = db.session.execute(text('select count(id) from cart'))
    for r in total_cart:
        total_cart = r[0]
    query_result = db.session.execute(query)
    query_result = [r for r in query_result]

    return render_template('cart.html',
                           title=title,
                           cart=query_result,
                           form=cart_form,
                           total_cart=total_cart,
                           total_price=total_price,
                           order_id=order_id
                           )

@main.route('/order/', methods=['POST'])
def order():
    order_id = create_order()
    return redirect(url_for('main.cart', order_id=order_id))

@main.route('/<meals>/', methods=['GET', 'POST'])
def menu(meals=None):
    total_price = get_total_price()
    
    cart = Cart.query.all()

    cart_form = add_to_cart()

    if meals != 'dessert':
        menu = Menu.query.filter_by(type=meals[:-1].capitalize()).all()
    else:
        menu = Menu.query.filter_by(type=meals.capitalize()).all()

    return render_template('home.html',
                           menu=menu,
                           title=meals.upper(),
                           form=cart_form,
                           total_cart=len(cart),
                           total_price=total_price)


def create_order():
    user_id = get_current_user_id()
    order_id = get_next_order_id()
    data = db.session.execute(text(f'select meal_id from cart where user_id = {user_id}')).all()
    for i in data:
        order = Orders(order_id=order_id, created_by=user_id, order_status="InProgress", meal_id=i[0])
        db.session.add(order)
    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return order_id

def add_to_cart():
    cart_form = CartForm()
    if cart_form.is_submitted():
        meal_id = cart_form.meal_id.data
        if cart_form.delete.data:
            meal = Cart.query.filter_by(meal_id=meal_id).first()
            if not meal is None:
                db.session.delete(meal)
        if cart_form.add.data:
            user_id = get_current_user_id()
            print(meal_id)
            meal = Cart(meal_id=meal_id, user_id=user_id)
            db.session.add(meal)
        db.session.commit()
    return cart_form


def get_total_price():
    total_price = db.session.execute(text('select sum(price) from cart join menu on menu.id = cart.meal_id')).first()[0]
    return total_price


def get_next_order_id():
    order_id = db.session.execute(text('SELECT CASE WHEN max(order_id) is NULL THEN 1 ELSE max(order_id)+1 END AS id FROM orders')).first()[0]
    return order_id

def get_current_user_id():
    return 1