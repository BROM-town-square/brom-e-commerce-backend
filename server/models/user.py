from . import db
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.associationproxy import association_proxy

class User(db.Model, SerializerMixin):

    __tablename__ = "users"

    serialize_rules = ('-orders.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    orders = db.relationship("Order", back_populates="user", cascade="all, delete-orphan")
    menu_items = association_proxy("orders", "food_items")

    @property
    def password(self):
        raise AttributeError("Pssword is write-only")

    @password.setter
    def password(self, plaintext):
        self._password_hash = generate_password_hash(plaintext)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f"<User {self.username} (customer)>"
