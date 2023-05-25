from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, EqualTo, Email
from menu.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Sign Up')

    def validate_number(self, phone_number):
        phone_number = User.query.filter_by(phone_number=phone_number.data).first()
        if phone_number:
            raise ValidationError(f'Phone Number {phone_number.data} already exists. Please log in.')


class LoginForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
