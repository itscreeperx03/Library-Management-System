"""
verify_web_app.py
=================
End-to-End smoke test verifying all web HTML views and REST API endpoints.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
import json

def verify_all_views():
    app = create_app({'TESTING': True})
    client = app.test_client()

    pages = [
        ('/', 'Circulation & Operations Dashboard'),
        ('/books', 'Books & Inventory Catalog'),
        ('/members', 'Member Directory'),
        ('/circulation', 'Circulation Desk'),
        ('/fines', 'Decision Table for Fines'),
        ('/se-dossier', 'Software Engineering Specification Dossier'),
        ('/reports', 'Audit Reports & Function Point Estimator')
    ]

    print("[*] Testing HTML View Endpoints:")
    for path, title_fragment in pages:
        res = client.get(path)
        assert res.status_code == 200, f"Failed on {path}: {res.status_code}"
        assert title_fragment in res.data.decode('utf-8'), f"Missing expected text on {path}"
        print(f"  [+] {path.ljust(15)} -> 200 OK (Content verified)")

    print("\n[*] Testing RESTful API Endpoints:")
    api_tests = [
        ('/api/books', 'books'),
        ('/api/members', 'members'),
        ('/api/circulation/loans', 'loans'),
        ('/api/fines', 'fines'),
        ('/api/fines/decision-matrix', 'rules'),
        ('/api/se/function-points', 'analysis'),
        ('/api/dashboard/stats', 'stats')
    ]

    for path, expected_key in api_tests:
        res = client.get(path)
        assert res.status_code == 200, f"Failed on {path}: {res.status_code}"
        data = json.loads(res.data)
        assert data['success'] is True, f"Unsuccessful response on {path}"
        assert expected_key in data, f"Missing key {expected_key} on {path}"
        print(f"  [+] {path.ljust(28)} -> 200 OK (Key '{expected_key}' verified)")

    print("\n[*] Testing Live Decision Table Simulation API:")
    sim_res = client.post('/api/fines/simulate', json={
        'days_overdue': 10,
        'member_type': 'Student',
        'book_tier': 'Standard',
        'return_condition': 'Minor Damage'
    })
    assert sim_res.status_code == 200
    sim_data = json.loads(sim_res.data)['result']
    assert sim_data['gross_overdue_fine'] == 5.0
    assert sim_data['damage_fee'] == 5.0
    assert sim_data['total_fine'] == 10.0
    print(f"  [+] Fine Simulation -> Total Fine: ${sim_data['total_fine']:.2f} (Rule: {sim_data['rule_id']})")

    print("\n[SUCCESS] ALL WEB APP ENDPOINTS AND BUSINESS LOGIC FULLY OPERATIONAL!")

if __name__ == '__main__':
    verify_all_views()
