from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from service.routes import products
    app.register_blueprint(products)

    with app.app_context():
        db.create_all()

    return app
