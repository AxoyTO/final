from flask import render_template,Blueprint

users = Blueprint('users', __name__)

@users.route('/', methods=['GET'])
@users.route('/home', methods=['GET'])
def home():
    return render_template('home.html')