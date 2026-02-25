from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
import json
from werkzeug.utils import secure_filename
from database import init_db, DB_NAME, DB_CONFIG, get_db_connection

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Configuration
UPLOAD_FOLDER_FABRIC = '../assets/images/fabric-samples'
UPLOAD_FOLDER_GALLERY = '../assets/images/gallery'
UPLOAD_FOLDER_QUOTES = '../assets/images/quotes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app.config['UPLOAD_FOLDER_FABRIC'] = UPLOAD_FOLDER_FABRIC
app.config['UPLOAD_FOLDER_GALLERY'] = UPLOAD_FOLDER_GALLERY
app.config['UPLOAD_FOLDER_QUOTES'] = UPLOAD_FOLDER_QUOTES

# Ensure upload directories exist
os.makedirs(app.config['UPLOAD_FOLDER_FABRIC'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_GALLERY'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_QUOTES'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- API ENDPOINTS ---

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    if not conn: return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products ORDER BY created_at DESC")
    products = cursor.fetchall()
    
    for p in products:
        p['price'] = float(p['price'])
        
    cursor.close()
    conn.close()
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def add_product():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER_FABRIC'], filename)
    file.save(file_path)
    
    relative_path = f"assets/images/fabric-samples/{filename}"
    
    name = request.form['name']
    price = request.form['price']
    category = request.form.get('category', 'Fabric')

    conn = get_db_connection()
    if not conn: return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, category, image_url) VALUES (%s, %s, %s, %s)", 
                   (name, price, category, relative_path))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Product added successfully', 'image_url': relative_path}), 201

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db_connection()
    if not conn: return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product deleted'}), 200

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    conn = get_db_connection()
    if not conn: return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    
    name = request.form.get('name')
    price = request.form.get('price')
    
    if 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_FABRIC'], filename))
            image_url = f"assets/images/fabric-samples/{filename}"
            cursor.execute("UPDATE products SET name=%s, price=%s, image_url=%s WHERE id=%s", (name, price, image_url, id))
    else:
        cursor.execute("UPDATE products SET name=%s, price=%s WHERE id=%s", (name, price, id))
        
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product updated'}), 200

@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    conn = get_db_connection()
    if not conn: return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gallery ORDER BY created_at DESC")
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(projects)

@app.route('/api/gallery/<int:id>', methods=['DELETE'])
def delete_gallery_item(id):
    conn = get_db_connection()
    if not conn: return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gallery WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Gallery item deleted'}), 200

@app.route('/api/gallery/<int:id>', methods=['PUT'])
def update_gallery_item(id):
    conn = get_db_connection()
    if not conn: return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    
    title = request.form.get('title')
    category = request.form.get('category')
    
    if 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_GALLERY'], filename))
            image_url = f"assets/images/gallery/{filename}"
            cursor.execute("UPDATE gallery SET title=%s, category=%s, image_url=%s WHERE id=%s", (title, category, image_url, id))
    else:
        cursor.execute("UPDATE gallery SET title=%s, category=%s WHERE id=%s", (title, category, id))
        
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Gallery item updated'}), 200

@app.route('/api/gallery', methods=['POST'])
def add_gallery_item():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER_GALLERY'], filename)
    file.save(file_path)
    
    relative_path = f"assets/images/gallery/{filename}"
    
    title = request.form['title']
    category = request.form['category']

    conn = get_db_connection()
    if not conn: return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gallery (title, category, image_url) VALUES (%s, %s, %s)", 
                   (title, category, relative_path))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Gallery item added successfully', 'image_url': relative_path}), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    if not conn: return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
    orders = cursor.fetchall()
    
    for order in orders:
        if isinstance(order['items'], str):
            try:
                order['items'] = json.loads(order['items'])
            except:
                order['items'] = []
        order['total_price'] = float(order['total_price'])

    cursor.close()
    conn.close()
    return jsonify(orders)

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    customer = data.get('customer')
    phone = data.get('phone')
    items = json.dumps(data.get('items'))
    total = data.get('total')
    order_ref = f"ORD-{os.urandom(4).hex().upper()}"

    conn = get_db_connection()
    if not conn: return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (order_ref, customer_name, phone, items, total_price) VALUES (%s, %s, %s, %s, %s)",
                   (order_ref, customer, phone, items, total))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Order placed successfully', 'order_ref': order_ref}), 201

@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    conn = get_db_connection()
    if not conn: return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM quotes ORDER BY created_at DESC")
    quotes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(quotes)

@app.route('/api/quotes', methods=['POST'])
def create_quote():
    name = request.form.get('name')
    phone = request.form.get('phone')
    service_type = request.form.get('type')
    message = request.form.get('message')
    
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_QUOTES'], filename))
            image_url = f"assets/images/quotes/{filename}"

    conn = get_db_connection()
    if not conn: return jsonify({'error': 'Database connection failed'}), 500
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quotes (name, phone, service_type, message, image_url) VALUES (%s, %s, %s, %s, %s)",
                   (name, phone, service_type, message, image_url))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Quote submitted successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed. Please ensure MySQL is running.'}), 500
        
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful', 'token': 'dummy-token-123'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# Serve Frontend Files (for simple hosting)
@app.route('/')
def serve_index():
    return send_from_directory('../', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../', path)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
