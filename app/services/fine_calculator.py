"""
fine_calculator.py
==================
Formal Decision Table Engine for Library Overdue Fines and Damage Assessments.
Directly implements the academic syllabus decision matrix for the Library Management System.
"""

from typing import Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class FineCalculationResult:
    days_overdue: int
    member_type: str
    book_tier: str
    return_condition: str
    base_rate: float
    tier_multiplier: float
    gross_overdue_fine: float
    capped_overdue_fine: float
    damage_fee: float
    replacement_fee: float
    total_fine: float
    is_grace_period: bool
    is_capped: bool
    rule_id: str
    rule_name: str
    explanation: str
    account_action: str
    repeat_defaulter: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            'days_overdue': self.days_overdue,
            'member_type': self.member_type,
            'book_tier': self.book_tier,
            'return_condition': self.return_condition,
            'repeat_defaulter': self.repeat_defaulter,
            'base_rate': round(self.base_rate, 2),
            'tier_multiplier': round(self.tier_multiplier, 2),
            'gross_overdue_fine': round(self.gross_overdue_fine, 2),
            'capped_overdue_fine': round(self.capped_overdue_fine, 2),
            'damage_fee': round(self.damage_fee, 2),
            'replacement_fee': round(self.replacement_fee, 2),
            'total_fine': round(self.total_fine, 2),
            'is_grace_period': self.is_grace_period,
            'is_capped': self.is_capped,
            'rule_id': self.rule_id,
            'rule_name': self.rule_name,
            'explanation': self.explanation,
            'account_action': self.account_action
        }

