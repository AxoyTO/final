from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from menu import db
from menu.users.forms import RegistrationForm, LoginForm
from menu.models import User, Cart
import menu.utils as ut
import phonenumbers

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    total_price = ut.get_total_price()
    cart = Cart.query.all()
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        pn = form.phone_number.data
        cc = phonenumbers.region_code_for_country_code('US')
        user = User(name=form.name.data, _phone_number=pn, phone_country_code=cc)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in.", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="REGISTER", form=form, total_price=total_price, total_cart=len(cart))


@users.route("/login", methods=["GET", "POST"])
def login():
    total_price = ut.get_total_price()
    cart = Cart.query.all()
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(_phone_number=form.phone_number.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(f"Successfully logged in as {user.phone_number}", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login failed. Please check email and password", "danger")
    return render_template("login.html", title="LOGIN", form=form, total_price=total_price, total_cart=len(cart))


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))