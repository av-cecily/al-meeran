import os
import sys

# Get the absolute path of the project root
project_root = os.path.abspath(os.path.dirname(__file__))
backend_path = os.path.join(project_root, 'backend')

# Add backend to Python path so we can import from it
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# We do NOT change directory here to keep the Flask reloader stable
from app import app

if __name__ == '__main__':
    print("--- Al Meeran Upholstery: Enterprise Management System ---")
    print("Backend API: http://localhost:5000")
    print("Frontend: http://localhost:5000")
    print("-----------------------------------------------------------")
    app.run(debug=True, port=5000)
