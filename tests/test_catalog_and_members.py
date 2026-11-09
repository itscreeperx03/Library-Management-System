"""
test_catalog_and_members.py
===========================
Unit and integration tests for catalog queries, filtering, member eligibility, and fine settlement.
"""

import pytest
from app.services.catalog_service import CatalogService
from app.services.member_service import MemberService
from app.services.circulation_service import CirculationService

def test_catalog_search_and_filters(app):
    db_path = app.config['DATABASE']

    # Search by keyword
    results = CatalogService.get_all_books(search='Python', db_path=db_path)
    assert len(results) >= 1
    assert any('Python' in b['title'] for b in results)

    # Filter by category
    cs_books = CatalogService.get_all_books(category='Computer Science', db_path=db_path)
    assert len(cs_books) >= 1
    assert all(b['category'] == 'Computer Science' for b in cs_books)

    # Filter by tier
    ref_books = CatalogService.get_all_books(tier='Rare/Reference', db_path=db_path)
    assert len(ref_books) >= 1
    assert all(b['tier'] == 'Rare/Reference' for b in ref_books)

    # Available copies only filter
    avail_books = CatalogService.get_all_books(available_only=True, db_path=db_path)
    assert all(b['available_copies'] > 0 for b in avail_books)

def test_prevent_book_deletion_with_active_loans(app):
    db_path = app.config['DATABASE']
    # Book 1 has an active loan in seed data
    success, msg = CatalogService.delete_book(1, db_path=db_path)
    assert success is False
    assert "active loans exist" in msg

def test_member_eligibility(app):
    db_path = app.config['DATABASE']

    # Member 1 (Active, fine within limits)
    ok, msg = MemberService.check_eligibility(1, db_path)
    assert ok is True

    # Member 6 (Suspended)
    ok_susp, msg_susp = MemberService.check_eligibility(6, db_path)
    assert ok_susp is False
    assert "Suspended" in msg_susp

def test_fine_settlement_flow(app):
    db_path = app.config['DATABASE']

    # Get unpaid fines
    unpaid = CirculationService.get_all_fines(paid_status='Unpaid', db_path=db_path)
    assert len(unpaid) > 0
    fine_to_pay = unpaid[0]

    # Settle the fine
    settle_ok, msg = CirculationService.settle_fine(fine_to_pay['id'], payment_method='Campus Card', db_path=db_path)
    assert settle_ok is True

    # Double payment should fail
    double_ok, double_msg = CirculationService.settle_fine(fine_to_pay['id'], db_path=db_path)
    assert double_ok is False
    assert "already settled" in double_msg
