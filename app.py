from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(_name_)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    # Check if table is empty
    c.execute("SELECT COUNT(*) FROM products")
    count = c.fetchone()[0]
    
    # If empty, insert sample products
    if count == 0:
        sample_products = [
            ("Smart TV", 599.99),
            ("Wireless Headphones", 99.99),
            ("Bluetooth Speaker", 49.99),
            ("Gaming Laptop", 1299.99),
            ("Smartphone", 799.99),
            ("Coffee Maker", 89.99),
            ("Air Fryer", 129.99),
            ("Electric Kettle", 39.99),
            ("Blender", 59.99),
            ("Toaster", 29.99),
            ("Leather Wallet", 49.99),
            ("Running Shoes", 119.99),
            ("Sunglasses", 69.99),
            ("Hoodie", 39.99),
            ("Watch", 199.99)
        ]
        c.executemany("INSERT INTO products (name, price) VALUES (?, ?)", sample_products)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        conn.close()
        
        return redirect('/')
    return render_template('add_product.html')

if _name_ == '_main_':
    init_db()
    app.run(debug=True)
