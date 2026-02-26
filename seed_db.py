from app import app, db
from models import Product

products = [
    # (Name, Description, Price, Stock, Category, Image)
    ("Fresh Spinach", "Organic green spinach leaves", 40.0, 15, "Vegetables", "spinach.png"),
    ("Royal Gala Apples", "Sweet and crunchy red apples", 180.0, 0, "Fruits", "apples.png"),
    ("Amul Fresh Milk", "Pasteurized full cream milk 1L", 60.0, 15, "Dairy Products", "milk.png"),
    ("Chicken Nuggets", "Crispy golden chicken nuggets 500g", 250.0, 15, "Frozen Non-Veg", "nuggets.png"),
    ("Coca Cola 2L", "Refreshing sparkling soft drink", 95.0, 15, "Soft Drinks", "cola.png"),
    ("Lays Classic", "Salted potato chips", 20.0, 0, "Snacks", "chips.png"),
    ("Daawat Basmati Rice", "Premium long grain rice 1kg", 150.0, 15, "Rice & Pulses", "rice.png"),
    ("Fortune Sunflower Oil", "Healthy refined sunflower oil 1L", 120.0, 15, "Cooking Oils", "oil.png"),
    ("Dove Soap", "Moisturizing cream beauty bar", 55.0, 15, "Personal Care", "soap.png"),
    ("Lizol Floor Cleaner", "Disinfectant surface cleaner", 145.0, 15, "Cleaning Supplies", "lizol.png"),
    ("Dairy Milk Silk", "Smooth and creamy chocolate bar", 80.0, 15, "Chocolates", "chocolate.png"),
    ("Johnson's Baby Powder", "Soft and gentle baby powder", 130.0, 15, "Baby Products", "powder.png")
]

with app.app_context():
    # Only add if table is empty or just add them
    for name, desc, price, stock, cat, img in products:
        if not Product.query.filter_by(name=name).first():
            p = Product(name=name, description=desc, price=price, stock=stock, category=cat, image=img)
            db.session.add(p)
    db.session.commit()
    print("Database seeded successfully!")
