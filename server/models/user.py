from . import db
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, SerializerMixin):

    __tablename__ = "users"

    serialize_rules = ('-orders.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    orders = db.relationship("Order", back_populates="user")

    @property
    def password(self):
        raise AttributeError("Pssword is write-only")

    @password.setter
    def password(self, plaintext):
        self._password_hash = generate_password_hash(plaintext)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f"<User {self.username} ({'Admin' if self.is_admin else 'Customer'})>"
