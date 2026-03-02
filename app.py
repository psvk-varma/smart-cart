from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Product, Cart, Order, OrderItem
from itsdangerous import URLSafeTimedSerializer
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText
import random
import os

# ================= ADMIN CREDENTIALS =================
ADMIN_EMAIL = "admin@smartcart.com"
ADMIN_PASSWORD = "admin123"

app = Flask(__name__)
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(days=7)

# ================= IMAGE CONFIG =================
app.config['UPLOAD_FOLDER'] = "/tmp"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

db.init_app(app)

with app.app_context():
    db.create_all()

    # ✅ SEED ONLY IF EMPTY
    if Product.query.count() == 0:

        products_data = [
            # (Name, Description, Price, Stock, Category, Image)
            ("Organic Tomatoes", "Fresh red organic tomatoes per kg", 60.0, 20, "Vegetables", "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=500&q=80"),
            ("Broccoli", "High protein fresh broccoli", 45.0, 0, "Vegetables", "https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?w=500&q=80"),
            ("Carrots", "Sweet and crunchy orange carrots", 30.0, 15, "Vegetables", "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=500&q=80"),
            ("Alphonso Mango", "King of mangoes 1kg pack", 450.0, 10, "Fruits", "https://images.unsplash.com/photo-1553279768-865429fa0078?w=500&q=80"),
            ("Bananas", "Fresh yellow ripe bananas 1 dozen", 60.0, 25, "Fruits", "https://images.unsplash.com/photo-1571771894821-ad9902ed120c?w=500&q=80"),
            ("Strawberries", "Fresh red mountain strawberries", 120.0, 0, "Fruits", "https://images.unsplash.com/photo-1464965911861-746a04b01ca6?w=500&q=80"),
            ("Amul Gold Milk", "Full cream milk 1 Litre", 66.0, 30, "Dairy Products", "https://images.unsplash.com/photo-1563636619-e910009355bb?w=500&q=80"),
            ("Greek Yogurt", "Plain high protein greek yogurt 500g", 180.0, 12, "Dairy Products", "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500&q=80"),
            ("Chicken Sausages", "Classic smoked chicken sausages", 220.0, 8, "Frozen Non-Veg", "https://images.unsplash.com/photo-1544025162-d76694265947?w=500&q=80"),
            ("Frozen Prawns", "Cleaned and deveined prawns 500g", 550.0, 5, "Frozen Non-Veg", "https://images.unsplash.com/photo-1559742811-822873691df8?w=500&q=80"),
            ("Mountain Dew", "Citrus flavoured cold drink 750ml", 45.0, 0, "Soft Drinks", "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&q=80"),
            ("Sparkling Water", "Refreshing citrus sparkling water", 90.0, 18, "Soft Drinks", "https://images.unsplash.com/photo-1551713437-01314fba00d3?w=500&q=80"),
            ("Pringles Onion", "Sour cream and onion chips", 110.0, 14, "Snacks", "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=500&q=80"),
            ("Doritos Nachos", "Classic cheese nacho chips", 50.0, 20, "Snacks", "https://images.unsplash.com/photo-1600952841320-db92ec4047ca?w=500&q=80"),
            ("Oreo Cookies", "Chocolate sandwich cookies 120g", 35.0, 0, "Snacks", "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=500&q=80"),
        ]

        for name, desc, price, stock, cat, img in products_data:
            p = Product(
                name=name,
                description=desc,
                price=price,
                stock=stock,
                category=cat,
                image=img
            )
            db.session.add(p)

        db.session.commit()
        print("Database seeded with products!")

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# ================= HELPER FUNCTIONS =================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = app.config['MAIL_USERNAME']
    msg['To'] = to_email

    server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
    server.starttls()
    server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    server.send_message(msg)
    server.quit()


# ================= REGISTER =================
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':

        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords do not match", "danger")
            return redirect('/register')

        if User.query.filter_by(email=request.form['email']).first():
            flash("Email already exists", "danger")
            return redirect('/register')

        hashed_pw = generate_password_hash(request.form['password'])

        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect('/login')

    return render_template('register.html')


# ================= USER LOGIN =================
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':

        email = request.form['email'].strip()
        password = request.form['password'].strip()

        # CAPTCHA CHECK
        if int(request.form['captcha']) != session.get('captcha_answer'):
            flash("Invalid CAPTCHA", "danger")
            return redirect('/login')

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Invalid credentials", "danger")
            return redirect('/login')

        if check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            return redirect('/')
        else:
            flash("Invalid password", "danger")
            return redirect('/login')

    num1 = random.randint(1,10)
    num2 = random.randint(1,10)
    session['captcha_answer'] = num1 + num2

    return render_template('login.html', num1=num1, num2=num2)


# ================= ADMIN LOGIN =================
@app.route('/admin_login', methods=['GET','POST'])
def admin_login():

    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session.clear()
            session['admin'] = True
            session['role'] = 'admin'
            return redirect('/admin')
        else:
            flash("Invalid Admin Credentials", "danger")
            return redirect('/admin_login')

    return render_template('admin_login.html')


# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ================= HOME =================
@app.route('/')
@app.route('/category/<string:cat>')
def home(cat=None):

    if cat:
        products = Product.query.filter_by(category=cat).all()
    else:
        products = Product.query.all()

    categories = [
        "Vegetables",
        "Fruits",
        "Dairy Products",
        "Frozen Non-Veg",
        "Soft Drinks",
        "Snacks",
        "Rice & Pulses",
        "Cooking Oils",
        "Personal Care",
        "Cleaning Supplies",
        "Chocolates",
        "Baby Products"
    ]

    cart_dict = {}
    if session.get('user_id'):
        user_cart = Cart.query.filter_by(user_id=session['user_id']).all()
        cart_dict = {item.product_id: item for item in user_cart}

    return render_template('index.html',
                           products=products,
                           categories=categories,
                           cart_dict=cart_dict)


