from flask import request, jsonify
from models.gallery import Gallery
from services.upload_service import UploadService
from config import Config
import os

class GalleryController:
    @staticmethod
    def get_gallery():
        items = Gallery.get_all()
        return jsonify(items), 200

    @staticmethod
    def add_gallery_item():
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        filename = UploadService.save_file(file, Config.GALLERY_UPLOAD_PATH)
        
        if not filename:
            return jsonify({'error': 'Invalid file type'}), 400
            
        path = f"static/assets/images/gallery/{filename}"
        title = request.form.get('title')
        category = request.form.get('category', 'Classic')
        
        if Gallery.create(title, category, path):
            return jsonify({'message': 'Gallery item added successfully'}), 201
        return jsonify({'error': 'Failed to add gallery item'}), 500

    @staticmethod
    def delete_gallery_item(id):
        if Gallery.delete(id):
            return jsonify({'message': 'Gallery item deleted successfully'}), 200
        return jsonify({'error': 'Item not found or failed to delete'}), 404
