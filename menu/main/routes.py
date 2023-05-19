from flask import render_template, Blueprint, redirect, url_for, request, flash
from menu import db
from sqlalchemy import func, text, desc
from menu.forms import CartForm
from menu.models import Menu, Order

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    total_price = get_total_price()
    cart = Order.query.filter_by(order_status="InProgress").all()
    cart_form = add_to_cart()
    return redirect(
                    url_for('main.menu',
                            meals='kebabs',
                            form=cart_form,
                            total_cart=len(cart),
                            total_price=total_price))

@main.route('/cart/', methods=['GET', 'POST'])
def cart():
    cart_form = add_to_cart()
    total_price = get_total_price()

    query = text('select                                            \
                    count("order".meal_id) as meal_count,           \
                    meal_id,                                        \
                    menu.meal,                                      \
                    menu.protein,                                   \
                    menu.fat,                                       \
                    menu.carbs,                                     \
                    menu.calory,                                    \
                    sum(menu.price) as total_price                  \
                from                                                \
                    "order" as "order"                              \
                    join menu as menu on menu.id = "order".meal_id  \
                group by                                            \
                    meal_id;')
    
    total_cart = db.session.execute(text('select count(id) from "order"'))
    for r in total_cart:
        total_cart = r[0]
    query_result = db.session.execute(query)
    query_result = [r for r in query_result]

    return render_template('cart.html',
                           title='CART',
                           cart=query_result,
                           form=cart_form,
                           total_cart=total_cart,
                           total_price=total_price)

@main.route('/<meals>/', methods=['GET', 'POST'])
def menu(meals=None):
    total_price = get_total_price()
    cart = Order.query.filter_by(order_status="InProgress").all()

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


def add_to_cart():
    cart_form = CartForm()
    if cart_form.is_submitted():
        meal_id = cart_form.meal_id.data
        print(meal_id)
        if cart_form.delete.data:
            meal = Order.query.filter_by(meal_id=meal_id).order_by(desc(Order.created_at)).first()
            if not meal is None:
                db.session.delete(meal)
        if cart_form.add.data:
            print(meal_id)
            meal = Order(order_status="InProgress", meal_id=meal_id, created_by="dummy")
            db.session.add(meal)
        db.session.commit()
    return cart_form


def get_total_price():
    total_price = db.session.execute(text('select sum(price) from "order" join menu on menu.id = "order".meal_id')).first()[0]
    return total_price