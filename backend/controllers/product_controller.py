from flask import request, jsonify
from models.product import Product
from services.upload_service import UploadService
from config import Config
import os

class ProductController:
    @staticmethod
    def get_products():
        products = Product.get_all()
        return jsonify(products), 200

    @staticmethod
    def add_product():
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        filename = UploadService.save_file(file, Config.FABRIC_UPLOAD_PATH)
        
        if not filename:
            return jsonify({'error': 'Invalid file type'}), 400
            
        path = f"static/assets/images/fabric-samples/{filename}"
        name = request.form.get('name')
        price = request.form.get('price', 0)
        category = request.form.get('category', 'Classic')
        
        if Product.create(name, price, category, path):
            return jsonify({'message': 'Product added successfully'}), 201
        return jsonify({'error': 'Failed to add product'}), 500

    @staticmethod
    def delete_product(id):
        if Product.delete(id):
            return jsonify({'message': 'Product deleted successfully'}), 200
        return jsonify({'error': 'Product not found or failed to delete'}), 404
