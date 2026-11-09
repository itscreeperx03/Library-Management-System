"""
test_fine_calculator.py
=======================
Exhaustive verification of the FineDecisionTable rule engine.
Validates all condition/action combinations, boundary values, and statutory caps.
"""

import pytest
from app.services.fine_calculator import FineDecisionTable

def test_grace_period_zero_fine():
    """Rule R0: Return within 2 days grace period incurs zero overdue fine."""
    for days in [0, 1, 2]:
        result = FineDecisionTable.calculate(days_overdue=days, member_type='Student', book_tier='Standard', return_condition='Normal')
        assert result.total_fine == 0.0
        assert result.is_grace_period is True
        assert result.rule_id == 'R0-GRACE'
        assert result.account_action == 'Normal'

def test_grace_period_with_damage():
    """Rule R0 with physical damage: Overdue fine waived, but damage penalty applied."""
    result = FineDecisionTable.calculate(days_overdue=1, member_type='Student', book_tier='Standard', return_condition='Minor Damage')
    assert result.capped_overdue_fine == 0.0
    assert result.damage_fee == 5.0
    assert result.total_fine == 5.0
    assert result.account_action == 'Warning'

def test_student_tier1_standard_book():
    """Rule R-STU-T1-STD: Student 4 days overdue on standard book ($0.50 * 4 * 1.0 = $2.00)."""
    result = FineDecisionTable.calculate(days_overdue=4, member_type='Student', book_tier='Standard')
    assert result.days_overdue == 4
    assert result.base_rate == 0.50
    assert result.tier_multiplier == 1.0
    assert result.gross_overdue_fine == 2.00
    assert result.capped_overdue_fine == 2.00
    assert result.total_fine == 2.00
    assert result.is_capped is False
    assert result.rule_id == 'R-STU-T1-STD'
    assert result.account_action == 'Normal'

def test_student_tier1_course_reserve():
    """Rule R-STU-T1-CR: Student 5 days overdue on Course Reserve (2x multiplier) -> $0.50 * 5 * 2.0 = $5.00."""
    result = FineDecisionTable.calculate(days_overdue=5, member_type='Student', book_tier='Course Reserve')
    assert result.gross_overdue_fine == 5.00
    assert result.total_fine == 5.00
    assert result.rule_id == 'R-STU-T1-CR'

def test_student_tier2_rare_reference():
    """Rule R-STU-T2-REF: Student 10 days overdue on Rare/Ref (3x multiplier) -> $0.50 * 10 * 3.0 = $15.00."""
    result = FineDecisionTable.calculate(days_overdue=10, member_type='Student', book_tier='Rare/Reference')
    assert result.gross_overdue_fine == 15.00
    assert result.capped_overdue_fine == 15.00
    assert result.total_fine == 15.00
    assert result.rule_id == 'R-STU-T2-REF'
    assert result.account_action == 'Warning'

def test_student_cap_enforcement():
    """Student fine cap is $20.00. 50 days overdue at $0.50/day would be $25.00, but capped at $20.00."""
    result = FineDecisionTable.calculate(days_overdue=50, member_type='Student', book_tier='Standard')
    assert result.gross_overdue_fine == 25.00
    assert result.capped_overdue_fine == 20.00
    assert result.total_fine == 20.00
    assert result.is_capped is True
    assert result.account_action == 'Suspended'

def test_faculty_rates_and_cap():
    """Faculty base rate is $0.20/day, cap is $30.00."""
    # 10 days overdue on standard book = $2.00
    res1 = FineDecisionTable.calculate(days_overdue=10, member_type='Faculty', book_tier='Standard')
    assert res1.total_fine == 2.00
    assert res1.rule_id == 'R-FAC-T2-STD'

    # 200 days overdue: 200 * 0.20 = $40.00 -> Capped at $30.00
    res2 = FineDecisionTable.calculate(days_overdue=200, member_type='Faculty', book_tier='Standard')
    assert res2.capped_overdue_fine == 30.00
    assert res2.total_fine == 30.00
    assert res2.is_capped is True

def test_guest_rates_and_cap():
    """Guest base rate is $1.00/day, cap is $50.00."""
    # 5 days overdue on Course Reserve: 5 * $1.00 * 2.0 = $10.00
    res1 = FineDecisionTable.calculate(days_overdue=5, member_type='Guest', book_tier='Course Reserve')
    assert res1.total_fine == 10.00
    assert res1.rule_id == 'R-GST-T1-CR'

    # 60 days overdue on Rare: 60 * 1 * 3 = $180 -> Capped at $50.00
    res2 = FineDecisionTable.calculate(days_overdue=60, member_type='Guest', book_tier='Rare/Reference')
    assert res2.capped_overdue_fine == 50.00
    assert res2.total_fine == 50.00
    assert res2.is_capped is True

def test_lost_item_rule():
    """Lost item incurs Replacement Cost + $10 Fee, bypasses overdue fine cap, account suspended."""
    result = FineDecisionTable.calculate(days_overdue=30, member_type='Student', book_tier='Standard',
                                         return_condition='Lost', replacement_cost=75.00)
    assert result.rule_id == 'R16-LOST'
    assert result.damage_fee == 0.0
    assert result.replacement_fee == 85.00 # 75 + 10
    assert result.total_fine == 85.00
    assert result.account_action == 'Suspended'

def test_severe_damage_penalty():
    """Severe physical damage incurs +$15.00 penalty added to overdue fine."""
    result = FineDecisionTable.calculate(days_overdue=6, member_type='Student', book_tier='Standard',
                                         return_condition='Severe Damage')
    # 6 * 0.50 = $3.00 overdue + $15.00 damage = $18.00
    assert result.capped_overdue_fine == 3.00
    assert result.damage_fee == 15.00
    assert result.total_fine == 18.00

def test_boundary_values():
    """Boundary Value Analysis: test exactly at transition points D=2, D=3, D=7, D=8, D=21, D=22."""
    # D=2 -> Grace period ($0)
    assert FineDecisionTable.calculate(2, 'Student').total_fine == 0.0
    # D=3 -> Tier 1 ($1.50)
    assert FineDecisionTable.calculate(3, 'Student').total_fine == 1.50
    # D=7 -> Tier 1 upper limit ($3.50)
    assert FineDecisionTable.calculate(7, 'Student').total_fine == 3.50
    # D=8 -> Tier 2 lower limit ($4.00)
    assert FineDecisionTable.calculate(8, 'Student').total_fine == 4.00
    # D=21 -> Tier 2 upper limit ($10.50)
    assert FineDecisionTable.calculate(21, 'Student').total_fine == 10.50
    # D=22 -> Tier 3 lower limit ($11.00)
    assert FineDecisionTable.calculate(22, 'Student').total_fine == 11.00

def test_decision_matrix_generation():
    """Verify that full decision matrix generator returns all 27 canonical rules."""
    matrix = FineDecisionTable.get_decision_matrix()
    assert len(matrix) == 27
    assert matrix[0]['rule_number'] == 'R01'
    assert matrix[-1]['rule_number'] == 'R27'
