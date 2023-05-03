from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from orderbox.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    CORS.init_app(app)

    from orderbox.main.routes import main
    #from orderbox.users.routes import users

    app.register_blueprint(main)
    #app.register_blueprint(users)

    return app