class FineDecisionTable:
    """
    Formal Decision Table implementation for fines calculation.

    Condition Stubs:
    C1: Member Type {Student, Faculty, Guest}
    C2: Days Overdue {D <= 2 [Grace], 3 <= D <= 7 [Tier 1], 8 <= D <= 21 [Tier 2], D > 21 [Tier 3]}
    C3: Book Tier {Standard, Course Reserve, Rare/Reference}
    C4: Return Condition {Normal, Minor Damage, Severe Damage, Lost}

    Action Stubs:
    A1: Assign Base Daily Rate ($0.50 for Student, $0.20 for Faculty, $1.00 for Guest)
    A2: Assign Category Multiplier (1.0x Standard, 2.0x Reserve, 3.0x Rare)
    A3: Apply Grace Exemption (Fine = $0 if D <= 2 and condition != Lost)
    A4: Apply Overdue Cap (Student $20, Faculty $30, Guest $50)
    A5: Assess Damage/Loss Penalty ($5 Minor, $15 Severe, Cost + $10 Lost)
    A6: Set Account Status Action (Normal, Warning, Suspended)
    """

    BASE_RATES = {
        'Student': 0.50,
        'Faculty': 0.20,
        'Guest': 1.00
    }

    TIER_MULTIPLIERS = {
        'Standard': 1.0,
        'Course Reserve': 2.0,
        'Rare/Reference': 3.0
    }

    FINE_CAPS = {
        'Student': 20.0,
        'Faculty': 30.0,
        'Guest': 50.0
    }

    DAMAGE_FEES = {
        'Normal': 0.0,
        'Minor Damage': 5.0,
        'Severe Damage': 15.0
    }

    LOST_PROCESSING_FEE = 10.0
    GRACE_PERIOD_DAYS = 2

    @classmethod
    def calculate(cls, days_overdue: int, member_type: str, book_tier: str = 'Standard',
                  return_condition: str = 'Normal', replacement_cost: float = 50.0,
                  repeat_defaulter: bool = False) -> FineCalculationResult:
        """
        Evaluate conditions against decision table rules and return detailed fine result.
        """
        # Normalize and validate inputs
        days_overdue = max(0, int(days_overdue))
        member_type = member_type if member_type in cls.BASE_RATES else 'Student'
        book_tier = book_tier if book_tier in cls.TIER_MULTIPLIERS else 'Standard'
        return_condition = return_condition if return_condition in ('Normal', 'Minor Damage', 'Severe Damage', 'Lost') else 'Normal'
        replacement_cost = max(0.0, float(replacement_cost))
        repeat_defaulter = bool(repeat_defaulter)

        base_rate = cls.BASE_RATES[member_type]
        multiplier = cls.TIER_MULTIPLIERS[book_tier]
        fine_cap = cls.FINE_CAPS[member_type]

        # Case 1: Lost Book (Rule R16 - Special Terminal Rule)
        if return_condition == 'Lost':
            rule_id = 'R16-LOST'
            rule_name = 'Lost Item Replacement Rule'
            damage_fee = 0.0
            replacement_fee = replacement_cost + cls.LOST_PROCESSING_FEE
            # Overdue fee waived in favor of replacement fee + handling
            capped_overdue = 0.0
            gross_overdue = 0.0
            total_fine = replacement_fee
            explanation = (f"Book declared Lost. Full replacement cost (${replacement_cost:.2f}) "
                           f"plus ${cls.LOST_PROCESSING_FEE:.2f} administrative processing fee assessed.")
            account_action = 'Suspended'
            return FineCalculationResult(
                days_overdue=days_overdue,
                member_type=member_type,
                book_tier=book_tier,
                return_condition=return_condition,
                base_rate=base_rate,
                tier_multiplier=multiplier,
                gross_overdue_fine=gross_overdue,
                capped_overdue_fine=capped_overdue,
                damage_fee=damage_fee,
                replacement_fee=replacement_fee,
                total_fine=total_fine,
                is_grace_period=False,
                is_capped=False,
                rule_id=rule_id,
                rule_name=rule_name,
                explanation=explanation,
                account_action=account_action,
                repeat_defaulter=repeat_defaulter
            )

        # Case 2: Within Grace Period (Rule R0)
        damage_fee = cls.DAMAGE_FEES.get(return_condition, 0.0)
        if days_overdue <= cls.GRACE_PERIOD_DAYS:
            rule_id = 'R0-GRACE'
            rule_name = 'Grace Period Exemption'
            gross_overdue = 0.0
            capped_overdue = 0.0
            replacement_fee = 0.0
            total_fine = damage_fee
            if damage_fee > 0:
                explanation = (f"Within {cls.GRACE_PERIOD_DAYS}-day grace period (overdue fine waived: $0.00). "
                               f"Physical condition penalty assessed: ${damage_fee:.2f} ({return_condition}).")
                account_action = 'Suspended' if return_condition == 'Severe Damage' else 'Warning'
            else:
                explanation = f"Within {cls.GRACE_PERIOD_DAYS}-day grace period. Zero fine assessed."
                account_action = 'Normal'

            return FineCalculationResult(
                days_overdue=days_overdue,
                member_type=member_type,
                book_tier=book_tier,
                return_condition=return_condition,
                base_rate=base_rate,
                tier_multiplier=multiplier,
                gross_overdue_fine=gross_overdue,
                capped_overdue_fine=capped_overdue,
                damage_fee=damage_fee,
                replacement_fee=replacement_fee,
                total_fine=total_fine,
                is_grace_period=True,
                is_capped=False,
                rule_id=rule_id,
                rule_name=rule_name,
                explanation=explanation,
                account_action=account_action,
                repeat_defaulter=repeat_defaulter
            )

        # Case 3: Overdue Days > Grace Period -> Apply Decision Rules
        gross_overdue = days_overdue * base_rate * multiplier
        if repeat_defaulter and days_overdue >= 8:
            gross_overdue = round(gross_overdue * 1.20, 2)

        is_capped = gross_overdue >= fine_cap
        capped_overdue = min(gross_overdue, fine_cap)
        replacement_fee = 0.0
        total_fine = capped_overdue + damage_fee

        # Determine Tier Rule
        if 3 <= days_overdue <= 7:
            tier_code = "T1"
            tier_label = "Short Overdue (3-7 days)"
            account_action = 'Suspended' if return_condition == 'Severe Damage' else ('Normal' if damage_fee == 0 else 'Warning')
        elif 8 <= days_overdue <= 21:
            tier_code = "T2"
            tier_label = "Moderate Overdue (8-21 days)"
            account_action = 'Suspended' if return_condition == 'Severe Damage' else 'Warning'
        else: # days_overdue > 21
            tier_code = "T3"
            tier_label = "Severe Overdue (>21 days)"
            account_action = 'Suspended'

        # Synthesize Rule ID
        prefix_map = {'Student': 'STU', 'Faculty': 'FAC', 'Guest': 'GST'}
        tier_map = {'Standard': 'STD', 'Course Reserve': 'CR', 'Rare/Reference': 'REF'}
        cond_map = {'Normal': 'OK', 'Minor Damage': 'MIN', 'Severe Damage': 'SEV'}

        rule_id = f"R-{prefix_map[member_type]}-{tier_code}-{tier_map[book_tier]}"
        rule_name = f"{member_type} {tier_label} [{book_tier}]"

        cap_note = f" (Capped at maximum limit of ${fine_cap:.2f})" if is_capped else ""
        damage_note = f" plus ${damage_fee:.2f} {return_condition} fee" if damage_fee > 0 else ""
        surcharge_note = " (includes 20% repeat defaulter surcharge)" if (repeat_defaulter and days_overdue >= 8) else ""
        explanation = (f"{days_overdue} days overdue at base rate ${base_rate:.2f}/day "
                       f"x {multiplier:.1f} multiplier for {book_tier} = ${gross_overdue:.2f}{surcharge_note}{cap_note}{damage_note}.")

        return FineCalculationResult(
            days_overdue=days_overdue,
            member_type=member_type,
            book_tier=book_tier,
            return_condition=return_condition,
            base_rate=base_rate,
            tier_multiplier=multiplier,
            gross_overdue_fine=gross_overdue,
            capped_overdue_fine=capped_overdue,
            damage_fee=damage_fee,
            replacement_fee=replacement_fee,
            total_fine=total_fine,
            is_grace_period=False,
            is_capped=is_capped,
            rule_id=rule_id,
            rule_name=rule_name,
            explanation=explanation,
            account_action=account_action,
            repeat_defaulter=repeat_defaulter
        )

    @classmethod
    def get_decision_matrix(cls) -> list:
        """
        Returns full structured table of rules for documentation display and interactive viewer.
        """
        matrix = []
        rule_num = 1
        for m_type, b_rate in cls.BASE_RATES.items():
            for b_tier, mult in cls.TIER_MULTIPLIERS.items():
                for overdue_range, d_sample in [('3-7 Days (Tier 1)', 5), ('8-21 Days (Tier 2)', 14), ('> 21 Days (Tier 3)', 30)]:
                    res = cls.calculate(d_sample, m_type, b_tier, 'Normal')
                    matrix.append({
                        'rule_number': f"R{rule_num:02d}",
                        'member_type': m_type,
                        'days_range': overdue_range,
                        'book_tier': b_tier,
                        'base_rate': f"${b_rate:.2f}",
                        'multiplier': f"{mult}x",
                        'effective_rate': f"${(b_rate * mult):.2f}/day",
                        'sample_calc_days': d_sample,
                        'sample_overdue_fine': f"${res.capped_overdue_fine:.2f}",
                        'max_cap': f"${cls.FINE_CAPS[m_type]:.2f}",
                        'is_capped_in_sample': res.is_capped,
                        'action': res.account_action
                    })
                    rule_num += 1
        return matrix
