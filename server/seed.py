from faker import Faker
from random import randint, choice

from server.models import db
from server.models.user import User
from server.models.admin import Admin
from server.models.food_item import FoodItem
from server.models.order import Order
from server.models.order_item import OrderItem
from server.app import create_app

fake = Faker()

def seed_data():
    print("Seeding Taste Town data...")

    # Clear existing data
    OrderItem.query.delete()
    Order.query.delete()
    FoodItem.query.delete()
    User.query.delete()
    Admin.query.delete()
    db.session.commit()

    # Create admin
    admin = Admin(username="admin1", email="admin@example.com")
    admin.password = "adminpass123"
    db.session.add(admin)

    # Create users
    users = []
    for _ in range(5):
        user = User(username=fake.user_name(), email=fake.email())
        user.password = "userpass123"
        users.append(user)
        db.session.add(user)

    # Food images from Unsplash
    unsplash_images = {
        "Burgers": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=400&auto=format",
        "Pizza": "https://images.unsplash.com/photo-1542281286-9e0a16bb7366?w=400&auto=format",
        "Drinks": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=400&auto=format",
        "Desserts": "https://images.unsplash.com/photo-1599785209798-8d9e060d2a4f?w=400&auto=format"
    }

    categories = list(unsplash_images.keys())

    # Create food items
    food_items = []
    for category in categories:
        item = FoodItem(
            name=fake.word().capitalize(),
            description=fake.sentence(),
            price=round(fake.pyfloat(min_value=5, max_value=25), 2),
            category=category,
            image_url=unsplash_images[category]
        )
        food_items.append(item)
        db.session.add(item)

    db.session.commit()

    # Create orders and order items
    for user in users:
        order = Order(user_id=user.id, total=0)
        db.session.add(order)
        db.session.commit()

        for _ in range(randint(1, 3)):
            food = choice(food_items)
            order_item = OrderItem(
                order_id=order.id,
                food_item_id=food.id,
                quantity=randint(1, 3)
            )
            db.session.add(order_item)

    db.session.commit()
    print("Seeding complete.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_data()
