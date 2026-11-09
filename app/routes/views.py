"""
views.py
========
Web view controllers rendering HTML templates for the Library Management System.
"""

from flask import Blueprint, render_template
from app.services.circulation_service import CirculationService
from app.services.catalog_service import CatalogService
from app.services.member_service import MemberService
from app.services.fine_calculator import FineDecisionTable
from app.services.fp_service import calculate_fp

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    stats = CirculationService.get_dashboard_stats()
    recent_loans = CirculationService.get_all_loans()[:6]
    pending_fines = CirculationService.get_all_fines(paid_status='Unpaid')[:5]
    return render_template('index.html', stats=stats, recent_loans=recent_loans, pending_fines=pending_fines)

@views_bp.route('/books')
def books_view():
    books = CatalogService.get_all_books()
    categories = CatalogService.get_categories()
    return render_template('books.html', books=books, categories=categories)

@views_bp.route('/members')
def members_view():
    members = MemberService.get_all_members()
    return render_template('members.html', members=members)

@views_bp.route('/circulation')
def circulation_view():
    active_loans = CirculationService.get_all_loans(status_filter='Active')
    overdue_loans = [loan for loan in CirculationService.get_all_loans() if loan['is_overdue']]
    books = CatalogService.get_all_books(available_only=True)
    members = [m for m in MemberService.get_all_members() if m['status'] == 'Active']
    return render_template('circulation.html', active_loans=active_loans, overdue_loans=overdue_loans, books=books, members=members)

@views_bp.route('/fines')
def fines_view():
    fines = CirculationService.get_all_fines()
    rules = FineDecisionTable.get_decision_matrix()
    return render_template('fines.html', fines=fines, rules=rules)

@views_bp.route('/se-dossier')
def se_dossier_view():
    fp_data = calculate_fp()
    decision_rules = FineDecisionTable.get_decision_matrix()
    return render_template('documentation.html', fp_data=fp_data, decision_rules=decision_rules)

@views_bp.route('/reports')
def reports_view():
    stats = CirculationService.get_dashboard_stats()
    fp_data = calculate_fp()
    return render_template('reports.html', stats=stats, fp_data=fp_data)
