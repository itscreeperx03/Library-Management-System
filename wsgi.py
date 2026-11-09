"""
wsgi.py
=======
Production WSGI application gateway entry point for deployment.
Compatible with Gunicorn, Waitress, uWSGI, and cloud platforms (Heroku, Render, AWS, Azure, GCP).
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()
