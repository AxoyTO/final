from sqlalchemy import text
from menu import db

def get_total_price():
    total_price = db.session.execute(text('select sum(price) from cart join menu on menu.id = cart.meal_id')).first()[0]
    return total_price


def get_next_order_id():
    order_id = db.session.execute(text('SELECT CASE WHEN max(order_id) is NULL THEN 1 ELSE max(order_id)+1 END AS id FROM orders')).first()[0]
    return order_id