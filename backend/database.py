import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Default XAMPP password
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

def init_db():
    """Initialize Database and Tables"""
    try:
        # 1. Connect to MySQL Server (no DB selected)
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create Database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' checked/created.")
        
        conn.database = DB_NAME
        
        # 2. Create Tables
        
        # Products Table
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

        # Gallery Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gallery (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                image_url VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Orders Table
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

        # Quotes Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                phone VARCHAR(50) NOT NULL,
                service_type VARCHAR(100) NOT NULL,
                message TEXT,
                status VARCHAR(50) DEFAULT 'New',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Admins Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        # 3. Seed Data
        
        # Admin
        cursor.execute("SELECT * FROM admins WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", ('admin', 'admin123'))
            print("Admin user created.")

        # Seed Products (From Frontend Data)
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            products = [
                ('Premium Velvet', 45.00, 'Fabric', 'assets/images/fabric-samples/premium-velvet.jpg'),
                ('Italian Leather', 85.00, 'Leather', 'assets/images/fabric-samples/italian-leather.jpg'),
                ('Premium Linen', 35.00, 'Fabric', 'assets/images/fabric-samples/premium-linen.jpg'),
                ('Modern Tweed', 40.00, 'Fabric', 'assets/images/fabric-samples/modern-tweed.jpg'),
                ('Royal Silk', 65.00, 'Silk', 'assets/images/fabric-samples/royal-silk.jpg'),
                ('Cotton Canvas', 25.00, 'Fabric', 'assets/images/fabric-samples/cotton-canvas.jpg')
            ]
            cursor.executemany("INSERT INTO products (name, price, category, image_url) VALUES (%s, %s, %s, %s)", products)
            print("Products seeded.")

        # Seed Gallery (From Frontend Data)
        cursor.execute("SELECT COUNT(*) FROM gallery")
        if cursor.fetchone()[0] == 0:
            gallery_items = [
                ('Royal Velvet Suite', 'luxury', 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?q=80&w=800&auto=format&fit=crop'),
                ('Minimalist Tan Leather', 'modern', 'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?q=80&w=800&auto=format&fit=crop'),
                ('Royal Blue Chesterfield', 'classic', 'https://images.unsplash.com/photo-1540518614846-7eded433c457?q=80&w=800&auto=format&fit=crop'),
                ('Contemporary Accent Chair', 'modern', 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?q=80&w=800&auto=format&fit=crop'),
                ('Modern Suite Integration', 'modern', 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?q=80&w=800&auto=format&fit=crop'),
                ('Golden Era Armchair', 'classic', 'https://images.unsplash.com/photo-1592078615290-033ee584e267?q=80&w=800&auto=format&fit=crop')
            ]
            cursor.executemany("INSERT INTO gallery (title, category, image_url) VALUES (%s, %s, %s)", gallery_items)
            print("Gallery seeded.")

        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully.")

    except Error as e:
        print(f"Error while initializing database: {e}")

if __name__ == '__main__':
    init_db()
