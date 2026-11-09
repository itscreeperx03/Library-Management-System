"""
conftest.py
===========
Pytest test fixtures and temporary isolated test database configuration.
"""

import pytest
import os
import tempfile
from app import create_app
from app.database import init_db

@pytest.fixture
def app():
    # Create a temporary file to isolate the test database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db(db_path)

    yield app

    os.close(db_fd)
    try:
        os.unlink(db_path)
    except PermissionError:
        pass

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
