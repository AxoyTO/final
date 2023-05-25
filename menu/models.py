from menu import db, login_manager
from sqlalchemy_utils import PhoneNumber
from flask_login import UserMixin
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    order_status = db.Column(db.String)
    
    def __repr__(self):
        return f"<Order with ID#{self.id} and status {self.order_status}, created at {self.created_at} by {self.created_by}>"

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Cart with ID#{self.id} by User#{self.user_id}>"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    _phone_number = db.Column(db.Unicode(20))
    phone_country_code = db.Column(db.Unicode(8))
    phone_number = db.composite(
        PhoneNumber,
        _phone_number,
        phone_country_code
    )
    name = db.Column(db.String)
    balance = db.Column(db.Float)

    orders = db.relationship("Orders", backref='user', lazy=True)
    cart = db.relationship("Cart", backref="user", lazy=True)

    @classmethod
    def subtract_balance(cls, sub_balance, **kw):
        cls.query.filter_by(**kw).update({'balance': cls.balance - sub_balance})
        db.session.commit()

    @classmethod
    def get(cls, **kw):
        user = cls.query.filter_by(**kw).first()
        return user

    def __repr__(self):
        return f"<User with ID#{self.id} and phone number:{self.phone_number} and balance:{self.balance}>"
    
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