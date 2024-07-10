"""
This file serves as the entry point
for running the Flask application.
"""
from . import create_app

app = create_app()

if __name__ == "__main__":
    """
    Run the Flask application.
    """
    app.run(host='0.0.0.0', port=5000)
