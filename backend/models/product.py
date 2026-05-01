from database.db_connection import DBConnection

class Product:
    @staticmethod
    def get_all():
        conn = DBConnection.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products ORDER BY created_at DESC")
            products = cursor.fetchall()
            for p in products: p['price'] = float(p['price'])
            return products
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create(name, price, category, image_url):
        conn = DBConnection.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, category, image_url) VALUES (%s, %s, %s, %s)", 
                           (name, price, category, image_url))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete(product_id):
        conn = DBConnection.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_names():
        conn = DBConnection.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT name FROM products")
            return [p['name'] for p in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()