# ================= ADMIN DASHBOARD =================
@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin_login')

    products = Product.query.all()
    orders = Order.query.all()

    return render_template(
        'admin_dashboard.html',
        products=products,
        orders=orders
    )


# ================= ADD PRODUCT =================
@app.route('/add_product', methods=['GET','POST'])
def add_product():

    if not session.get('admin'):
        return redirect('/admin_login')

    if request.method == 'POST':

        image_file = request.files.get('image')
        filename = None

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)

        product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            stock=int(request.form['stock']),
            category=request.form['category'],
            image=filename
        )

        db.session.add(product)
        db.session.commit()

        flash("Product Added Successfully", "success")
        return redirect('/admin')

    return render_template('add_product.html')


# ================= EDIT PRODUCT =================
@app.route('/edit_product/<int:id>', methods=['GET','POST'])
def edit_product(id):
    if not session.get('admin'):
        return redirect('/admin_login')

    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        image_file = request.files.get('image')
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            product.image = filename

        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.category = request.form['category']

        db.session.commit()
        flash("Product Updated Successfully", "success")
        return redirect('/admin')

    return render_template('edit_product.html', product=product)


# ================= DELETE PRODUCT =================
@app.route('/delete_product/<int:id>')
def delete_product(id):

    if not session.get('admin'):
        return redirect('/admin_login')

    product = Product.query.get(id)

    if product.image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)
    db.session.commit()

    return redirect('/admin')


# ================= CART =================
@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if not session.get('user_id'):
        return redirect('/login')

    product = Product.query.get(id)

    if product.stock == 0:
        flash("Product is out of stock!", "danger")
        return redirect('/')

    # Check if already in cart
    item = Cart.query.filter_by(user_id=session['user_id'], product_id=id).first()
    if item:
        item.quantity += 1
    else:
        cart = Cart(user_id=session['user_id'], product_id=id, quantity=1)
        db.session.add(cart)
    
    db.session.commit()
    return redirect(request.referrer or '/cart')


@app.route('/increase/<int:id>')
def increase_cart(id):
    item = Cart.query.get(id)
    product = Product.query.get(item.product_id)
    if product.stock > item.quantity:
        item.quantity += 1
        db.session.commit()
    else:
        flash("Product out of stock!", "danger")
    return redirect(request.referrer or '/cart')


@app.route('/decrease/<int:id>')
def decrease_cart(id):
    item = Cart.query.get(id)
    if item.quantity > 1:
        item.quantity -= 1
        db.session.commit()
    else:
        db.session.delete(item)
        db.session.commit()
    return redirect(request.referrer or '/cart')


@app.route('/remove/<int:id>')
def remove_cart(id):
    item = Cart.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(request.referrer or '/cart')


@app.route('/cart')
def cart():
    if not session.get('user_id'):
        return redirect('/login')

    items = Cart.query.filter_by(user_id=session['user_id']).all()
    total = 0

    for item in items:
        product = Product.query.get(item.product_id)
        total += product.price * item.quantity

    return render_template('cart.html', items=items, total=total)


# ================= PLACE ORDER =================
@app.route('/place_order')
def place_order():
    if not session.get('user_id'):
        return redirect('/login')

    user = User.query.get(session['user_id'])
    items = Cart.query.filter_by(user_id=user.id).all()

    total = 0
    details = ""

    for item in items:
        product = Product.query.get(item.product_id)

        if product.stock < item.quantity:
            flash(f"{product.name} is out of stock!", "danger")
            return redirect('/cart')

        product.stock -= item.quantity

        subtotal = product.price * item.quantity
        total += subtotal
        details += f"{product.name} (Qty: {item.quantity}) - ₹{subtotal}\n"

    order = Order(user_id=user.id, total=total)
    db.session.add(order)
    db.session.flush()  # To get the order ID

    for item in items:
        product = Product.query.get(item.product_id)
        order_item = OrderItem(
            order_id=order.id,
            product_name=product.name,
            quantity=item.quantity,
            price=product.price
        )
        db.session.add(order_item)

    Cart.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    send_email(user.email,
               "Order Confirmation",
               f"Hello {user.name}\n\nYour Order:\n{details}\nTotal: ₹{total}\n\nThank you!")

    return redirect('/orders')


# ================= ORDERS =================
@app.route('/orders')
def orders():
    if not session.get('user_id'):
        return redirect('/login')

    orders = Order.query.filter_by(user_id=session['user_id']).all()
    return render_template('orders.html', orders=orders)


# ================= FORGOT PASSWORD =================
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = serializer.dumps(email, salt='password-reset-salt')
            reset_url = request.host_url + 'reset_password/' + token
            send_email(email, "Password Reset", f"Click here to reset: {reset_url}")
            flash("Reset link sent to your email", "info")
        else:
            flash("Email not found", "danger")
    return render_template('forgot_password.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash("Invalid or expired token", "danger")
        return redirect('/login')

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(request.url)

        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(password)
        db.session.commit()
        flash("Password updated!", "success")
        return redirect('/login')

    return render_template('reset_password.html', token=token)


if __name__ == '__main__':
    app.run(debug=True)
app = app