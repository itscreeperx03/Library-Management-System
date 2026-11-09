"""
api.py
======
RESTful API endpoints powering the single-page interactivity of the LMS web application.
"""

from flask import Blueprint, request, jsonify
from app.services.catalog_service import CatalogService
from app.services.member_service import MemberService
from app.services.circulation_service import CirculationService
from app.services.fine_calculator import FineDecisionTable
from app.services.fp_service import calculate_fp

api_bp = Blueprint('api', __name__, url_prefix='/api')

# --- HEALTH CHECK ENDPOINT ---
@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render, cloud monitors, and container orchestrators."""
    try:
        from app.database import get_db_connection
        conn = get_db_connection()
        conn.execute("SELECT 1").fetchone()
        conn.close()
        return jsonify({
            'status': 'healthy',
            'service': 'Athena Library Management System',
            'database': 'connected',
            'version': '2.0.0'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# --- CATALOG ENDPOINTS ---
@api_bp.route('/books', methods=['GET'])
def get_books():
    search = request.args.get('search')
    category = request.args.get('category')
    tier = request.args.get('tier')
    avail = request.args.get('available') == 'true'
    books = CatalogService.get_all_books(search, category, tier, avail)
    return jsonify({'success': True, 'count': len(books), 'books': books})

@api_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = CatalogService.get_book_by_id(book_id)
    if not book:
        return jsonify({'success': False, 'error': 'Book not found'}), 404
    return jsonify({'success': True, 'book': book})

@api_bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json() or {}
    if not data.get('isbn') or not data.get('title') or not data.get('author'):
        return jsonify({'success': False, 'error': 'ISBN, Title, and Author are mandatory fields.'}), 400
    try:
        book = CatalogService.create_book(data)
        return jsonify({'success': True, 'message': 'Book added successfully', 'book': book}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json() or {}
    try:
        book = CatalogService.update_book(book_id, data)
        return jsonify({'success': True, 'message': 'Book updated successfully', 'book': book})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    success, msg = CatalogService.delete_book(book_id)
    status_code = 200 if success else 400
    return jsonify({'success': success, 'message': msg}), status_code

# --- MEMBER ENDPOINTS ---
@api_bp.route('/members', methods=['GET'])
def get_members():
    search = request.args.get('search')
    m_type = request.args.get('member_type')
    status = request.args.get('status')
    members = MemberService.get_all_members(search, m_type, status)
    return jsonify({'success': True, 'count': len(members), 'members': members})

@api_bp.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = MemberService.get_member_by_id(member_id)
    if not member:
        return jsonify({'success': False, 'error': 'Member not found'}), 404
    return jsonify({'success': True, 'member': member})

@api_bp.route('/members', methods=['POST'])
def add_member():
    data = request.get_json() or {}
    if not data.get('member_code') or not data.get('name') or not data.get('email'):
        return jsonify({'success': False, 'error': 'Member code, Name, and Email are required.'}), 400
    try:
        member = MemberService.create_member(data)
        return jsonify({'success': True, 'message': 'Member enrolled successfully', 'member': member}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# --- CIRCULATION ENDPOINTS ---
@api_bp.route('/circulation/issue', methods=['POST'])
def issue_book():
    data = request.get_json() or {}
    book_id = data.get('book_id')
    member_id = data.get('member_id')
    due_days = data.get('due_days')
    notes = data.get('notes')

    if not book_id or not member_id:
        return jsonify({'success': False, 'message': 'Please select both a Member and an available Book.'}), 200

    try:
        b_id = int(book_id)
        m_id = int(member_id)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Invalid Book ID or Member ID format.'}), 200

    d_days = None
    if due_days is not None and str(due_days).strip() != '':
        try:
            d_days = int(due_days)
        except (ValueError, TypeError):
            d_days = None

    success, msg, record = CirculationService.issue_book(b_id, m_id, d_days, notes)
    return jsonify({'success': success, 'message': msg, 'record': record}), 200

@api_bp.route('/circulation/return', methods=['POST'])
def return_book():
    data = request.get_json() or {}
    borrow_id = data.get('borrow_record_id')
    condition = data.get('return_condition', 'Normal')
    notes = data.get('notes')
    simulated_date = data.get('return_date') # Allows testing hypothetical overdue dates!

    if not borrow_id:
        return jsonify({'success': False, 'message': 'Borrow record ID is required.'}), 200

    try:
        br_id = int(borrow_id)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Invalid borrow record ID format.'}), 200

    success, msg, details = CirculationService.return_book(br_id, condition, notes, simulated_date)
    return jsonify({'success': success, 'message': msg, 'details': details}), 200

@api_bp.route('/circulation/renew', methods=['POST'])
def renew_book():
    data = request.get_json() or {}
    borrow_id = data.get('borrow_record_id')
    additional_days = 14
    if data.get('additional_days'):
        try:
            additional_days = int(data.get('additional_days'))
        except (ValueError, TypeError):
            additional_days = 14

    if not borrow_id:
        return jsonify({'success': False, 'message': 'Borrow record ID is required.'}), 200

    try:
        br_id = int(borrow_id)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Invalid borrow record ID format.'}), 200

    success, msg, details = CirculationService.renew_book(br_id, additional_days)
    return jsonify({'success': success, 'message': msg, 'details': details}), 200

@api_bp.route('/circulation/reserve', methods=['POST'])
def reserve_book():
    data = request.get_json() or {}
    book_id = data.get('book_id')
    member_id = data.get('member_id')
    if not book_id or not member_id:
        return jsonify({'success': False, 'message': 'Book ID and Member ID are required.'}), 200

    try:
        b_id = int(book_id)
        m_id = int(member_id)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Invalid Book ID or Member ID format.'}), 200

    success, msg = CirculationService.reserve_book(b_id, m_id)
    return jsonify({'success': success, 'message': msg}), 200

@api_bp.route('/circulation/loans', methods=['GET'])
def get_loans():
    status = request.args.get('status')
    member_id = request.args.get('member_id')
    m_id = int(member_id) if member_id else None
    loans = CirculationService.get_all_loans(status, m_id)
    return jsonify({'success': True, 'count': len(loans), 'loans': loans})

# --- FINES & DECISION TABLE SIMULATOR ---
@api_bp.route('/fines', methods=['GET'])
def get_fines():
    status = request.args.get('status')
    fines = CirculationService.get_all_fines(status)
    return jsonify({'success': True, 'count': len(fines), 'fines': fines})

@api_bp.route('/fines/<int:fine_id>/settle', methods=['POST'])
def settle_fine(fine_id):
    data = request.get_json() or {}
    method = data.get('payment_method', 'Cash')
    success, msg = CirculationService.settle_fine(fine_id, method)
    status_code = 200 if success else 400
    return jsonify({'success': success, 'message': msg}), status_code

@api_bp.route('/fines/simulate', methods=['POST'])
def simulate_fine():
    """
    Live interactive simulation of the Decision Table for Fines.
    Directly tests any hypothetical combination of inputs.
    """
    data = request.get_json() or {}
    days = int(data.get('days_overdue', 0))
    m_type = data.get('member_type', 'Student')
    tier = data.get('book_tier', 'Standard')
    cond = data.get('return_condition', 'Normal')
    cost = float(data.get('replacement_cost', 50.0))
    repeat = bool(data.get('repeat_defaulter', False))

    result = FineDecisionTable.calculate(days, m_type, tier, cond, cost, repeat)
    return jsonify({'success': True, 'result': result.to_dict()})

@api_bp.route('/fines/decision-matrix', methods=['GET'])
def get_decision_matrix():
    matrix = FineDecisionTable.get_decision_matrix()
    return jsonify({'success': True, 'rules': matrix})

# --- FUNCTION POINT ANALYSIS ENDPOINT ---
@api_bp.route('/se/function-points', methods=['GET', 'POST'])
def get_function_points():
    custom_scores = None
    if request.method == 'POST':
        data = request.get_json() or {}
        custom_scores = data.get('gsc_scores', {})
    fp_analysis = calculate_fp(custom_scores)
    return jsonify({'success': True, 'analysis': fp_analysis})

# --- DASHBOARD STATS ---
@api_bp.route('/dashboard/stats', methods=['GET'])
def get_stats():
    stats = CirculationService.get_dashboard_stats()
    return jsonify({'success': True, 'stats': stats})
