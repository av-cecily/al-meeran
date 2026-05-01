from flask import jsonify
from models.product import Product
from models.order import Order
from models.quote import Quote
from database.db_connection import DBConnection

class AnalyticsController:
    @staticmethod
    def get_stats():
        # I need to ensure Product model has get_count
        # For now I'll use a direct query or update Product model
        
        conn = DBConnection.get_connection()
        p_count = 0
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM products")
            p_count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
        o_count = Order.get_count()
        q_count = Quote.get_count()
        
        return jsonify({
            'stats': {
                'products': p_count,
                'orders': o_count,
                'quotes': q_count
            },
            'recent': []
        }), 200
