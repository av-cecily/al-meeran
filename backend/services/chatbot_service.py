from google import genai
from config import Config
from models.product import Product

class ChatbotService:
    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY, http_options={'api_version': 'v1'})

    def get_response(self, user_message):
        try:
            fabrics = Product.get_names()
            fab_context = f"We have {', '.join(fabrics[:8])}."
            chat_context = f"You are Meeran AI expert for Al Meeran, Bahrain. {fab_context}"
            
            response = self.client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=f"{chat_context}\nUser: {user_message}"
            )
            return response.text
        except Exception as e:
            print(f"Chatbot Error: {e}")
            return "I'm experiencing heavy traffic."
