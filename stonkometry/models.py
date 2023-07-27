from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime


# Adding Flask Security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import Secrets Module
import secrets

from flask_login import UserMixin, LoginManager

# import for flask-marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # stonk = db.relationship('Stonks', backref = 'owner', lazy = True)

    def __init__(self, email, username, password='', first_name = '', last_name = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    
    def __repr__(self):
        return f"User {self.email} has been added to the database! :O"
    

class Stocks(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    exchange = db.Column(db.String(200), nullable = True)
    currency = db.Column(db.Numeric(precision=10, scale=2))
    open_price = db.Column(db.String(150), nullable = True)
    high_price = db.Column(db.String(100), nullable=True)
    low_price = db.Column(db.String(100))
    close_price = db.Column(db.String(100))
    volume = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, exchange, currency, open_price, high_price, low_price, close_price,
                  volume, user_token):
        self.id = self.set_id()
        self.name = name
        self.exchange = exchange
        self.currency = currency
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"{self.name} has been added to the database!!! :)"
    

class StocksSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'exchange', 'currency', 'open_price', 'high_price', 'low_price',
                  'close_price', 'volume']
        
stock_schema = StocksSchema()
stocks_schema = StocksSchema(many = True)