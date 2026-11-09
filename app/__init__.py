"""
Library Management System (LMS)
Flask Application Package Factory
"""

import os
from flask import Flask, render_template
from app.database import init_db

def create_app(test_config=None):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    default_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'library.db')

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'lms-super-secure-production-key-2026'),
        DATABASE=default_db
    )

    if test_config:
        app.config.update(test_config)

    # Initialize SQLite database schema and seed data
    init_db(app.config['DATABASE'])

    # Register blueprints
    from app.routes.views import views_bp
    from app.routes.api import api_bp

    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('base.html', error_message="Page Not Found (404)"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('base.html', error_message="Internal Server Error (500)"), 500

    return app
