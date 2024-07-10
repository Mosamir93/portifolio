"""
This file initializes the Flask application
and its routes.
"""
from flask import Flask

def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    
    with app.app_context():
        from . import routes
        routes.init_app(app)
    
    return app
