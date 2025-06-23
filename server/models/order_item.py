from . import db
from sqlalchemy_serializer import SerializerMixin

class OrderItem(db.Model, SerializerMixin):

    __tablename__ = "order_items"

    serialize_rules = ('-order.items', '-food_item.order_items',)

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    order = db.relationship("Order", back_populates="items")
    food_item = db.relationship("FoodItem", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem {self.quantity}x {self.food_item_id} in Order {self.order_id}>"
