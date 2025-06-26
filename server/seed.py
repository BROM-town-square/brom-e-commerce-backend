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

sample_foods = {
    "Burgers": [
        "Classic Cheeseburger", "Bacon Double Deluxe", "Veggie Supreme Burger",
        "Spicy Chicken Burger", "Mushroom Swiss Burger"
    ],
    "Pizza": [
        "Pepperoni Feast", "Margherita", "BBQ Chicken Pizza",
        "Hawaiian Pizza", "Four Cheese Pizza", "Spicy Sausage Pizza"
    ],
    "Drinks": [
        "Coca-Cola", "Fresh Mango Juice", "Iced Latte", "Sparkling Water", "Lemon Iced Tea"
    ],
    "Desserts": [
        "Chocolate Lava Cake", "New York Cheesecake", "Vanilla Ice Cream",
        "Apple Pie", "Tiramisu", "Brownie Sundae"
    ]
}


food_images = {
    "Classic Cheeseburger": "https://plus.unsplash.com/premium_photo-1683619761492-639240d29bb5?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Q2xhc3NpYyUyMENoZWVzZWJ1cmdlcnxlbnwwfHwwfHx8MA%3D%3D",
    "Bacon Double Deluxe": "https://images.unsplash.com/photo-1606851576477-6e801666853a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fEJhY29uJTIwJTIwRG91YmxlJTIwZGVsdXhlfGVufDB8fDB8fHww",
    "Veggie Supreme Burger": "https://images.unsplash.com/photo-1603064752734-4c48eff53d05?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHZlZ2dpZSUyMHN1cHJlbWUlMjBidXJnZXJ8ZW58MHx8MHx8fDA%3D",
    "Spicy Chicken Burger": "https://images.unsplash.com/photo-1645024679624-e8351ac98f01?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8c3BpY3klMjBjaGlja2VuJTIwYnVyZ2VyfGVufDB8fDB8fHww",
    "Mushroom Swiss Burger": "https://media.istockphoto.com/id/539659420/photo/mushroom-swiss-burger.jpg?s=612x612&w=is&k=20&c=FBMTVh9zkcSd3Q7d-kBQrVPBdT9LvMm42Q_chpb2QLo=",

    "Pepperoni Feast": "https://images.unsplash.com/photo-1564128442383-9201fcc740eb?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cGVwcGVyb25pJTIwcGl6emF8ZW58MHx8MHx8fDA%3D",
    "Margherita": "https://images.unsplash.com/photo-1598023696416-0193a0bcd302?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8bWFyZ2hlcml0YSUyMHBpenphfGVufDB8fDB8fHww",
    "BBQ Chicken Pizza": "https://plus.unsplash.com/premium_photo-1664472696633-4b0b41e95202?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8YmJxJTIwY2hpY2tlbiUyMHBpenphfGVufDB8fDB8fHww",
    "Hawaiian Pizza": "https://images.unsplash.com/photo-1708968118195-156379baf904?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cGluYXBwbGUlMjBwaXp6YXxlbnwwfHwwfHx8MA%3D%3D",
    "Four Cheese Pizza": "https://images.unsplash.com/photo-1595378833483-c995dbe4d74f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y2hlc3NlJTIwcGl6emF8ZW58MHx8MHx8fDA%3D",
    "Spicy Sausage Pizza": "https://media.istockphoto.com/id/968775256/photo/sausage-pizza.jpg?s=612x612&w=is&k=20&c=SzpIvs9mJzE0cuNrmlOZ9SfnifvK2M__nNi8rd1bqeA=",

    "Coca-Cola": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y29jYSUyMGNvbGF8ZW58MHx8MHx8fDA%3D",
    "Fresh Mango Juice": "https://images.unsplash.com/photo-1604298331663-de303fbc7059?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZnJlc2glMjBtYW5nbyUyMGp1aWNlfGVufDB8fDB8fHww",
    "Iced Latte": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8aWNlZCUyMGxhdHRlfGVufDB8fDB8fHww",
    "Sparkling Water": "https://images.unsplash.com/photo-1689861596658-3bdeb6aa0e30?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8c3BhY2tsaW5nJTIwd2F0ZXIlMjBkcmlua3xlbnwwfHwwfHx8MA%3D%3D",
    "Lemon Iced Tea": "https://plus.unsplash.com/premium_photo-1664392087859-815b337c3324?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8bGVtb24lMjBpY2VkJTIwdGVhfGVufDB8fDB8fHww",

    "Chocolate Lava Cake": "https://images.unsplash.com/photo-1652561781059-58d5d9ffcb4d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8Y2hvY29sYXRlJTIwbGF2YSUyMGNha2V8ZW58MHx8MHx8fDA%3D",
    "New York Cheesecake": "https://media.istockphoto.com/id/2152360084/photo/slice-of-strawberry-cheesecake.jpg?s=612x612&w=is&k=20&c=w1x5OKnuoy34SF65dQqjztQrvC5qtaTSVaoc0b-lHKA=",
    "Vanilla Ice Cream": "https://images.unsplash.com/photo-1560008581-09826d1de69e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8dmFuaWxsYSUyMGljZSUyMGNyZWFtfGVufDB8fDB8fHww",
    "Apple Pie": "https://images.unsplash.com/photo-1562007908-17c67e878c88?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8YXBwbGUlMjBwaWV8ZW58MHx8MHx8fDA%3D",
    "Tiramisu": "https://media.istockphoto.com/id/1134778606/photo/fresh-tiramisu-cake-white-background.webp?a=1&b=1&s=612x612&w=0&k=20&c=k9AnRxnY22v-4m1jlNYoS3GNGFVxjvys-FYM7e2IiMU=",
    "Brownie Sundae": "https://media.istockphoto.com/id/157586474/photo/vanilla-ice-cream-and-walnut-brownie.webp?a=1&b=1&s=612x612&w=0&k=20&c=4HW7Y37nklE35VU9Il3vl43wlrzNYmC_7_Df1XuugTM="
}

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
        db.session.add(user)
        users.append(user)

    food_items = []
    for category, items in sample_foods.items():
        for item_name in items:
            food = FoodItem(
                name=item_name,
                description=fake.sentence(nb_words=10),
                price=round(fake.pyfloat(min_value=4, max_value=20), 2),
                category=category,
                image_url=food_images[item_name]
            )
            db.session.add(food)
            food_items.append(food)

    db.session.commit()

    for user in users:
        for _ in range(randint(1, 2)):
            order = Order(user_id=user.id, total=0)
            db.session.add(order)
            db.session.commit()

            order_total = 0
            for _ in range(randint(1, 3)):
                item = choice(food_items)
                qty = randint(1, 3)
                order_item = OrderItem(
                    order_id=order.id,
                    food_item_id=item.id,
                    quantity=qty
                )
                order_total += item.price * qty
                db.session.add(order_item)

            order.total = round(order_total, 2)
            db.session.commit()

    print("Seeding complete.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_data()