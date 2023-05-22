from menu import create_app, db
from menu.models import Cart, User, Menu, Orders

orders_app = create_app()
with orders_app.app_context():
    #db.drop_all()
    db.create_all()