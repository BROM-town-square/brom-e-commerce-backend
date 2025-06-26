from . import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy

class Order(db.Model, SerializerMixin):

    __tablename__ = 'orders'

    serialize_rules = ('-user.orders', '-items.order',)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False, default=0.0)
    user = db.relationship("User", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order")
    menu_items = association_proxy("items", "food_item")

    def __repr__(self):
        return f"<Order #{self.id} - User {self.user_id} - Total: ${self.total:.2f}>"
