"""
fp_service.py
=============
Function Point (FP) Analysis Service following the IFPUG / Albrecht standard.
Provides formal mathematical calculation of Unadjusted Function Points (UFP),
14 General System Characteristics (GSC), Value Adjustment Factor (VAF),
and Adjusted Function Points (AFP) for the Library Management System.
"""

from typing import Dict, List, Any

# Standard IFPUG Complexity Weight Matrix
FP_WEIGHTS = {
    'ILF': {'Low': 7, 'Average': 10, 'High': 15},   # Internal Logical Files
    'EIF': {'Low': 5, 'Average': 7,  'High': 10},   # External Interface Files
    'EI':  {'Low': 3, 'Average': 4,  'High': 6},    # External Inputs
    'EO':  {'Low': 4, 'Average': 5,  'High': 7},    # External Outputs
    'EQ':  {'Low': 3, 'Average': 4,  'High': 6}     # External Inquiries
}

DEFAULT_COMPONENTS = [
    # 1. Internal Logical Files (ILF)
    {'type': 'ILF', 'name': 'Books Catalog File', 'det': 12, 'ret': 1, 'complexity': 'Low', 'desc': 'Stores book inventory, ISBN, availability, tier'},
    {'type': 'ILF', 'name': 'Members Directory File', 'det': 10, 'ret': 1, 'complexity': 'Low', 'desc': 'Stores user details, member tier, quotas'},
    {'type': 'ILF', 'name': 'Circulation Borrow Records', 'det': 11, 'ret': 2, 'complexity': 'Average', 'desc': 'Tracks loan transactions, issue/return/renew dates'},
    {'type': 'ILF', 'name': 'Fines Ledger File', 'det': 13, 'ret': 2, 'complexity': 'Average', 'desc': 'Records assessed fines, rules matched, payment status'},
    {'type': 'ILF', 'name': 'Reservations Hold File', 'det': 6, 'ret': 1, 'complexity': 'Low', 'desc': 'Maintains queued reservation requests'},
    {'type': 'ILF', 'name': 'System Settings File', 'det': 4, 'ret': 1, 'complexity': 'Low', 'desc': 'Rule parameters, grace periods, daily rates'},

    # 2. External Interface Files (EIF)
    {'type': 'EIF', 'name': 'Campus Directory Service (LDAP/SSO)', 'det': 6, 'ret': 1, 'complexity': 'Low', 'desc': 'External student/faculty identity validation'},
    {'type': 'EIF', 'name': 'Payment Gateway Interface', 'det': 8, 'ret': 1, 'complexity': 'Average', 'desc': 'External digital receipt and settlement gateway'},

    # 3. External Inputs (EI)
    {'type': 'EI', 'name': 'Add New Book', 'det': 9, 'ftr': 1, 'complexity': 'Low', 'desc': 'Register new acquisition into catalog'},
    {'type': 'EI', 'name': 'Update Book Details', 'det': 8, 'ftr': 1, 'complexity': 'Low', 'desc': 'Modify shelf location or copy count'},
    {'type': 'EI', 'name': 'Register Member', 'det': 8, 'ftr': 1, 'complexity': 'Low', 'desc': 'Enroll new student/faculty/guest'},
    {'type': 'EI', 'name': 'Issue Book Loan', 'det': 7, 'ftr': 3, 'complexity': 'Average', 'desc': 'Check quotas, update available copies, create loan record'},
    {'type': 'EI', 'name': 'Process Book Return', 'det': 8, 'ftr': 3, 'complexity': 'Average', 'desc': 'Assess condition, evaluate overdue days, generate fine'},
    {'type': 'EI', 'name': 'Renew Book Loan', 'det': 5, 'ftr': 2, 'complexity': 'Low', 'desc': 'Verify renewal limits and extend due date'},
    {'type': 'EI', 'name': 'Settle Fine Payment', 'det': 6, 'ftr': 2, 'complexity': 'Average', 'desc': 'Record payment against outstanding balance'},
    {'type': 'EI', 'name': 'Reserve Unavailable Book', 'det': 5, 'ftr': 2, 'complexity': 'Low', 'desc': 'Place waitlist hold on out-of-stock item'},
    {'type': 'EI', 'name': 'Update Rule Configuration', 'det': 5, 'ftr': 1, 'complexity': 'Low', 'desc': 'Adjust grace days, caps, rates'},

    # 4. External Outputs (EO)
    {'type': 'EO', 'name': 'Circulation Checkout Receipt', 'det': 8, 'ftr': 3, 'complexity': 'Average', 'desc': 'Issued book slip with due dates and policies'},
    {'type': 'EO', 'name': 'Overdue Notice & Fine Breakdown', 'det': 12, 'ftr': 3, 'complexity': 'Average', 'desc': 'Formal fine slip displaying matched Decision Rule'},
    {'type': 'EO', 'name': 'Daily Operations & Audit Report', 'det': 14, 'ftr': 4, 'complexity': 'High', 'desc': 'Aggregated circulation and revenue metrics'},
    {'type': 'EO', 'name': 'Inventory & Low Stock Alert Report', 'det': 9, 'ftr': 2, 'complexity': 'Average', 'desc': 'Catalog status and zero-available copies list'},

    # 5. External Inquiries (EQ)
    {'type': 'EQ', 'name': 'Catalog Search & Filter Query', 'det': 7, 'ftr': 1, 'complexity': 'Low', 'desc': 'Search by title, author, category, ISBN'},
    {'type': 'EQ', 'name': 'Member Borrowing Status Inquiry', 'det': 9, 'ftr': 2, 'complexity': 'Low', 'desc': 'Active loans, due dates, current fine balance'},
    {'type': 'EQ', 'name': 'Fine Decision Table Simulation Query', 'det': 6, 'ftr': 1, 'complexity': 'Low', 'desc': 'Interactive fine evaluation simulator'},
    {'type': 'EQ', 'name': 'Book Availability & Hold Position Query', 'det': 6, 'ftr': 2, 'complexity': 'Low', 'desc': 'Live availability and waitlist queue status'}
]

