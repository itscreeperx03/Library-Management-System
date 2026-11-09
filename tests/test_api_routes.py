"""
test_api_routes.py
==================
Integration testing of REST API endpoints for catalog, circulation, fines, and SE metrics.
"""

import json
import pytest

def test_api_get_books(client):
    response = client.get('/api/books')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['count'] > 0
    assert len(data['books']) > 0

def test_api_add_and_delete_book(client):
    new_book = {
        'isbn': '978-0001112223',
        'title': 'Test Software Engineering Book',
        'author': 'Prof. Academic',
        'category': 'Software Engineering',
        'tier': 'Course Reserve',
        'total_copies': 2,
        'replacement_cost': 60.0,
        'shelf_location': 'TEST-01'
    }
    # Add book
    res = client.post('/api/books', json=new_book)
    assert res.status_code == 201
    book_data = json.loads(res.data)
    assert book_data['success'] is True
    book_id = book_data['book']['id']

    # Delete book
    del_res = client.delete(f'/api/books/{book_id}')
    assert del_res.status_code == 200
    del_data = json.loads(del_res.data)
    assert del_data['success'] is True

def test_api_members(client):
    # Fetch members
    res = client.get('/api/members')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['success'] is True
    assert data['count'] > 0

    # Add new member
    new_m = {
        'member_code': 'MEM-TST-999',
        'name': 'Integration Test User',
        'email': 'tester@campus.edu',
        'phone': '1234567890',
        'member_type': 'Student'
    }
    create_res = client.post('/api/members', json=new_m)
    assert create_res.status_code == 201

def test_api_fine_simulation(client):
    payload = {
        'days_overdue': 12,
        'member_type': 'Student',
        'book_tier': 'Standard',
        'return_condition': 'Normal'
    }
    res = client.post('/api/fines/simulate', json=payload)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['success'] is True
    assert data['result']['total_fine'] == 6.00 # 12 * 0.50
    assert data['result']['rule_id'] == 'R-STU-T2-STD'

def test_api_decision_matrix(client):
    res = client.get('/api/fines/decision-matrix')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['success'] is True
    assert len(data['rules']) == 27

def test_api_function_points(client):
    res = client.get('/se/function-points', base_url='http://localhost/api')
    # Or call directly via url_prefix
    res2 = client.get('/api/se/function-points')
    assert res2.status_code == 200
    data = json.loads(res2.data)
    assert data['success'] is True
    assert data['analysis']['unadjusted_fp'] > 0
    assert data['analysis']['adjusted_fp'] > 0

def test_api_dashboard_stats(client):
    res = client.get('/api/dashboard/stats')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['success'] is True
    assert 'total_unique_titles' in data['stats']
    assert 'active_loans' in data['stats']
