from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

ITEM_TYPES = ['BURGER', 'DRINK', 'FRIES']