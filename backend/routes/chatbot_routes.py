from flask import Blueprint
from controllers.chatbot_controller import ChatbotController

chatbot_bp = Blueprint('chatbot', __name__)

chatbot_bp.route('', methods=['POST'])(ChatbotController.chat)
