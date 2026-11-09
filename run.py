"""
run.py
======
Local development entry point for the Athena Library Management System.
"""

import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    print("=" * 70)
    print("   ATHENA LIBRARY MANAGEMENT SYSTEM (LMS) - WEB APP")
    print("   Software Engineering Minor Project #1 (Iterative Waterfall)")
    print("=" * 70)
    print(f" * Server running on: http://{host}:{port}")
    print(f" * Interactive Web UI: http://{host}:{port}/")
    print(f" * Decision Table Simulator: http://{host}:{port}/fines")
    print(f" * Software Engineering Dossier: http://{host}:{port}/se-dossier")
    print(f" * Function Point Engine: http://{host}:{port}/reports")
    print("=" * 70)
    app.run(host=host, port=port, debug=True)
