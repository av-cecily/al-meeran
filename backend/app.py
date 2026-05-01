from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.gallery_routes import gallery_bp
from routes.order_routes import order_bp
from routes.quote_routes import quote_bp
from routes.chatbot_routes import chatbot_bp
from routes.analytics_routes import analytics_bp
from routes.visualizer_routes import visualizer_bp
import os

# Initialize Flask with separate static folder and url path
app = Flask(__name__, 
            static_folder=Config.STATIC_FOLDER, 
            static_url_path='/static',
            template_folder=Config.FRONTEND_DIR)

CORS(app)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api/products')
app.register_blueprint(gallery_bp, url_prefix='/api/gallery')
app.register_blueprint(order_bp, url_prefix='/api/orders')
app.register_blueprint(quote_bp, url_prefix='/api/quotes')
app.register_blueprint(chatbot_bp, url_prefix='/api/chat')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(visualizer_bp, url_prefix='/api/visualize')

@app.route('/')
def serve_index():
    return send_from_directory(Config.FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    # 1. Try to serve from frontend root (HTML files)
    if os.path.exists(os.path.join(Config.FRONTEND_DIR, path)):
        return send_from_directory(Config.FRONTEND_DIR, path)
    
    # 2. If it's an API or Static asset that reached here, it's a real 404
    if path.startswith('api/') or path.startswith('static/'):
        return jsonify({'error': 'Not Found'}), 404
        
    # 3. Fallback to index.html ONLY for potential SPA routes
    return send_from_directory(Config.FRONTEND_DIR, 'index.html')

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
