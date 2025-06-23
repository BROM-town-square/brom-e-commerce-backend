from . import db
from sqlalchemy_serializer import SerializerMixin

class FoodItem(db.Model, SerializerMixin):

    __tablename__ = 'food_items'

    serialize_rules = ('-order_items.food_item',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.string)
    category = db.Column(db.string)
    order_items = db.relationship("OrderItem", back_populates="food_item")

    def __repr__(self):
        return f"<FoodItem {self.name} - ${self.price}>"