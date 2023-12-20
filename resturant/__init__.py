from flask import Flask, session
from .extns import db, bcrypt

from .auth import auth
from .customer import customer
from .employee import employee


def create_app():
    app = Flask(__name__)

    app.jinja_env.globals['APPLICATION_NAME'] = "Fancy Restaurant"

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SECRET_KEY'] = "SECRETKEY123"

    app.register_blueprint(auth)
    app.register_blueprint(employee)
    app.register_blueprint(customer)

    db.init_app(app)
    with app.app_context():
        from resturant import models
        db.create_all()

    bcrypt.init_app(app)

    return app
