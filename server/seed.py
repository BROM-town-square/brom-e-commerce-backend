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

    OrderItem.query.delete()
    Order.query.delete()
    FoodItem.query.delete()
    User.query.delete()
    Admin.query.delete()
    db.session.commit()

    
    admin = Admin(username="admin1", email="admin@example.com")
    admin.password = "adminpass123"
    db.session.add(admin)

    
    users = []
    for _ in range(5):
        user = User(username=fake.user_name(), email=fake.email())
        user.password = "userpass123"
        users.append(user)
        db.session.add(user)

    
    categories = ["Burgers", "Pizza", "Drinks", "Desserts"]
    food_items = []
    for _ in range(10):
        name = fake.word().capitalize()
        item = FoodItem(
            name=name,
            description=fake.sentence(),
            price=round(fake.pyfloat(min_value=5, max_value=25), 2),
            category=choice(categories),
            image_url=f"https://loremflickr.com/320/240/food?random={randint(1,1000)}"
        )
        food_items.append(item)
        db.session.add(item)

    db.session.commit()

    
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