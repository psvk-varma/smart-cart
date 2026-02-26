from app import app, db
from models import Product

# List of 30 products across all categories
products_data = [
    # (Name, Description, Price, Stock, Category, Image)
    # Vegetables
    ("Organic Tomatoes", "Fresh red organic tomatoes per kg", 60.0, 20, "Vegetables", "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=500&q=80"),
    ("Broccoli", "High protein fresh broccoli", 45.0, 0, "Vegetables", "https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?w=500&q=80"),
    ("Carrots", "Sweet and crunchy orange carrots", 30.0, 15, "Vegetables", "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=500&q=80"),
    
    # Fruits
    ("Alphonso Mango", "King of mangoes 1kg pack", 450.0, 10, "Fruits", "https://images.unsplash.com/photo-1553279768-865429fa0078?w=500&q=80"),
    ("Bananas", "Fresh yellow ripe bananas 1 dozen", 60.0, 25, "Fruits", "https://images.unsplash.com/photo-1571771894821-ad9902ed120c?w=500&q=80"),
    ("Strawberries", "Fresh red mountain strawberries", 120.0, 0, "Fruits", "https://images.unsplash.com/photo-1464965911861-746a04b01ca6?w=500&q=80"),
    
    # Dairy
    ("Amul Gold Milk", "Full cream milk 1 Litre", 66.0, 30, "Dairy Products", "https://images.unsplash.com/photo-1563636619-e910009355bb?w=500&q=80"),
    ("Greek Yogurt", "Plain high protein greek yogurt 500g", 180.0, 12, "Dairy Products", "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500&q=80"),
    
    # Frozen Non-Veg
    ("Chicken Sausages", "Classic smoked chicken sausages", 220.0, 8, "Frozen Non-Veg", "https://images.unsplash.com/photo-1544025162-d76694265947?w=500&q=80"),
    ("Frozen Prawns", "Cleaned and deveined prawns 500g", 550.0, 5, "Frozen Non-Veg", "https://images.unsplash.com/photo-1559742811-822873691df8?w=500&q=80"),
    
    # Soft Drinks
    ("Mountain Dew", "Citrus flavoured cold drink 750ml", 45.0, 0, "Soft Drinks", "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&q=80"),
    ("Sparkling Water", "Refreshing citrus sparkling water", 90.0, 18, "Soft Drinks", "https://images.unsplash.com/photo-1551713437-01314fba00d3?w=500&q=80"),
    
    # Snacks
    ("Pringles Onion", "Sour cream and onion chips", 110.0, 14, "Snacks", "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=500&q=80"),
    ("Doritos Nachos", "Classic cheese nacho chips", 50.0, 20, "Snacks", "https://images.unsplash.com/photo-1600952841320-db92ec4047ca?w=500&q=80"),
    ("Oreo Cookies", "Chocolate sandwich cookies 120g", 35.0, 0, "Snacks", "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=500&q=80"),
    
    # Rice & Pulses
    ("Basmati Rice", "Premium long grain basmati 5kg", 750.0, 8, "Rice & Pulses", "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=500&q=80"),
    ("Red Lentils", "Masoor dal high protein 1kg", 110.0, 15, "Rice & Pulses", "https://images.unsplash.com/photo-1585994192701-11c50b6bc791?w=500&q=80"),
    
    # Cooking Oils
    ("Olive Oil", "Extra virgin olive oil col pressed 1L", 950.0, 6, "Cooking Oils", "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500&q=80"),
    ("Coconut Oil", "Pure cold pressed coconut oil 500ml", 250.0, 0, "Cooking Oils", "https://images.unsplash.com/photo-1549479704-df4e339f4007?w=500&q=80"),
    
    # Personal Care
    ("Luxury Handwash", "Aromatic gentle handwash 250ml", 195.0, 10, "Personal Care", "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500&q=80"),
    ("Face Cream", "Aloe vera moisturizer 50g", 350.0, 7, "Personal Care", "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=500&q=80"),
    ("Organic Shampoo", "Sulfate free herbal shampoo", 450.0, 0, "Personal Care", "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=500&q=80"),
    
    # Cleaning Supplies
    ("Dishwashing Liquid", "Lemon fresh dish gel 500ml", 120.0, 12, "Cleaning Supplies", "https://images.unsplash.com/photo-1584622781564-1d9876a13d00?w=500&q=80"),
    ("Glass Cleaner", "Streak free glass cleaner spray", 145.0, 9, "Cleaning Supplies", "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=500&q=80"),
    
    # Chocolates
    ("Dark Chocolate", "85% cocoa gourmet bar", 250.0, 5, "Chocolates", "https://images.unsplash.com/photo-1511381939415-e4401546383a?w=500&q=80"),
    ("Assorted Truffles", "Box of 12 luxury truffles", 650.0, 0, "Chocolates", "https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=500&q=80"),
    ("Hazelnut Bar", "Milk chocolate with hazelnuts", 150.0, 15, "Chocolates", "https://images.unsplash.com/photo-1548907040-4baa42d10919?w=500&q=80"),
    
    # Baby Products
    ("Baby Lotion", "pH balanced gentle baby lotion", 240.0, 8, "Baby Products", "https://images.unsplash.com/photo-1515488764276-38548b01ba93?w=500&q=80"),
    ("Baby Wipes", "Unscented zero alcohol wipes", 185.0, 20, "Baby Products", "https://images.unsplash.com/photo-1544145945-f904253d0c7b?w=500&q=80"),
    ("Diaper Pack", "Soft comfort diapers small 44pk", 850.0, 0, "Baby Products", "https://images.unsplash.com/photo-1595111022312-d7efc4687e2b?w=500&q=80")
]

with app.app_context():
    # Clear existing products to avoid duplicates and start fresh as requested
    Product.query.delete()
    
    for name, desc, price, stock, cat, img in products_data:
        p = Product(
            name=name, 
            description=desc, 
            price=price, 
            stock=stock, 
            category=cat, 
            image=img # Storing URL as image for this demo
        )
        db.session.add(p)
    
    db.session.commit()
    print(f"Success: {len(products_data)} products added to the database!")
