from flask import request, jsonify
from services.upload_service import UploadService

class VisualizerController:
    @staticmethod
    def process():
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
            
        file = request.files['image']
        try:
            result = UploadService.process_visualizer_image(file.stream)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
