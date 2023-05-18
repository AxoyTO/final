from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField

class CartForm(FlaskForm):
    meal_id = IntegerField()
    add = SubmitField('Add to cart')
    delete = SubmitField('Delete from cart')