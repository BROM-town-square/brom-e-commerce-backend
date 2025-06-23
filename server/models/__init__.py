from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

from .user import User
from .admin import Admin
from .order import Order
from .food_item import FoodItem
from .order_item import OrderItem
from .token_blocklist import TokenBlocklist