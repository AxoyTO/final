from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from menu.config import Config


db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from menu.main.routes import main
    from menu.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
