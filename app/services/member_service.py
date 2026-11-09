"""
member_service.py
=================
Member directory and patron account management service.
"""

from typing import List, Dict, Any, Optional, Tuple
from app.database import get_db_connection

class MemberService:
    @staticmethod
    def get_all_members(search: str = None, member_type: str = None,
                        status: str = None, db_path: str = None) -> List[Dict[str, Any]]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        query = """
        SELECT m.*,
               (SELECT COUNT(*) FROM borrow_records br WHERE br.member_id = m.id AND br.status IN ('Active', 'Overdue')) as current_borrowed_count,
               COALESCE((SELECT SUM(f.total_fine) FROM fines f WHERE f.member_id = m.id AND f.paid_status = 'Unpaid'), 0.0) as outstanding_fines
        FROM members m
        WHERE 1=1
        """
        params = []

        if search:
            term = f"%{search.strip()}%"
            query += " AND (m.name LIKE ? OR m.member_code LIKE ? OR m.email LIKE ?)"
            params.extend([term, term, term])

        if member_type and member_type != 'All':
            query += " AND m.member_type = ?"
            params.append(member_type)

        if status and status != 'All':
            query += " AND m.status = ?"
            params.append(status)

        query += " ORDER BY m.name ASC"
        cursor.execute(query, params)
        members = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return members

    @staticmethod
    def get_member_by_id(member_id: int, db_path: str = None) -> Optional[Dict[str, Any]]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*,
                   (SELECT COUNT(*) FROM borrow_records br WHERE br.member_id = m.id AND br.status IN ('Active', 'Overdue')) as current_borrowed_count,
                   COALESCE((SELECT SUM(f.total_fine) FROM fines f WHERE f.member_id = m.id AND f.paid_status = 'Unpaid'), 0.0) as outstanding_fines
            FROM members m
            WHERE m.id = ?
        """, (member_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def create_member(data: Dict[str, Any], db_path: str = None) -> Dict[str, Any]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        member_type = data.get('member_type', 'Student')
        # Standard limits by policy: Student: 4 books, 14 days; Faculty: 8 books, 30 days; Guest: 2 books, 7 days
        default_limits = {
            'Student': (4, 14),
            'Faculty': (8, 30),
            'Guest': (2, 7)
        }
        max_books, loan_period = default_limits.get(member_type, (3, 14))
        max_books = int(data.get('max_books', max_books))
        loan_period = int(data.get('loan_period_days', loan_period))

        cursor.execute("""
            INSERT INTO members (member_code, name, email, phone, member_type, status, max_books, loan_period_days)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['member_code'].strip(),
            data['name'].strip(),
            data['email'].strip(),
            data.get('phone', '').strip(),
            member_type,
            data.get('status', 'Active'),
            max_books,
            loan_period
        ))
        member_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return MemberService.get_member_by_id(member_id, db_path)

    @staticmethod
    def check_eligibility(member_id: int, db_path: str = None) -> Tuple[bool, str]:
        """Verify if member is eligible to borrow a book."""
        member = MemberService.get_member_by_id(member_id, db_path)
        if not member:
            return False, "Member not found."

        if member['status'] != 'Active':
            return False, f"Member account is {member['status']}. Borrowing privileges suspended."

        if member['current_borrowed_count'] >= member['max_books']:
            return False, f"Maximum borrow limit reached ({member['current_borrowed_count']}/{member['max_books']} books held)."

        if member['outstanding_fines'] > 15.0:
            return False, f"Outstanding unpaid fines (${member['outstanding_fines']:.2f}) exceed policy threshold ($15.00). Settle fines first."

        return True, "Eligible"
