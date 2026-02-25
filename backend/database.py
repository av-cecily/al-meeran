import mysql.connector
from mysql.connector import Error
import os

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',  # Default XAMPP password
    'auth_plugin': 'mysql_native_password'
}

DB_NAME = 'al_meeran_upholstery'

def get_db_connection():
    """Connect to the specific database"""
    try:
        connection = mysql.connector.connect(
            database=DB_NAME,
            **DB_CONFIG
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def sync_products_from_folder():
    """Sync all images from assets/images/fabric-samples/ into the products table"""
    fabric_dir = os.path.join(os.path.dirname(__file__), '../assets/images/fabric-samples')
    if not os.path.exists(fabric_dir): return

    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    cursor.execute("SELECT image_url FROM products")
    existing_urls = {row[0] for row in cursor.fetchall()}

    new_products = []
    for filename in os.listdir(fabric_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            if 'Solo-Upholstered-Lounge-Chair' in filename: continue
            
            relative_path = f"assets/images/fabric-samples/{filename}"
            if relative_path not in existing_urls:
                name = filename.rsplit('.', 1)[0].replace('-', ' ').replace('_', ' ').title()
                new_products.append((name, 0.00, 'Fabric', relative_path))

    if new_products:
        cursor.executemany("INSERT INTO products (name, price, category, image_url) VALUES (%s, %s, %s, %s)", new_products)
        conn.commit()

    # Always ensure prices are 0 for all products
    cursor.execute("UPDATE products SET price = 0")
    conn.commit()

    cursor.close()
    conn.close()

def sync_gallery_from_folder():
    """Sync all images from assets/images/gallery/ into the gallery table"""
    gallery_dir = os.path.join(os.path.dirname(__file__), '../assets/images/gallery')
    if not os.path.exists(gallery_dir): return

    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    cursor.execute("SELECT image_url FROM gallery")
    existing_urls = {row[0] for row in cursor.fetchall()}

    new_items = []
    for filename in os.listdir(gallery_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            relative_path = f"assets/images/gallery/{filename}"
            if relative_path not in existing_urls:
                title = filename.rsplit('.', 1)[0].replace('-', ' ').replace('_', ' ').title()
                new_items.append((title, 'Project', relative_path))

    if new_items:
        cursor.executemany("INSERT INTO gallery (title, category, image_url) VALUES (%s, %s, %s)", new_items)
        conn.commit()

    cursor.close()
    conn.close()

def init_db():
    """Initialize Database and Tables"""
    try:
        # 1. Connect to MySQL Server (no DB selected)
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create Database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        
        # 2. Create Tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                category VARCHAR(100),
                image_url VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gallery (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                image_url VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_ref VARCHAR(50) UNIQUE NOT NULL,
                customer_name VARCHAR(255) NOT NULL,
                phone VARCHAR(50) NOT NULL,
                items JSON NOT NULL,
                total_price DECIMAL(10, 2) NOT NULL,
                status VARCHAR(50) DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                phone VARCHAR(50) NOT NULL,
                service_type VARCHAR(100) NOT NULL,
                message TEXT,
                image_url VARCHAR(255),
                status VARCHAR(50) DEFAULT 'New',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        # 3. Seed Data
        cursor.execute("SELECT * FROM admins WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", ('admin', 'admin123'))

        conn.commit()
        cursor.close()
        conn.close()
        
        # Syncing folders
        sync_products_from_folder()
        sync_gallery_from_folder()
        
        print("Database initialized successfully.")

    except Error as e:
        print(f"Error while initializing database: {e}")

if __name__ == '__main__':
    init_db()
