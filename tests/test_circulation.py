"""
test_circulation.py
===================
Unit and integration tests for circulation workflows: Issue, Return, Renew, and Reserve.
"""

import pytest
from app.services.circulation_service import CirculationService
from app.services.catalog_service import CatalogService
from app.services.member_service import MemberService

def test_successful_issue_book(app):
    db_path = app.config['DATABASE']
    # Member 3 (Faculty) borrows Book 1 (Effective Java)
    # Check initial available copies
    book_before = CatalogService.get_book_by_id(1, db_path)
    initial_avail = book_before['available_copies']

    success, msg, record = CirculationService.issue_book(1, 3, due_days=14, notes="Test Loan", db_path=db_path)
    assert success is True, f"Issue failed: {msg}"
    assert record is not None
    assert record['book_id'] == 1
    assert record['member_id'] == 3

    # Verify inventory was decremented
    book_after = CatalogService.get_book_by_id(1, db_path)
    assert book_after['available_copies'] == initial_avail - 1

def test_prevent_duplicate_issue(app):
    db_path = app.config['DATABASE']
    # Try borrowing the same book again while still holding it
    success, msg, _ = CirculationService.issue_book(1, 1, db_path=db_path)
    assert success is False
    assert "already has an active loan" in msg

def test_block_issue_to_suspended_member(app):
    db_path = app.config['DATABASE']
    # Member 6 is pre-seeded as Suspended
    success, msg, _ = CirculationService.issue_book(2, 6, db_path=db_path)
    assert success is False
    assert "Suspended" in msg

def test_block_issue_when_out_of_stock(app):
    db_path = app.config['DATABASE']
    # Book 8 (Knuth) is pre-seeded with 0 available copies
    success, msg, _ = CirculationService.issue_book(8, 3, db_path=db_path)
    assert success is False
    assert "No copies currently available" in msg

def test_return_book_clean(app):
    db_path = app.config['DATABASE']
    # Member 2 issues book 7 then returns it cleanly
    success, _, record = CirculationService.issue_book(7, 2, due_days=14, db_path=db_path)
    assert success is True
    loan_id = record['id']

    book_before = CatalogService.get_book_by_id(7, db_path)
    avail_before = book_before['available_copies']

    ret_success, ret_msg, ret_data = CirculationService.return_book(loan_id, return_condition='Normal', db_path=db_path)
    assert ret_success is True
    assert ret_data['fine_details']['total_fine'] == 0.0

    # Verify book restocked
    book_after = CatalogService.get_book_by_id(7, db_path)
    assert book_after['available_copies'] == avail_before + 1

def test_return_book_with_simulated_overdue_and_fine(app):
    db_path = app.config['DATABASE']
    # Issue book 9 to Member 3 (Faculty)
    success, _, record = CirculationService.issue_book(9, 3, due_days=10, db_path=db_path)
    loan_id = record['id']

    # Simulate return 15 days later (5 days overdue -> Tier 1 for Faculty on Standard book = $0.20 * 5 = $1.00)
    # Plus simulated minor damage (+$5.00) = $6.00 total fine
    ret_success, _, ret_data = CirculationService.return_book(
        loan_id,
        return_condition='Minor Damage',
        return_date_str='2026-12-01', # Way past due date
        db_path=db_path
    )
    assert ret_success is True
    assert ret_data['fine_id'] is not None
    assert ret_data['fine_details']['total_fine'] > 0.0
    assert ret_data['fine_details']['damage_fee'] == 5.0

def test_renew_book_success_and_limit(app):
    db_path = app.config['DATABASE']
    # Issue book 10 to Member 4
    success, _, record = CirculationService.issue_book(10, 4, due_days=14, db_path=db_path)
    loan_id = record['id']

    # 1st renewal
    ren1_ok, msg1, d1 = CirculationService.renew_book(loan_id, additional_days=14, db_path=db_path)
    assert ren1_ok is True
    assert d1['renewals_count'] == 1

    # 2nd renewal
    ren2_ok, msg2, d2 = CirculationService.renew_book(loan_id, additional_days=14, db_path=db_path)
    assert ren2_ok is True
    assert d2['renewals_count'] == 2

    # 3rd renewal - should be blocked by policy limit (max 2)
    ren3_ok, msg3, _ = CirculationService.renew_book(loan_id, additional_days=14, db_path=db_path)
    assert ren3_ok is False
    assert "Maximum renewal limit" in msg3

def test_reserve_book(app):
    db_path = app.config['DATABASE']
    # Member 1 reserves out-of-stock Book 8
    res_ok, msg = CirculationService.reserve_book(8, 1, db_path=db_path)
    assert res_ok is True

    # Duplicate reservation should fail
    dup_ok, dup_msg = CirculationService.reserve_book(8, 1, db_path=db_path)
    assert dup_ok is False
    assert "already have a pending reservation" in dup_msg
