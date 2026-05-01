import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('JWT_SECRET', 'meeran_secret_2026')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    PORT = int(os.getenv('FLASK_PORT', 5000))

    # Database
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'al_meeran_upholstery')

    # SMTP
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = os.getenv('SMTP_USER', "adpcs006@gmail.com")
    SMTP_PASS = os.getenv('SMTP_PASS', "mnea llmx nune iovh") 
    NOTIFY_EMAIL = os.getenv('NOTIFY_EMAIL', "salehagulzar632@gmail.com")

    # Gemini AI
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    # Absolute Paths for Backend
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
    STATIC_FOLDER = os.path.join(FRONTEND_DIR, 'static')
    
    # Corrected subfolders as per actual file movement
    FABRIC_UPLOAD_PATH = os.path.join(STATIC_FOLDER, 'assets/fabrics')
    GALLERY_UPLOAD_PATH = os.path.join(STATIC_FOLDER, 'assets/images')
    QUOTES_UPLOAD_PATH = os.path.join(STATIC_FOLDER, 'assets/quotes')

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    @staticmethod
    def init_app(app):
        os.makedirs(Config.FABRIC_UPLOAD_PATH, exist_ok=True)
        os.makedirs(Config.GALLERY_UPLOAD_PATH, exist_ok=True)
        os.makedirs(Config.QUOTES_UPLOAD_PATH, exist_ok=True)
