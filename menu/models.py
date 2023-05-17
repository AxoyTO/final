from menu import db
from sqlalchemy_utils import PhoneNumber
import datetime
from zoneinfo import ZoneInfo

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.now(tz=ZoneInfo('localtime')))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)

    def __repr__(self):
        return f"<Order with ID#{id} and status {self.order_status}, created at {self.created_at} by {self.created_by}>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    _phone_number = db.Column(db.Unicode(255))
    phone_country_code = db.Column(db.Unicode(8))
    phone_number = db.composite(
        PhoneNumber,
        _phone_number,
        phone_country_code
    )

    orders = db.relationship("Order", backref='user_orders', lazy=True)

    def __repr__(self):
        return f"<User with ID#{self.id} and phone number: {self.phone_number}>"
    
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(80), nullable = False, unique=True)
    type = db.Column(db.String(40))
    price = db.Column(db.Float)
    orders = db.relationship('Order', backref='meal_orders', lazy=True)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbs = db.Column(db.Float)
    calory = db.Column(db.Integer)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f"<Meal {self.meal} with ID#{self.id}>"