from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from orders.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from orders.main.routes import main

    app.register_blueprint(main)

    return app
