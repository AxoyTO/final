from menu import db
from sqlalchemy_utils import PhoneNumber
import datetime

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_status = db.Column(db.String)
    meals = db.relationship('Cart', backref='orders')
    
    def __repr__(self):
        return f"<Order with ID#{self.id} and status {self.order_status}, created at {self.created_at} by {self.created_by}>"

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

    def __repr__(self):
        return f"<Cart with ID#{self.id}>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    _phone_number = db.Column(db.Unicode(255))
    phone_country_code = db.Column(db.Unicode(8))
    phone_number = db.composite(
        PhoneNumber,
        _phone_number,
        phone_country_code
    )

    cart = db.relationship("Order", backref='user_cart', lazy=True)

    def __repr__(self):
        return f"<User with ID#{self.id} and phone number: {self.phone_number}>"
    
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(80), nullable = False, unique=True)
    type = db.Column(db.String(40))
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbs = db.Column(db.Float)
    calory = db.Column(db.Integer)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)

    def __repr__(self):
        return f"<Meal {self.meal} with ID#{self.id}>"