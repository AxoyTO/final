from flask import render_template, Blueprint, redirect, url_for, request, flash
from menu import db
from sqlalchemy import func
from menu.forms import AddToCartForm
from menu.models import Menu, Order

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    cart = Order.query.filter_by(order_status="InProgress").all()
    add_to_cart_form = add_to_cart()
    return redirect(url_for('main.menu', meals='kebabs', form=add_to_cart_form, cart=len(cart)))

@main.route('/cart/', methods=['GET', 'POST'])
def cart():
    cart = db.session.query(Order.meal_id, func.count(Order.meal_id)).group_by(Order.meal_id).all()
    """
    select 
        count("order".meal_id) as meal_count,
        menu.meal,
        menu.protein,
        menu.fat,
        menu.carbs,
        menu.calory,
        sum(menu.price) 
    from 
        "order" as "order" 
        join menu as menu on menu.id = "order".meal_id 
    group by
        meal_id;
    """
    print(cart)
    return render_template('cart.html', title='CART', cart=cart)

@main.route('/<meals>/', methods=['GET', 'POST'])
def menu(meals=None):
    cart = Order.query.filter_by(order_status="InProgress").all()
    print(request.form)

    add_to_cart_form = add_to_cart()

    if meals != 'Dessert':
        menu = Menu.query.filter_by(type=meals[:-1].capitalize()).all()
    else:
        menu = Menu.query.filter_by(type=meals.capitalize()).all()
    return render_template('home.html', menu=menu, title=meals.upper(), form=add_to_cart_form, cart=len(cart))


def add_to_cart():
    add_to_cart_form = AddToCartForm()
    if add_to_cart_form.is_submitted():
        meal_id = add_to_cart_form.meal_id.data
        meal = Order(order_status="InProgress", meal_id=meal_id, created_by="dummy")
        db.session.add(meal)
        db.session.commit()
    return add_to_cart_form
