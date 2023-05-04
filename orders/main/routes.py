from flask import render_template, Blueprint

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
@main.route('/home', methods=['GET'])
def home():
    return render_template('home.html')
