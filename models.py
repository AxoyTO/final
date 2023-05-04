from orders import db
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
        return f"<OrderId: {id}>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    _phone_number = db.Column(db.Unicode(255))
    phone_country_code = db.Column(db.Unicode(8))
    phone_number = db.composite(
        PhoneNumber,
        _phone_number,
        phone_country_code
    )

    orders = db.relationship("Order", backref='user', lazy=True)

    def __repr__(self):
        return f"<User: {self.id} {self.phone_number}>"
    
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(80), nullable = False, unique=True)
    orders = db.relationship('Order', backref='meal', lazy=True)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbs = db.Column(db.Float)
    calory = db.Column(db.Integer)
    description = db.Column(db.String(200))