DEFAULT_GSC = [
    {'id': 'C1', 'name': 'Data Communications', 'score': 4, 'desc': 'Web-based application requiring HTTP/HTTPS multi-user client-server communications.'},
    {'id': 'C2', 'name': 'Distributed Data Processing', 'score': 2, 'desc': 'Client-side reactive rendering with centralized server-side SQLite database.'},
    {'id': 'C3', 'name': 'Performance Objectives', 'score': 4, 'desc': 'Sub-second catalog lookup, responsive UI interaction, and immediate fine computation.'},
    {'id': 'C4', 'name': 'Heavily Used Configuration', 'score': 3, 'desc': 'Concurrent checkout, return, and browsing during peak university campus hours.'},
    {'id': 'C5', 'name': 'Transaction Rate', 'score': 3, 'desc': 'Frequent circulation transactions during book issue/return hours.'},
    {'id': 'C6', 'name': 'Online Data Entry', 'score': 5, 'desc': 'All book registration, checkout, returns, and fine payments entered online.'},
    {'id': 'C7', 'name': 'End-User Efficiency', 'score': 5, 'desc': 'Single-page responsiveness, search auto-complete, keyboard friendly, clear visual status.'},
    {'id': 'C8', 'name': 'Online Update', 'score': 4, 'desc': 'Immediate inventory decrement, member quota update, and fine generation on return.'},
    {'id': 'C9', 'name': 'Complex Processing', 'score': 4, 'desc': 'Multi-condition decision table evaluation, grace-period filtering, fine caps, and damage multipliers.'},
    {'id': 'C10', 'name': 'Reusability', 'score': 4, 'desc': 'Modular service layers (fine calculator, circulation, catalog) reusable across CLI and Web.'},
    {'id': 'C11', 'name': 'Installation Ease', 'score': 4, 'desc': 'Single-command launch, SQLite zero-configuration DB, automated migration and seed data.'},
    {'id': 'C12', 'name': 'Operational Ease', 'score': 4, 'desc': 'Automated backup readiness, automated due date tracking, zero manual DB intervention.'},
    {'id': 'C13', 'name': 'Multiple Sites', 'score': 2, 'desc': 'Usable across multiple department libraries with centralized campus database.'},
    {'id': 'C14', 'name': 'Facilitate Change', 'score': 4, 'desc': 'Configurable fine rules, extensible tier schema, clean MVC separation.'}
]

def calculate_fp(custom_gsc_scores: Dict[str, int] = None) -> Dict[str, Any]:
    """
    Computes full Function Point analysis including UFP, TDI, VAF, and AFP.
    """
    gsc_list = []
    tdi = 0
    scores_dict = custom_gsc_scores or {}

    for gsc in DEFAULT_GSC:
        score = scores_dict.get(gsc['id'], gsc['score'])
        score = max(0, min(5, int(score)))
        tdi += score
        gsc_list.append({
            'id': gsc['id'],
            'name': gsc['name'],
            'score': score,
            'desc': gsc['desc']
        })

    # Group components by category
    categories = {'ILF': [], 'EIF': [], 'EI': [], 'EO': [], 'EQ': []}
    type_totals = {'ILF': 0, 'EIF': 0, 'EI': 0, 'EO': 0, 'EQ': 0}
    ufp = 0

    for comp in DEFAULT_COMPONENTS:
        c_type = comp['type']
        comp_level = comp['complexity']
        weight = FP_WEIGHTS[c_type][comp_level]
        comp_copy = dict(comp)
        comp_copy['weight'] = weight
        categories[c_type].append(comp_copy)
        type_totals[c_type] += weight
        ufp += weight

    # VAF Formula: VAF = 0.65 + 0.01 * TDI
    vaf = round(0.65 + (0.01 * tdi), 4)
    # AFP Formula: AFP = UFP * VAF
    afp = round(ufp * vaf, 2)

    # Software Engineering Effort Estimation (Standard Albrecht / Python benchmark)
    # Empirical productivity for Python web app: ~15-20 hours per FP
    hours_per_fp = 16.0
    total_person_hours = round(afp * hours_per_fp, 1)
    # Assuming 4-student team working 10 hours/week each = 40 hours/week team capacity
    weeks_duration = round(total_person_hours / 40.0, 1)

    return {
        'components': DEFAULT_COMPONENTS,
        'categories': categories,
        'type_totals': type_totals,
        'weights_reference': FP_WEIGHTS,
        'unadjusted_fp': ufp,
        'gsc_factors': gsc_list,
        'total_degree_influence': tdi,
        'value_adjustment_factor': vaf,
        'adjusted_fp': afp,
        'effort_estimation': {
            'productivity_rate': f"{hours_per_fp} Person-Hours / FP",
            'total_person_hours': total_person_hours,
            'team_size': 4,
            'estimated_duration_weeks': weeks_duration
        }
    }
