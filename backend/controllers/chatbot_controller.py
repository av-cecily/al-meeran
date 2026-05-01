from flask import request, jsonify
from services.chatbot_service import ChatbotService

chatbot_service = ChatbotService()

class ChatbotController:
    @staticmethod
    def chat():
        data = request.json
        user_msg = data.get('message')
        if not user_msg:
            return jsonify({'error': 'No message provided'}), 400
            
        reply = chatbot_service.get_response(user_msg)
        return jsonify({'reply': reply}), 200
