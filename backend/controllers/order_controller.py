from flask import request, jsonify
from models.order import Order
import os

class OrderController:
    @staticmethod
    def get_orders():
        orders = Order.get_all()
        return jsonify(orders), 200

    @staticmethod
    def create_order():
        data = request.json
        ref = f"ORD-{os.urandom(4).hex().upper()}"
        customer = data.get('customer')
        phone = data.get('phone')
        address = data.get('address')
        items = data.get('items')
        total = data.get('total')
        
        if Order.create(ref, customer, phone, address, items, total):
            return jsonify({'order_ref': ref}), 201
        return jsonify({'error': 'Failed to create order'}), 500
