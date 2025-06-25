
from server.app import create_app
from server.models import db
from server.models.admin import Admin
from server.models.user import User
from server.models.food_item import FoodItem
from server.models.order import Order
from server.models.order_item import OrderItem

app = create_app()

with app.app_context():
    print(" Dropping all tables...")
    db.drop_all()

    print(" Creating all tables...")
    db.create_all()

    print(" Seeding admin...")
    admin = Admin(username="admin", email="admin@example.com")
    admin.password = "admin123"
    db.session.add(admin)

    print(" Seeding users...")
    user1 = User(username="alice", email="alice@example.com")
    user1.password = "password1"

    user2 = User(username="bob", email="bob@example.com")
    user2.password = "password2"

    db.session.add_all([user1, user2])
    db.session.flush() 

    print(" Seeding food items...")
    burger = FoodItem(name="Cheeseburger", description="Tasty burger", price=8.99, image_url="https://example.com/burger.jpg", category="Fast Food")
    pizza = FoodItem(name="Margherita Pizza", description="Tomato & cheese", price=10.99, image_url="https://example.com/pizza.jpg", category="Pizza")
    wrap = FoodItem(name="Chicken Wrap", description="Spicy chicken wrap", price=7.49, image_url="https://example.com/wrap.jpg", category="Wraps")

    db.session.add_all([burger, pizza, wrap])
    db.session.flush()  

    print(" Creating order for Alice...")
    order = Order(user_id=user1.id)
    db.session.add(order)
    db.session.flush()

    print(" Adding items to order...")
    item1 = OrderItem(order_id=order.id, food_item_id=burger.id, quantity=2)
    item2 = OrderItem(order_id=order.id, food_item_id=wrap.id, quantity=1)

    db.session.add_all([item1, item2])

    db.session.commit()
    print(" Done seeding database!")
