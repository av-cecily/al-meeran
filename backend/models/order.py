import json
from database.db_connection import DBConnection

class Order:
    @staticmethod
    def get_all():
        conn = DBConnection.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
            orders = cursor.fetchall()
            for o in orders:
                o['total_price'] = float(o['total_price'])
                try:
                    o['items'] = json.loads(o['items']) if isinstance(o['items'], str) else o['items']
                except:
                    o['items'] = []
            return orders
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create(order_ref, customer_name, phone, address, items, total_price):
        conn = DBConnection.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO orders (order_ref, customer_name, phone, address, items, total_price) VALUES (%s, %s, %s, %s, %s, %s)", 
                           (order_ref, customer_name, phone, address, json.dumps(items), total_price))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()
            
    @staticmethod
    def get_count():
        conn = DBConnection.get_connection()
        if not conn: return 0
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as t FROM orders")
            return cursor.fetchone()['t']
        finally:
            cursor.close()
            conn.close()
