import sys
import os

# Add your project directory to Python path
path = '/home/yourusername/library-api'
if path not in sys.path:
    sys.path.append(path)

# Import your FastAPI app
from main import app

# For WSGI compatibility with PythonAnywhere
from fastapi.middleware.wsgi import WSGIMiddleware

# Create WSGI app
application = WSGIMiddleware(app) 