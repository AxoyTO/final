from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField

class AddToCartForm(FlaskForm):
    meal_id = IntegerField()
    submit = SubmitField('Add to cart')