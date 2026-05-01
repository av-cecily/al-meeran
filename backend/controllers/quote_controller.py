from flask import request, jsonify
from models.quote import Quote
from services.upload_service import UploadService
from config import Config
import os

class QuoteController:
    @staticmethod
    def get_quotes():
        quotes = Quote.get_all()
        return jsonify(quotes), 200

    @staticmethod
    def submit_quote():
        img_url = None
        if 'image' in request.files:
            file = request.files['image']
            filename = UploadService.save_file(file, Config.QUOTES_UPLOAD_PATH)
            if filename:
                img_url = f"/static/assets/images/quotes/{filename}"
        
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        service_type = request.form.get('type')
        fabric_pref = request.form.get('fabric')
        message = request.form.get('message')
        
        if Quote.create(name, phone, address, service_type, fabric_pref, message, img_url):
            return jsonify({'msg': 'Quote submitted successfully'}), 201
        return jsonify({'error': 'Failed to submit quote'}), 500
