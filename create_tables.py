from orders import create_app, db
from models import Order, User, Menu

orders_app = create_app()
with orders_app.app_context():
    #db.drop_all()
    db.create_all()
